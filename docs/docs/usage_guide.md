## Installation

These instructions describe **GenoFLU-Asia** and its local scripts and reference files. They follow the installation–usage–interpretation structure of the [original GenoFLU documentation](https://github.com/USDA-VS/GenoFLU), with commands checked against this adaptation. Installing the upstream `genoflu` Conda package alone does not install the Asia-specific scripts, references, or genotype key.

### 1. Prepare a Linux environment

Use Linux or an Ubuntu terminal under Windows Subsystem for Linux (WSL). Run all commands below in that terminal. Use Conda installed through Miniforge or Miniconda; WSL users need Conda available **inside Ubuntu**.

### 2. Obtain the GenoFLU-Asia project files


```bash
mkdir -p "$HOME/projects"
git clone https://github.com/KDCA-KNU-VirusResearch/GenoFLU-Asia.git "$HOME/projects/GenoFLU-Asia"
cd "$HOME/projects/GenoFLU-Asia"
```

For a new installation, use `$HOME/projects/GenoFLU-Asia` for the examples below, or use its actual location. Download the files together and retain this structure:

```text
GenoFLU-Asia/
├── README.md
├── install_command.sh
├── run_genoflu.sh
├── genoflu.py
├── docs/
└── dependencies/
    ├── asia_fastas/
    │   └── *.fasta
    └── genotype_key_asia.xlsx
```

The shell script finds `genoflu.py` and the references relative to its own folder. The project folder and the Conda environment are separate: the project download does not need to contain Conda directories such as `bin/` or `lib/`.

### 3. Install dependencies

Create a dedicated environment once:

```bash
conda create -n genoflu-asia --override-channels -c conda-forge -c bioconda \
  python=3.13 pandas=2.3.2 openpyxl=3.1.5 blast=2.17.0
conda activate genoflu-asia
```

If this environment already exists and has the required dependencies, activate it rather than creating it again. The specified package versions reflect the current local setup (Python 3.13.7); this installation recipe still requires clean-environment validation before release.

Check that the activated environment supplies the required programs and Python modules:

```bash
python --version
python -c "import pandas, Bio, openpyxl; print('Python dependencies available')"
blastn -version
makeblastdb -version
```

### 4. Register the command

Activate the environment and run the installer from the project folder once:

```bash
conda activate genoflu-asia
cd "$HOME/projects/GenoFLU-Asia"
bash install_command.sh
genoflu-asia --help
```

The installer registers `genoflu-asia` in the active environment and connects it to this project's `run_genoflu.sh`. Keep the project at this location; if it is moved, re-register the command after preserving or removing the old launcher. The installer refuses to overwrite an existing command.

## Prepare input files

Use ~/genoflu_asia_analysis/input and ~/genoflu_asia_analysis/output for every analysis. This analysis folder is separate from ~/projects/GenoFLU-Asia. Move old input FASTA files aside before adding a new set to avoid analyzing them again.

### 1. Create input and output folders

```bash
mkdir -p "$HOME/genoflu_asia_analysis/input" "$HOME/genoflu_asia_analysis/output"
```

Copy the assembled nucleotide FASTA files you want to analyze into `~/genoflu_asia_analysis/input`. One file can contain one virus or multiple viruses. A complete genotype assignment requires accepted matches for all eight segments: **PB2, PB1, PA, HA, NP, NA, MP, and NS**.

```text
genoflu_asia_analysis/input/
├── sample01.fasta
├── sample02.fasta
└── samples_combined.fasta
```

Use lowercase `.fasta` extensions. The batch script reads files directly inside this folder; subfolders and `.fa`, `.fna`, or `.FASTA` files are not included. This adaptation accepts assembled **FASTA**, not raw FASTQ reads.

On Linux/WSL, program, input, reference, and output paths may contain spaces, parentheses, or Korean characters. Quote paths containing spaces in terminal commands. BLAST runs in an isolated temporary directory. If `makeblastdb` or `blastn` fails, execution stops with the tool name, exit code, and diagnostic message; no final workbook is written. With `-d`, temporary files are retained in a uniquely named `genoflu_debug_*` directory.

### 2. Check the FASTA headers

The text **before the first `|`** identifies the virus. All segments belonging to the same virus must have the same ID, with no spaces in that ID. Distinct viruses must have distinct IDs.

The following are **header examples only**, using a fictitious isolate name:

```text
>A/duck/Example/001/2023|PB2
>A/duck/Example/001/2023|PB1
>A/duck/Example/001/2023|PA
>A/duck/Example/001/2023|HA
>A/duck/Example/001/2023|NP
>A/duck/Example/001/2023|NA
>A/duck/Example/001/2023|MP
>A/duck/Example/001/2023|NS
```

Each header in an actual FASTA file must be followed by the corresponding nucleotide sequence. Labels after `|` are descriptive; the program determines the segment from the reference match. Review sequence completeness and ambiguous bases before interpreting an assignment. Read depth cannot be assessed from the FASTA file alone.

## Run GenoFLU-Asia

### Run from the analysis folder

```bash
conda activate genoflu-asia
cd ~/genoflu_asia_analysis
genoflu-asia --input ./input --output ./output
```

The input folder must already contain lowercase `.fasta` files. **Relative paths are resolved from the directory where you invoke the command.** The output folder is created if needed. The final workbook is `./output/genoflu_results_DATE_TIME_ID.xlsx`, with results in **All Results**.

To use the folders created in the previous section:

```bash
genoflu-asia --input "$HOME/genoflu_asia_analysis/input" --output "$HOME/genoflu_asia_analysis/output"
```

| Option | Meaning |
| --- | --- |
| `--input DIR`, `-i DIR` | Input FASTA folder; default `$HOME/genoflu_fasta`. |
| `--output DIR`, `-o DIR` | Output folder; default `$HOME/genoflu_output`. |
| `--help`, `-h` | Show usage without running an analysis. |

The no-argument command `genoflu-asia` uses the defaults above. You can override either or both paths without editing the script. Missing input folders, empty input folders, and unsupported options produce an error.

### Run the shell script directly

The original entry point remains available from the project folder:

```bash
conda activate genoflu-asia
cd "$HOME/projects/GenoFLU-Asia"
chmod +x run_genoflu.sh
./run_genoflu.sh --input "$HOME/genoflu_asia_analysis/input" --output "$HOME/genoflu_asia_analysis/output"
```

`./run_genoflu.sh` without arguments uses the same defaults. Confirm that all expected virus IDs are represented in the workbook; a completion message does not guarantee that every virus received a genotype.

### Optional: analyze a single FASTA directly

From the project folder, use both Asia-specific reference arguments:

```bash
python genoflu.py \
  -f "$HOME/genoflu_asia_analysis/input/sample01.fasta" \
  -i dependencies/asia_fastas \
  -c dependencies/genotype_key_asia.xlsx
```

This creates a new timestamped workbook in the **current working directory**, or in the directory supplied with `--output`. Reference defaults resolve beside the Python script to the bundled Asia references. Use `python genoflu.py --help` to inspect available options.

### Repeated runs

BLAST intermediate files are created in an isolated scratch directory; the workbook is written to the output directory. The project folder needs to be writable only when retaining debug files with `-d`.

Each invocation creates a new timestamped workbook with a unique suffix. Earlier workbooks are neither read nor overwritten. All input files in a batch are combined into one new workbook only after they finish successfully.

## Understand the results

### How a genotype is assigned

BLASTn compares each query with the reference sequences. When multiple query sequences represent the same virus/segment, the program selects a hit by percent identity, then bit score, then alignment length. A segment assignment is retained when its BLAST nucleotide identity is **≥97%**. The accepted eight-segment combination must exactly match a row in `genotype_key_asia.xlsx` to receive that row's genotype name.

The 97% threshold applies to the reported local alignment, not necessarily the entire segment. The current implementation has no additional minimum alignment-coverage filter and no command-line option to change this threshold.

### Read an output row

1. Identify the virus using `sample` and `File Name`.
2. Read `Genotype` for the assignment or the reason it was not assigned.
3. Inspect `Genotype List Used, >=97%` for the accepted segment groups.
4. Compare reference titles with the percent-match and mismatch lists to assess each reported hit.

| Column | How to interpret it |
| --- | --- |
| `sample` | Full input filename stem (without the final extension) plus `__` and the virus ID. |
| `date` | Analysis timestamp; this is not the collection date. |
| `File Name` | Source FASTA filename. |
| `Genotype` | A name from the current key, such as `AS-d.1` or `minor34`, or an unassigned-result message. |
| `Genotype List Used, >=97%` | Accepted `segment:group` assignments used to match the genotype key. |
| `Genotype Sample Title List` | Selected reference hits, formatted as `segment:group:reference_sample`. This may include hits below 97%. |
| `Genotype Percent Match List` | BLAST percent identities, in the same order as the reference-title list. |
| `Genotype Mismatch List` | Numbers of mismatching bases within the corresponding BLAST alignments, in the same order as the reference-title list. These are counts, not genotype numbers or percentages. |
| `Genotype Average Depth of Coverage List` | `Ran on FASTA - No Coverage Report`: read depth is unavailable for this FASTA workflow. |

**Do not assume a fixed segment order for the lists.** Read the gene label in `Genotype Sample Title List` and match the corresponding position in the identity and mismatch lists. The accepted-segment list can be shorter because it excludes hits below the threshold.

For example, a mismatch value of `40` means 40 mismatching bases in that selected alignment. A value of `0` means no mismatches in the aligned region; it does not establish an identical full-length segment, and gaps are treated separately. Percent identities are displayed to two decimal places, whereas the threshold comparison uses the underlying BLAST value.

### Assigned and unassigned genotypes

| Result | Meaning | What to check next |
| --- | --- | --- |
| A genotype name, e.g. `AS-d.1` | Eight accepted segment groups match a genotype-key entry. | Review sequence quality and individual reference matches; the label is not a confidence score or a measure of disease severity. |
| A `minor` name, e.g. `minor34` | A defined genotype-key entry whose name contains `minor`. | Treat it as an assigned genotype; `minor` does not mean a failed analysis or low-confidence sequence. |
| `Not assigned: No Matching Genotypes` | Eight segments pass the identity threshold, but their combination is absent from the key. | Check the segment combination, sequence quality, and current key. This result alone does not establish a novel genotype. |
| `Not assigned: Only ... segments >=97% ...` | Fewer than eight segment assignments pass the threshold. The threshold is **≥97%**. | Identify missing or below-threshold segments and verify the FASTA IDs and completeness. |
| An input virus is absent from the workbook | No reportable BLAST-hit group may have been generated for it. | Compare input IDs with reported IDs; check the input format, reference files, and BLAST availability. |

Genotype labels describe the study's reference-based classification. They do not independently establish HA clade membership, transmission direction, a phylogenetic relationship, or equivalence to another study's genotype nomenclature.

## Troubleshooting

| Problem | Action |
| --- | --- |
| `ModuleNotFoundError: No module named 'pandas'`, `Bio`, or `openpyxl` | Activate `genoflu-asia` and repeat the dependency checks. Install any missing package into that environment, not automatically into `base`. |
| `blastn` or `makeblastdb` is unavailable | Activate the environment containing BLAST+; verify both commands with `-version`. |
| The script ends without processing files | Check the `--input` folder, confirm it contains files directly inside it, and use lowercase `.fasta` extensions. |
| `genoflu-asia: command not found` | Activate `genoflu-asia` and run `bash install_command.sh` from the project folder if the command is not yet registered. |
| Reference FASTA or genotype key cannot be found | Restore the documented folder structure. For direct Python execution, provide `-i` and `-c`. |
| All or many samples are unassigned | Check BLAST availability, reference/key consistency, FASTA header grouping, and the per-segment identities. Do not infer a new genotype from a failed run. |
| Results contain repeated rows or earlier samples | Check for a workbook left in the project folder from an interrupted or direct run. Preserve it separately before rerunning. |
| `Permission denied` when using `./run_genoflu.sh` | Run `chmod +x run_genoflu.sh` and retry `./run_genoflu.sh`; also ensure that the project and output folders are writable. |
| `blastn failed` or `makeblastdb failed` | Read the diagnostic below the error, correct the reported cause, and rerun. No final workbook is saved for a failed run. |



### Input validation and reporting

- Empty or malformed FASTA files stop the entire batch before BLAST starts. The error identifies the file and cause; no new workbook is saved.
- Sequence IDs must be unique within each file. Nucleotide sequences may contain IUPAC ambiguity codes and gap hyphens; empty sequences and invalid characters are rejected.
- Every input virus is retained in the output. `Not assigned: No BLAST hits` means no reference alignment was returned for that virus.
- The terminal reports sequence count, input virus count, output row count, and no-hit virus count for each file.
- `sample` uses the full input filename stem followed by `__` and the virus ID, so `batch_alpha.fasta` and `batch_beta.fasta` remain distinct.

### Environment and temporary storage

- `environment.yml` contains the Conda dependencies: from the project folder, use `conda env create -f environment.yml` as an alternative to the installation command above.
- `requirements.txt` lists Python packages only; BLAST+ must be installed separately. Biopython is no longer required.
- BLAST scratch storage uses `GENOFLU_TMPDIR`, then `TMPDIR`, then the operating system default. Choose an existing writable directory with enough space.
- BLAST requires a simple scratch path containing only ASCII letters, numbers, `_`, `-`, `/`, and `.`. If your `TMPDIR` contains spaces, set a suitable path with `export GENOFLU_TMPDIR=/path/to/scratch`. Input, reference, project, and output paths may still contain spaces or Korean characters.
- Linux/WSL remain the supported platforms; macOS has not been fully validated.

