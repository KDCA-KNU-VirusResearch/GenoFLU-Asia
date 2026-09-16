#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-only
# Based on GenoFLU by Tod Stuber; see LICENSE and the upstream repository.

__version__ = "1.0"

import os
import sys
import re
import shutil
import glob
import argparse
import textwrap
import tempfile
import subprocess
import pandas as pd
from datetime import datetime


# Fixed study criterion for reference-based segment assignment.
PIDENT_THRESHOLD = 97.0


def run_external(command, input_data=None, cwd=None):
    """Run a tool without a shell and stop with its diagnostics on failure."""
    try:
        result = subprocess.run(command, input=input_data, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=True, cwd=cwd)
    except FileNotFoundError:
        raise SystemExit(f'Error: {command[0]} was not found. Activate the environment containing BLAST+.')
    except subprocess.CalledProcessError as exc:
        diagnostic = (exc.stderr or exc.stdout or b'No diagnostic output.').decode('utf-8', errors='replace').strip()
        raise SystemExit(f'Error: {command[0]} failed (exit code {exc.returncode}).\n{diagnostic}')
    except OSError as exc:
        raise SystemExit(f'Error: unable to run {command[0]}: {exc}')
    if result.stderr:
        print(result.stderr.decode('utf-8', errors='replace').rstrip(), file=sys.stderr)
    return result

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
        num_threads=2,
        working_dir=None
    ):
        FASTA_abs_path = FASTA
        FASTA_name = os.path.basename(FASTA_abs_path)
        sample_name = os.path.splitext(FASTA_name)[0]
        self.sample_name = sample_name
        self.blast_db = blast_db
        blastout_file = os.path.join(working_dir or '.', 'query_blast_out.txt')
        run_external(['blastn', '-query', FASTA_abs_path, '-db', blast_db,
                      '-word_size', '11', '-out', blastout_file, '-outfmt', format,
                      '-num_alignments', str(num_alignment), '-num_threads', str(num_threads)], cwd=working_dir)
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


def inspect_fasta(path):
    """Validate nucleotide FASTA and inventory every virus, including no-hit queries."""
    viruses = {}
    query_ids = set()
    current = None
    bases = 0
    record_count = 0
    allowed = set('ACGTURYSWKMBDHVN-')
    def invalid(message):
        raise SystemExit(f'Error: invalid FASTA {path}: {message}')
    try:
        with open(path, encoding='utf-8-sig') as handle:
            for line_number, raw in enumerate(handle, 1):
                line = raw.strip()
                if not line:
                    continue
                if line.startswith('>'):
                    if current is not None and bases == 0:
                        invalid(f'empty sequence for {current}')
                    header = line[1:].strip()
                    if not header:
                        invalid(f'empty header at line {line_number}')
                    query_id = header.split()[0]
                    if '|' in header and '|' not in query_id:
                        invalid(f'whitespace in virus ID at line {line_number}; use underscores')
                    if query_id in query_ids:
                        invalid(f'duplicate sequence ID at line {line_number}: {query_id}')
                    virus_id = parse_query_virus_id(query_id)
                    if not virus_id:
                        invalid(f'empty virus ID at line {line_number}')
                    query_ids.add(query_id)
                    viruses[virus_id] = viruses.get(virus_id, 0) + 1
                    record_count += 1
                    current, bases = query_id, 0
                else:
                    if current is None:
                        invalid(f'sequence before the first > header at line {line_number}')
                    sequence = ''.join(line.split()).upper()
                    bad = set(sequence) - allowed
                    if bad:
                        invalid(f'invalid nucleotide character(s) {sorted(bad)} at line {line_number}')
                    bases += len(sequence.replace('-', ''))
        if current is None:
            invalid('no sequence records')
        if bases == 0:
            invalid(f'empty sequence for {current}')
    except (OSError, UnicodeError) as exc:
        invalid(str(exc))
    return viruses, record_count


def blast_workspace():
    """Honor configured scratch storage while avoiding BLAST's unsafe DB paths."""
    parent = os.path.abspath(os.environ.get('GENOFLU_TMPDIR') or
                             os.environ.get('TMPDIR') or tempfile.gettempdir())
    if not re.fullmatch(r'[A-Za-z0-9_./-]+', os.path.realpath(parent)):
        raise SystemExit('Error: BLAST scratch path must use ASCII letters, numbers, _, -, / and .; '
                         'set GENOFLU_TMPDIR to a writable path without spaces. '
                         f'Configured path: {parent}')
    try:
        return tempfile.TemporaryDirectory(prefix='genoflu_blast_', dir=parent)
    except OSError as exc:
        raise SystemExit(f'Error: cannot create BLAST scratch directory in {parent}: {exc}')


