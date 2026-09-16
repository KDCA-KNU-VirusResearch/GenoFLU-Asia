#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

import os
import sys
import re
import shutil
import glob
import argparse
import textwrap
import tempfile
import pandas as pd
from collections import defaultdict
from datetime import datetime

from Bio import SeqIO

# Fixed study criterion for reference-based segment assignment.
PIDENT_THRESHOLD = 97.0

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
    Write one new, uniquely named workbook for the current invocation.
    """
    def __init__(self, output_dir):
        self.output_dir = os.path.abspath(output_dir)
        self.date_stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')

    def write_all_results_rows(self, rows):
        """
        rows: a list of dictionaries, with one result row per virus.
        """
        if not rows:
            raise RuntimeError('No result rows were produced; no workbook was saved.')
        os.makedirs(self.output_dir, exist_ok=True)
        # Exclusive creation adds a random suffix, preventing same-time collisions.
        fd, filename = tempfile.mkstemp(prefix=f'genoflu_results_{self.date_stamp}_',
                                        suffix='.xlsx', dir=self.output_dir)
        os.close(fd)
        try:
            pd.DataFrame(rows).to_excel(filename, sheet_name='All Results', index=False)
        except BaseException:
            os.unlink(filename)
            raise
        return filename


class Blast_Fasta(bcolors):
    """
    Run BLAST against the specified database and retain the output file and raw lines.
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


# Parse the virus ID from the text before the first '|'.
def parse_query_virus_id(header: str) -> str:
    """
    Use the text before the first '|', stripping leading and trailing whitespace.
    Example: '>A/.../2022|PB2' -> 'A/.../2022'
    If '|' is absent, use the first whitespace-delimited token.
    """
    h = header.lstrip('>').strip()
    if '|' in h:
        return h.split('|', 1)[0].strip()
    return h.split()[0] if h else 'SINGLE_SAMPLE'


