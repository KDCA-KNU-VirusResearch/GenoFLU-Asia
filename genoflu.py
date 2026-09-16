#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "1.13-combined-only-debug-dup-genotype-safe"

import os
import sys
import re
import shutil
import glob
import argparse
import textwrap
import pandas as pd
from collections import defaultdict
from datetime import datetime

from Bio import SeqIO

combined_excel_filename = "genoflu_combined_results.xlsx"


class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


class Excel_Stats:
    """
    통합 파일("genoflu_combined_results.xlsx")의 "All Results" 시트에만 누적 저장.
    """
    def __init__(self, sample_name):
        self.sample_name = sample_name
        self.date_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    def write_all_results_rows(self, rows):
        """
        rows: 리스트[dict] 형태. 각 dict가 한 행(한 바이러스)의 결과
        """
        df = pd.DataFrame(rows)
        if os.path.exists(combined_excel_filename):
            with pd.ExcelWriter(combined_excel_filename, mode='a', if_sheet_exists='overlay') as writer:
                if "All Results" in writer.sheets:
                    start_row = writer.sheets["All Results"].max_row
                    df.to_excel(writer, sheet_name="All Results", index=False, header=False, startrow=start_row)
                else:
                    df.to_excel(writer, sheet_name="All Results", index=False)
        else:
            df.to_excel(combined_excel_filename, sheet_name="All Results", index=False)


class Blast_Fasta(bcolors):
    """
    입력 FASTA를 지정된 DB에 대해 BLAST 수행, 결과를 파일로 남기고 raw 라인 보관.
    """
    def __init__(
        self,
        FASTA=None,
        format="6 qseqid qseq length nident pident mismatch evalue bitscore sacc stitle",
        num_alignment=1,
        blast_db="hpai_geno_db",
        num_threads=2
    ):
        FASTA_abs_path = FASTA
        FASTA_name = os.path.basename(FASTA_abs_path)
        sample_name = re.sub('[_.].*', '', FASTA_name)
        self.sample_name = sample_name
        self.blast_db = blast_db
        blastout_file = f'{sample_name}_blast_out.txt'
        os.system(
            f'blastn -query {FASTA_abs_path} -db {blast_db} -word_size 11 '
            f'-out {blastout_file} -outfmt "{format}" -num_alignments {num_alignment} '
            f'-num_threads={num_threads} 2> /dev/null'
        )
        self.blastout_file = blastout_file

        self._raw_lines = []
        with open(blastout_file, 'r') as f:
            for line in f:
                self._raw_lines.append(line.rstrip('\n'))


# 샘플 ID 파싱: '|' 앞의 전체 문자열을 샘플 ID로 사용 (안정화)
def parse_query_virus_id(header: str) -> str:
    """
    샘플 ID = '|' 앞의 전체 문자열(양끝 공백 제거)
    예) '>A/.../2022|PB2' -> 'A/.../2022'
    '|'가 없으면 첫 공백 전까지 토큰 사용
    """
    h = header.lstrip('>').strip()
    if '|' in h:
        return h.split('|', 1)[0].strip()
    return h.split()[0] if h else 'SINGLE_SAMPLE'