class GenoFLU():
    """
    Support multi-virus FASTA input:
    - Extract virus IDs from query headers and group hits by virus.
    - Assign a genotype when all eight accepted segments (>=97% identity) match the key.
    """

    def __init__(self, FASTA=None, FASTA_dir=None, cross_reference=None, sample_name=None, debug=False, input_inventory=None):
        self.debug = debug
        self.FASTA_abs_path = FASTA
        FASTA_name = os.path.basename(self.FASTA_abs_path)

        self.input_viruses, self.fastas_in_file = (
            input_inventory if input_inventory is not None else inspect_fasta(self.FASTA_abs_path))

        if sample_name:
            sample_name = sample_name
        else:
            # Retain the entire filename stem to distinguish batch_alpha and batch_beta.
            sample_name = os.path.splitext(FASTA_name)[0]
        self.sample_name = sample_name

        # Default to the Asia references shipped beside this script.
        script_path = os.path.dirname(os.path.realpath(__file__))
        self.FASTA_dir = FASTA_dir or os.path.join(script_path, 'dependencies', 'asia_fastas')
        self.cross_reference = cross_reference or os.path.join(script_path, 'dependencies', 'genotype_key_asia.xlsx')

    def blast_hpai_genomes(self,):
        """
        - Build the local reference database (hpai_geno_db).
        - Run BLAST on the input FASTA.
        - Group hits as {gene: blast_result} for each virus ID.
        - Load the genotype key and assign genotypes.
        """
        # Build the BLAST database.
        reference_files = sorted(glob.glob(os.path.join(self.FASTA_dir, '*.fasta')))
        if not reference_files:
            raise SystemExit(f'Error: no reference FASTA files found in {self.FASTA_dir}')
        reference_data = bytearray()
        for reference_file in reference_files:
            try:
                with open(reference_file, 'rb') as reference:
                    reference_data.extend(reference.read())
            except OSError as exc:
                raise SystemExit(f'Error: cannot read reference FASTA {reference_file}: {exc}')
        # BLAST may split database paths containing spaces internally. Stage all
        # tool inputs in a simple Linux temporary path, independent of user paths.
        with blast_workspace() as work:
            query = os.path.join(work, 'query.fasta')
            shutil.copyfile(self.FASTA_abs_path, query)
            try:
                run_external(['makeblastdb', '-dbtype', 'nucl', '-out', 'hpai_geno_db',
                              '-title', 'hpai_geno_db'], input_data=bytes(reference_data), cwd=work)
                blast_hpai_genotyping = Blast_Fasta(
                    FASTA=query,
                    format="6 qseqid qseq length nident pident mismatch evalue bitscore sacc stitle",
                    num_alignment=1, blast_db='hpai_geno_db', num_threads=2,
                    working_dir=work)
            finally:
                if self.debug:
                    debug_dir = tempfile.mkdtemp(prefix='genoflu_debug_', dir=os.getcwd())
                    shutil.copytree(work, debug_dir, dirs_exist_ok=True)
                    print(f'Debug files: {debug_dir}')

        blast_genotyping_by_virus = {virus_id: {} for virus_id in self.input_viruses}

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

            if virus_id not in blast_genotyping_by_virus:
                raise SystemExit(f'Error: BLAST returned an unknown virus ID: {virus_id}')

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
                total_in_sample = self.input_viruses[virus_id]
                if not gene_map:
                    result['genotype'] = 'Not assigned: No BLAST hits'
                elif segcnt == 8:
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
        -c is the genotype definitions workbook (.xlsx). Default: dependencies/genotype_key_asia.xlsx beside this script
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
                        help='Genotype definitions Excel file (.xlsx). Default: dependencies/genotype_key_asia.xlsx beside this script. Columns: Genotype + 8 segments.')
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
    # Validate the whole batch before starting BLAST or writing a workbook.
    inventories = [inspect_fasta(os.path.abspath(path)) for path in args.FASTA]
    for input_fasta, inventory in zip(args.FASTA, inventories):
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
            debug=args.debug, input_inventory=inventory
        )

        genoflu.blast_hpai_genomes()
        rows = genoflu.excel_rows()
        if set(genoflu.results_per_virus) != set(genoflu.input_viruses) or len(rows) != len(genoflu.input_viruses):
            raise SystemExit(f'Error: input/output virus count mismatch for {input_fasta}; no workbook saved.')
        all_rows.extend(rows)
        no_hits = sum(result['genotype'] == 'Not assigned: No BLAST hits'
                      for result in genoflu.results_per_virus.values())
        print(f'File: {input_fasta} | sequences: {genoflu.fastas_in_file} | '
              f'input viruses: {len(genoflu.input_viruses)} | output rows: {len(rows)} | no BLAST hits: {no_hits}')
        if no_hits:
            print(f'Warning: {input_fasta}: {no_hits} virus(es) have no BLAST hits; retained as unassigned.', file=sys.stderr)

        # Print genotype assignments.
        for virus_id, result in genoflu.results_per_virus.items():
            used = ', '.join(genoflu.genotype_list_used_per_virus.get(virus_id, []))
            print(f'\n{genoflu.sample_name}__{virus_id} Genotype --> {result["genotype"]}: {used}\n')

    output_file = excel_stats.write_all_results_rows(all_rows)
    print(f"Results: {output_file}")

# Created 2023 by Tod Stuber
# GenoFLU-Asia adaptation: multi-virus input and combined workbook output.