class GenoFLU():
    """
    Support multi-virus FASTA input:
    - Extract virus IDs from query headers and group hits by virus.
    - Assign a genotype when all eight accepted segments (>=97% identity) match the key.
    """

    def __init__(self, FASTA=None, FASTA_dir=None, cross_reference=None, sample_name=None, debug=False):
        self.debug = debug
        self.FASTA_abs_path = FASTA
        FASTA_name = os.path.basename(self.FASTA_abs_path)

        # Count FASTA headers (the number of input sequences).
        with open(self.FASTA_abs_path, 'r') as f:
            fastas_in_file = sum(1 for line in f if line.startswith('>'))
        self.fastas_in_file = fastas_in_file

        if sample_name:
            sample_name = sample_name
        else:
            # Default to the filename prefix before the first '_' or '.'.
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
        - Build the local reference database (hpai_geno_db).
        - Run BLAST on the input FASTA.
        - Group hits as {gene: blast_result} for each virus ID.
        - Load the genotype key and assign genotypes.
        """
        # Build the BLAST database.
        os.system(
            f'cat {self.FASTA_dir}/*.fasta | makeblastdb -dbtype nucl -out hpai_geno_db -title hpai_geno_db > /dev/null 2>&1'
        )

        # Run BLAST with one subject alignment requested; multiple HSPs may be returned.
        blast_hpai_genotyping = Blast_Fasta(
            FASTA=self.FASTA_abs_path,
            format="6 qseqid qseq length nident pident mismatch evalue bitscore sacc stitle",
            num_alignment=1,
            blast_db='hpai_geno_db',
            num_threads=2
        )

        blast_genotyping_by_virus = defaultdict(dict)

        # Require reference titles in segment_group|reference_id|gene format.
        for line in blast_hpai_genotyping._raw_lines:
            cols = line.split('\t')
            if len(cols) < 10:
                continue

            qseqid, qseq, length, nident, pident, mismatch, evalue, bitscore, sacc, stitle = cols[:10]

            # Extract the gene from the reference title.
            parts = re.split(r'[|]', stitle)
            if len(parts) < 3:
                raise SystemExit(f"Invalid reference FASTA header (expected segment_group|reference_id|gene): {stitle}")
            gene = parts[2]

            # Extract the virus ID from the query header.
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

        # Report detected virus groups and segment counts.
        self.blast_genotyping_by_virus = dict(blast_genotyping_by_virus)
        if self.debug:
            print("\n[DEBUG] Detected virus_id groups and segment counts:")
            for vid, gm in sorted(self.blast_genotyping_by_virus.items()):
                try:
                    genes_sorted = sorted(gm.keys())
                except Exception:
                    genes_sorted = list(gm.keys())
                print(f"  - {vid}: {len(gm)} segments, genes={genes_sorted}")
            print()

        # Collect temporary BLAST files; remove them unless debug mode is enabled.
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

        # Load the genotype key using unique internal keys for duplicate names.
        df = pd.read_excel(self.cross_reference)

        # dictionary_of_genotypes: internal_key -> 8seg dict
        dictionary_of_genotypes = {}
        # genotype_display_name: internal_key -> original genotype name for output
        genotype_display_name = {}

        for idx, row in df.iterrows():
            gname = str(row['Genotype']).strip()
            internal_key = f"{gname}__{idx+1:04d}"  # Examples: G1__0001, G1__0002

            dictionary_of_genotypes[internal_key] = {
                'PB2': row['PB2'], 'PB1': row['PB1'], 'PA': row['PA'],
                'HA': row['HA'], 'NP': row['NP'], 'NA': row['NA'],
                'MP': row['MP'], 'NS': row['NS'],
            }
            genotype_display_name[internal_key] = gname

        self.genotype_display_name = genotype_display_name

        # Match the accepted segment combination for each virus.
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
                # Accept only alignments with at least 97% identity.
                try:
                    pid = float(value["pident"])
                except Exception:
                    pid = 0.0
                if pid >= PIDENT_THRESHOLD:
                    sample_dict[gene] = genotype
                    used_list.append(f'{gene}:{genotype}')

            matching_genotype = False
            result = {'matching_genotype': False, 'genotype': 'No Match', 'genotyped_segments': 'No Findings'}

            for gkey, gsegments in dictionary_of_genotypes.items():
                if sample_dict == gsegments:
                    matching_genotype = True
                    # Report the original genotype name rather than the internal key.
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
                        f'Not assigned: Only {segcnt} segments >=97% match found of total {total_in_sample} segments in this sample'
                    )

            self.results_per_virus[virus_id] = result
            self.genotype_list_used_per_virus[virus_id] = used_list

    def excel_rows(self):
        """
        Build a list of result dictionaries for the combined workbook.
        """
        rows = []
        for virus_id, result in self.results_per_virus.items():
            gene_map = self.blast_genotyping_by_virus.get(virus_id, {})
            full_sample_title_list = []
            pident_list = []
            mismatch_list = []
            coverage_list = []  # Read-depth coverage is unavailable from FASTA input.

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
            Write one new genoflu_results_DATE_TIME_ID.xlsx per invocation.
            Multiple FASTA files and viruses are combined in the "All Results" sheet.
            With -d/--debug, print virus groups and their segment counts/genes and retain temporary files.
            Duplicate Genotype names in genotype_key_asia.xlsx are supported safely (internal unique keys).
        '''), epilog='''---------------------------------------------------------'''
    )

    parser.add_argument('-f', '--fasta', nargs='+', dest='FASTA', required=True, help='One or more assembled FASTA files')
    parser.add_argument('-o', '--output', default='.', help='Output directory for a new timestamped workbook (default: current directory)')
    parser.add_argument('-i', '--FASTA_dir', action='store', dest='FASTA_dir', default=None,
                        help='Reference FASTA directory. Default: dependencies/asia_fastas beside this script')
    parser.add_argument('-c', '--cross_reference', action='store', dest='cross_reference', default=None,
                        help='Genotype key Excel file. Default: dependencies/genotype_key_asia.xlsx beside this script. Columns: Genotype + 8 segments.')
    parser.add_argument('-n', '--sample_name', action='store', dest='sample_name',
                        required=False, help='Force output files to this sample name')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', default=False, help='print debug details and keep temporary files')
    parser.add_argument('-v', '--version', action='version',
                        version=f'{os.path.basename(__file__)}: version {__version__}')
    args = parser.parse_args()

    print(f'\n{os.path.basename(__file__)} set arguments:\n')
    for key, value in vars(args).items():
        print(f'\t{key}:  {value}')
    print("\n")

    excel_stats = Excel_Stats(args.output)
    all_rows = []
    for input_fasta in args.FASTA:
        # Resolve input paths.
        FASTA_abs_path = os.path.abspath(input_fasta)
        try:
            FASTA_dir = os.path.abspath(args.FASTA_dir) if args.FASTA_dir else None
        except TypeError:
            FASTA_dir = args.FASTA_dir
        try:
            cross_reference = os.path.abspath(args.cross_reference) if args.cross_reference else None
        except TypeError:
            cross_reference = args.cross_reference

        # Run GenoFLU-Asia.
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

        # Accumulate only this invocation; publish after every input succeeds.
        all_rows.extend(genoflu.excel_rows())

        # Print genotype assignments.
        for virus_id, result in genoflu.results_per_virus.items():
            used = ', '.join(genoflu.genotype_list_used_per_virus.get(virus_id, []))
            print(f'\n{genoflu.sample_name}__{virus_id} Genotype --> {result["genotype"]}: {used}\n')

        # Clean up temporary files.
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

    output_file = excel_stats.write_all_results_rows(all_rows)
    print(f"Results: {output_file}")

# Created 2023 by Tod Stuber
# GenoFLU-Asia adaptation: multi-virus input and combined workbook output.