class GenoFLU():
    """
    다중 샘플 FASTA 지원:
    - 쿼리 헤더에서 virus_id를 추출하여 바이러스 단위로 그룹핑
    - 각 바이러스에 대해 8개 분절이 ≥97%로 일치하면 genotype 부여
    """

    def __init__(self, FASTA=None, FASTA_dir=None, cross_reference=None, sample_name=None, debug=False):
        self.debug = debug
        self.FASTA_abs_path = FASTA
        FASTA_name = os.path.basename(self.FASTA_abs_path)

        # 헤더 개수(= 파일 내 시퀀스 수)
        with open(self.FASTA_abs_path, 'r') as f:
            fastas_in_file = sum(1 for line in f if line.startswith('>'))
        self.fastas_in_file = fastas_in_file

        if sample_name:
            sample_name = sample_name
        else:
            # 기본 sample_name은 파일명에서 첫 '_' 또는 '.' 앞부분
            sample_name = re.sub('[_.].*', '', FASTA_name)
        self.sample_name = sample_name

        # Default to the Asia references shipped beside this script.
        script_path = os.path.dirname(os.path.realpath(__file__))
        self.FASTA_dir = FASTA_dir or os.path.join(script_path, 'dependencies', 'asia_fastas')
        self.cross_reference = cross_reference or os.path.join(script_path, 'dependencies', 'genotype_key_asia.xlsx')

    def get_metadata(self,):
        try:
            import dvl_metadata_capture
        except Exception:
            return
        sample_name = self.sample_name
        root_name = re.sub('-submissionfile', '', sample_name)
        metadata_dict = dvl_metadata_capture.get_metadata(root_name)
        if not metadata_dict:
            metadata_dict = {}
        try:
            metadata_dict["Collection Year"] = int(metadata_dict["Collection Year"])
        except (TypeError, ValueError, KeyError):
            metadata_dict["Collection Year"] = "n/a"
        try:
            metadata_format_string = (
                f'A/{metadata_dict.get("species")}/{metadata_dict.get("state")}/'
                f'{root_name}/{metadata_dict["Collection Year"]}'
            )
        except Exception:
            metadata_format_string = 'No Metadata'
        self.metadata_dict = metadata_dict
        self.metadata_format_string = metadata_format_string

    def blast_hpai_genomes(self,):
        """
        - 내부 DB(hpai_geno_db) 생성
        - 입력 FASTA BLAST
        - 결과를 virus_id별로 {gene: blast_result}로 그룹핑
        - genotype cross-reference 로드 및 판정
        """
        # DB 생성
        os.system(
            f'cat {self.FASTA_dir}/*.fasta | makeblastdb -dbtype nucl -out hpai_geno_db -title hpai_geno_db > /dev/null 2>&1'
        )

        # BLAST 실행 (최상위 히트 1개)
        blast_hpai_genotyping = Blast_Fasta(
            FASTA=self.FASTA_abs_path,
            format="6 qseqid qseq length nident pident mismatch evalue bitscore sacc stitle",
            num_alignment=1,
            blast_db='hpai_geno_db',
            num_threads=2
        )

        blast_genotyping_by_virus = defaultdict(dict)

        # stitle = Genotype|Sample|Gene 형식이 필요
        for line in blast_hpai_genotyping._raw_lines:
            cols = line.split('\t')
            if len(cols) < 10:
                continue

            qseqid, qseq, length, nident, pident, mismatch, evalue, bitscore, sacc, stitle = cols[:10]

            # stitle에서 gene 추출
            parts = re.split(r'[|]', stitle)
            if len(parts) < 3:
                raise SystemExit(f"❌ DB FASTA header 형식 오류 (예상: Genotype|Sample|Gene) → {stitle}")
            gene = parts[2]

            # 쿼리 헤더에서 virus_id 추출
            virus_id = parse_query_virus_id(qseqid)

            each_blast = {
                'blast_length': length,
                'nident': nident,
                'pident': pident,
                'mismatch': mismatch,
                'evalue': evalue,
                'bitscore': bitscore,
                'sacc': sacc,
                'stitle': stitle,
                'gene': gene,
                'qseqid': qseqid,
            }

            # Rank hits within each virus/gene by bitscore, then alignment length, then identity.
            best = blast_genotyping_by_virus[virus_id].get(gene)
            cur_p = float(each_blast['pident'])
            cur_bs = float(each_blast['bitscore'])
            cur_len = float(each_blast['blast_length'])
            if best is None:
                blast_genotyping_by_virus[virus_id][gene] = each_blast
            else:
                best_p = float(best['pident'])
                best_bs = float(best['bitscore'])
                best_len = float(best['blast_length'])
                if (cur_bs > best_bs) or (cur_bs == best_bs and (cur_len > best_len or (cur_len == best_len and cur_p > best_p))):
                    blast_genotyping_by_virus[virus_id][gene] = each_blast

        # ===== 디버그 출력 =====
        self.blast_genotyping_by_virus = dict(blast_genotyping_by_virus)
        print("\n[DEBUG] Detected virus_id groups and segment counts:")
        for vid, gm in sorted(self.blast_genotyping_by_virus.items()):
            try:
                genes_sorted = sorted(gm.keys())
            except Exception:
                genes_sorted = list(gm.keys())
            print(f"  - {vid}: {len(gm)} segments, genes={genes_sorted}")
        print()

        # 임시 파일 정리(디버그가 아니면 BLAST 결과 디렉토리 제거)
        blast_dir = f'{self.sample_name}_blast_hpia_genotyping_dir'
        os.makedirs(blast_dir, exist_ok=True)
        files_grab = []
        for patt in ('*_blast*txt', 'batch.sh',):
            files_grab.extend(glob.glob(patt))
        for each in files_grab:
            try:
                shutil.move(each, blast_dir)
            except Exception:
                pass
        if not self.debug:
            shutil.rmtree(blast_dir, ignore_errors=True)

        # ===== genotype cross-reference 로드 (중복 Genotype 안전) =====
        df = pd.read_excel(self.cross_reference)

        # dictionary_of_genotypes: internal_key -> 8seg dict
        dictionary_of_genotypes = {}
        # genotype_display_name: internal_key -> original genotype string (출력용)
        genotype_display_name = {}

        for idx, row in df.iterrows():
            gname = str(row['Genotype']).strip()
            internal_key = f"{gname}__{idx+1:04d}"  # 예: G1__0001, G1__0002

            dictionary_of_genotypes[internal_key] = {
                'PB2': row['PB2'], 'PB1': row['PB1'], 'PA': row['PA'],
                'HA': row['HA'], 'NP': row['NP'], 'NA': row['NA'],
                'MP': row['MP'], 'NS': row['NS'],
            }
            genotype_display_name[internal_key] = gname

        self.genotype_display_name = genotype_display_name

        # ===== 바이러스(샘플)별 genotype 매칭 =====
        self.results_per_virus = {}
        self.genotype_list_used_per_virus = {}

        for virus_id, gene_map in self.blast_genotyping_by_virus.items():
            sample_dict = {}
            used_list = []
            for gene, value in gene_map.items():
                try:
                    genotype, sample, gene_from_title = re.split('[|]', value["stitle"])
                except ValueError:
                    sys.exit(f'SEE TYPO in Database Input File with Header: {value["stitle"]}')
                # 97% 이상만 채택
                try:
                    pid = float(value["pident"])
                except Exception:
                    pid = 0.0
                if pid >= 97.0:
                    sample_dict[gene] = genotype
                    used_list.append(f'{gene}:{genotype}')

            matching_genotype = False
            result = {'matching_genotype': False, 'genotype': 'No Match', 'genotyped_segments': 'No Findings'}

            for gkey, gsegments in dictionary_of_genotypes.items():
                if sample_dict == gsegments:
                    matching_genotype = True
                    # ✅ 내부키(gkey)가 아니라 원래 genotype 이름으로 출력
                    result = {
                        'matching_genotype': True,
                        'genotype': self.genotype_display_name.get(gkey, gkey),
                        'genotyped_segments': gsegments
                    }
                    break

            if not matching_genotype:
                segcnt = len(sample_dict)
                total_in_sample = len(gene_map)
                if segcnt == 8:
                    result['genotype'] = "Not assigned: No Matching Genotypes"
                else:
                    result['genotype'] = (
                        f'Not assigned: Only {segcnt} segments >97% match found of total {total_in_sample} segments in this sample'
                    )

            self.results_per_virus[virus_id] = result
            self.genotype_list_used_per_virus[virus_id] = used_list

    def excel_rows(self):
        """
        통합 파일에 기록할 rows(dict 리스트) 생성
        """
        rows = []
        for virus_id, result in self.results_per_virus.items():
            gene_map = self.blast_genotyping_by_virus.get(virus_id, {})
            full_sample_title_list = []
            pident_list = []
            mismatch_list = []
            coverage_list = []  # FASTA 기반이라 coverage 없음

            for g, v in gene_map.items():
                genotype, sample, gene_from_title = re.split('[|]', v["stitle"])
                full_sample_title_list.append(f'{gene_from_title}:{genotype}:{sample}')
                try:
                    pident_list.append(f'{float(v["pident"]):0.2f}%')
                except Exception:
                    pident_list.append('NA')
                try:
                    mismatch_list.append(f'{int(float(v["mismatch"])):,}')
                except Exception:
                    mismatch_list.append('NA')

            if not coverage_list:
                coverage_list.append('ave_cov_depth_na')

            row = {
                'sample': f'{self.sample_name}__{virus_id}',
                'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                'File Name': os.path.basename(self.FASTA_abs_path),
                'Genotype': result['genotype'],
                'Genotype List Used, >=97%': ', '.join(self.genotype_list_used_per_virus.get(virus_id, [])),
                'Genotype Sample Title List': ', '.join(full_sample_title_list),
                'Genotype Percent Match List': ', '.join(pident_list),
                'Genotype Mismatch List': ', '.join(mismatch_list),
                'Genotype Average Depth of Coverage List': 'Ran on FASTA - No Coverage Report',
            }
            if hasattr(self, 'metadata_format_string'):
                row['Metadata'] = self.metadata_format_string

            try:
                column_order = list(row.keys())
                column_order.remove('File Name')
                column_order.insert(2, 'File Name')
                row = {k: row[k] for k in column_order}
            except ValueError:
                pass

            rows.append(row)
        return rows


