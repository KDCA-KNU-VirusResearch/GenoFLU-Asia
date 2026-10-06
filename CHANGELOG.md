# Update history

## Reference database update — 2026-10-06

- Replaced the eight reference FASTA files and `genotype_key_asia.xlsx` with the supplied October 2026 dataset.
- The supplied database contains 126 genotype definitions and 562 reference sequences. All segment-group identifiers match between the workbook and FASTA files.
- All 10 bundled example viruses were assigned successfully. The expected name `NA.1(B3.2)` is now `22NA.1(B3.2)`, as supplied in the updated workbook.
- Software version remains v1.0; this is a reference database update.

## v1.0 — Current version

Current documentation baseline for GenoFLU-Asia and its bundled reference database.

- Genotype names and eight-segment combinations are provided in `dependencies/genotype_key_asia.xlsx`.
- Reference sequences and genotype definitions will be updated as additional viruses are reported.
- A minor genotype becomes major when its cumulative number of viruses reaches three or more, including detections in subsequent years.
- (Viruses reported later may receive later genotype numbers even if their collection dates are earlier.)

## Future genotype update documents

Each genotype update will include a version and release date, a summary of reference changes, and a record of renamed or reclassified genotypes. For minor-to-major changes, the document will list the previous minor name, the new major name, the reason for the change, and the affected eight-segment combination. This will allow users to relate results produced with different database versions.

No minor-to-major conversion list is published in this baseline; mappings will be provided with the corresponding updates.