if __name__ == "__main__":  # execute if directly accessed by the interpreter
    parser = argparse.ArgumentParser(
        prog='genoflu.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\

        ---------------------------------------------------------
        Usage:
            genoflu.py -f sample.fasta # -i and -c default to the bundled Asia references
        -f is the input FASTA file which the genotype will be determined
        -i is the directory containing FASTAs to BLAST against. Headers must follow specific format. "Genotype|Sample|Gene"
        -c is the genotype key. Default: dependencies/genotype_key_asia.xlsx beside this script
        -n is the sample name to force output files to this sample name versus taking the name to be anything before [_.]

        Summary:
            Combined-only mode: writes ONLY "genoflu_combined_results.xlsx" (no per-file xlsx/tsv).
            Multi-sample FASTA is supported; rows are appended per virus in "All Results" sheet.
            DEBUG prints detected virus_id groups and their segment counts/genes.
            Duplicate Genotype names in genotype_key_asia.xlsx are supported safely (internal unique keys).
        '''), epilog='''---------------------------------------------------------'''
    )

    parser.add_argument('-f', '--fasta', action='store', dest='FASTA', required=True, help='Assembled FASTA')
    parser.add_argument('-i', '--FASTA_dir', action='store', dest='FASTA_dir', default=None,
                        help='Reference FASTA directory. Default: dependencies/asia_fastas beside this script')
    parser.add_argument('-c', '--cross_reference', action='store', dest='cross_reference', default=None,
                        help='Genotype key Excel file. Default: dependencies/genotype_key_asia.xlsx beside this script. Columns: Genotype + 8 segments.')
    parser.add_argument('-n', '--sample_name', action='store', dest='sample_name',
                        required=False, help='Force output files to this sample name')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', default=False, help='keep temp files')
    parser.add_argument('-v', '--version', action='version',
                        version=f'{os.path.basename(__file__)}: version {__version__}')
    args = parser.parse_args()

    print(f'\n{os.path.basename(__file__)} set arguments:\n')
    for key, value in vars(args).items():
        print(f'\t{key}:  {value}')
    print("\n")

    # 절대 경로 처리
    FASTA_abs_path = os.path.abspath(args.FASTA)
    try:
        FASTA_dir = os.path.abspath(args.FASTA_dir) if args.FASTA_dir else None
    except TypeError:
        FASTA_dir = args.FASTA_dir
    try:
        cross_reference = os.path.abspath(args.cross_reference) if args.cross_reference else None
    except TypeError:
        cross_reference = args.cross_reference

    # GenoFLU 실행
    genoflu = GenoFLU(
        FASTA=FASTA_abs_path,
        FASTA_dir=FASTA_dir,
        cross_reference=cross_reference,
        sample_name=args.sample_name,
        debug=args.debug
    )

    try:
        genoflu.get_metadata()
    except Exception:
        pass

    genoflu.blast_hpai_genomes()

    # 통합 파일에만 기록
    excel_stats = Excel_Stats(genoflu.sample_name)
    rows = genoflu.excel_rows()
    excel_stats.write_all_results_rows(rows)

    # 콘솔 출력
    for virus_id, result in genoflu.results_per_virus.items():
        used = ', '.join(genoflu.genotype_list_used_per_virus.get(virus_id, []))
        print(f'\n{genoflu.sample_name}__{virus_id} Genotype --> {result["genotype"]}: {used}\n')

    # 임시 파일 정리
    temp_dir = f'{FASTA_abs_path}.temp'
    os.makedirs(temp_dir, exist_ok=True)
    files_grab = []
    for patt in ('hpai_geno_db.*', 'slurm*.out'):
        files_grab.extend(glob.glob(patt))
    for each in files_grab:
        try:
            shutil.move(each, temp_dir)
        except Exception:
            pass

    if args.debug is False:
        shutil.rmtree(temp_dir, ignore_errors=True)

# Created 2023 by Tod Stuber
# Combined-only, multi-sample & debug extension 2025 by ChatGPT
