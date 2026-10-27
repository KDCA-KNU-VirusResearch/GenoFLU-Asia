# GenoFLU-Asia

[Documentation website](https://kdca-knu-virusresearch.github.io/GenoFLU-Asia/) · [GitHub repository](https://github.com/KDCA-KNU-VirusResearch/GenoFLU-Asia)

Reference-based genotype assignment for Asian H5 avian influenza viruses in clade 2.3.4.4b, group G2.

## Overview

GenoFLU-Asia is a genotyping tool designed to support the standardized classification of clade 2.3.4.4b H5 avian influenza viruses circulating in Asia. These viruses exhibit highly diverse genomic constellations that differ substantially from those circulating in other regions. Consequently, existing genotyping tools, such as GenoFLU and Genin2, may not adequately classify many Asian viruses. Differences in genotype nomenclature among countries and institutions further complicate comparisons, highlighting the need for a harmonized genotyping framework for Asia.

GenoFLU-Asia was developed based on the USDA-VS/GenoFLU program through a collaboration between the Korea Disease Control and Prevention Agency (KDCA) and Kyungpook National University, Republic of Korea. The tool automatically assigns genotypes to clade 2.3.4.4b H5 avian influenza viruses detected in Asia since 2021 using a newly established genotype nomenclature system.

GenoFLU-Asia uses BLAST-based sequence comparisons to assign each genomic segment to a segment group and determines the viral genotype based on the resulting eight-segment constellation. The tool supports batch analysis of multiple viruses provided in FASTA format and compiles all assignment results into a single Excel workbook. It thereby provides a consistent and efficient approach to genotype assignment and genomic surveillance of clade 2.3.4.4b H5 viruses across Asia.

Current version: v1.0. The reference sequences and genotype definitions require regular updates as additional viruses are reported. Future updates will document changes to genotype names and minor-to-major reclassifications. See [Update history](CHANGELOG.md).

## Genotype classification and nomenclature

Major and minor designations reflect the number of viruses representing each genotype in the study dataset.

- **Major:** Three or more viruses; names encode the HA subgroup.
- **Minor:** Fewer than three viruses; numbered in order of emergence without an HA subgroup label.
- **Example — AS-a.1:** AS denotes Asia, a denotes the HA subgroup, and 1 identifies the first genotype to emerge within that HA subgroup.
- **Reassortment numbering:** Subsequent reassortants receive suffixes such as .1 and .2 (for example, AS-a.1.1 and AS-a.1.2). A genotype differing from genotype 1 in five or more of the eight genome segments receives a new main number, such as AS-a.2. (Viruses reported later may receive later genotype numbers even if their collection dates are earlier; numbering therefore does not always follow collection-date order.)
- **Minor-to-major updates:** A minor genotype is reclassified as major when additional detections, including those in subsequent years, bring the cumulative number of viruses to three or more. These changes are made during reference database updates, not automatically from the number of samples in an individual analysis.
- **Genotype definitions:** The file `genotype_key_asia.xlsx` records genotype names and their corresponding eight-segment combinations.

![Major and minor genotype nomenclature](docs/docs/genotype_nomenclature.png?v=2)

**Genotype nomenclature.** Naming scheme for major and minor genotypes.

## Comparison with published genotype designations

Correspondence between GenoFLU-Asia genotypes and previously reported designations.

[Search and filter on the website](https://kdca-knu-virusresearch.github.io/GenoFLU-Asia/comparison.html)

<details>
<summary>View the full genotype comparison table (65 genotypes)</summary>

| GenoFLU-Asia | Previously reported designation | Reference |
| --- | --- | --- |
| AS-a.1(N6) | G3 | [Gu Wenli et al., 2022](https://doi.org/10.1080/22221751.2022.2063076)<br>Gu Wenli et al. (2022). Novel H5N6 reassortants bearing the clade 2.3.4.4b HA gene of H5N8 virus have been detected in poultry and caused multiple human infections in China. Emerging Microbes &amp; Infections. |
| AS-a.2(N6) | G01 | [Yang Kang et al., 2025](https://doi.org/10.1128/jvi.01145-24)<br>Yang Kang et al. (2025). Genetic diversity of highly pathogenic avian influenza H5N6 and H5N8 viruses in poultry markets in Guangdong, China, 2020-2022. Journal of Virology. |
| AS-a.3(N6) | G04 | [Yang Kang et al., 2025](https://doi.org/10.1128/jvi.01145-24)<br>Yang Kang et al. (2025). Genetic diversity of highly pathogenic avian influenza H5N6 and H5N8 viruses in poultry markets in Guangdong, China, 2020-2022. Journal of Virology. |
| AS-a.3(N6) | G7 | [Gu Wenli et al., 2022](https://doi.org/10.1080/22221751.2022.2063076)<br>Gu Wenli et al. (2022). Novel H5N6 reassortants bearing the clade 2.3.4.4b HA gene of H5N8 virus have been detected in poultry and caused multiple human infections in China. Emerging Microbes &amp; Infections. |
| AS-a.3.1 | G9 | [Cui Pengfei et al., 2022](https://doi.org/10.1080/22221751.2022.2088407)<br>Cui Pengfei et al. (2022). Global dissemination of H5N1 influenza viruses bearing the clade 2.3.4.4b HA gene and biologic analysis of the ones detected in China. Emerging Microbes &amp; Infections. |
| AS-a.3.2(N6) | G07 | [Yang Kang et al., 2025](https://doi.org/10.1128/jvi.01145-24)<br>Yang Kang et al. (2025). Genetic diversity of highly pathogenic avian influenza H5N6 and H5N8 viruses in poultry markets in Guangdong, China, 2020-2022. Journal of Virology. |
| AS-a.3.2(N6) | N6.1 | [Zhang Xinkui et al., 2025](https://doi.org/10.1080/22221751.2025.2502005)<br>Zhang Xinkui et al. (2025). Unique phenomenon of H5 highly pathogenic avian influenza virus in China: co-circulation of Clade 2.3.4.4b H5N1 and H5N6 results in diversity of H5 Virus. Emerging Microbes &amp; Infections. |
| AS-a.4(N6) | G6 | [Gu Wenli et al., 2022](https://doi.org/10.1080/22221751.2022.2063076)<br>Gu Wenli et al. (2022). Novel H5N6 reassortants bearing the clade 2.3.4.4b HA gene of H5N8 virus have been detected in poultry and caused multiple human infections in China. Emerging Microbes &amp; Infections. |
| AS-b.1 | G2b-1 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-b.1 | V | [Hew Lim Yik et al., 2024](https://doi.org/10.1155/2024/1199876)<br>Hew Lim Yik et al. (2024). Continuous Introduction of H5 High Pathogenicity Avian Influenza Viruses in Hokkaido, Japan: Characterization of Viruses Isolated in Winter 2022–2023 and Early Winter 2023–2024. Transboundary and Emerging Diseases. |
| AS-b.1 | G7 | [Cui Pengfei et al., 2022](https://doi.org/10.1080/22221751.2022.2088407)<br>Cui Pengfei et al. (2022). Global dissemination of H5N1 influenza viruses bearing the clade 2.3.4.4b HA gene and biologic analysis of the ones detected in China. Emerging Microbes &amp; Infections. |
| AS-b.1 | I | [Cha Ra Mi et al., 2023](https://doi.org/10.3390/v15061403)<br>Cha Ra Mi et al. (2023). Genetic Characterization and Pathogenesis of H5N1 High Pathogenicity Avian Influenza Virus Isolated in South Korea during 2021–2022. Viruses. |
| AS-b.1.1 | III | [Cha Ra Mi et al., 2023](https://doi.org/10.3390/v15061403)<br>Cha Ra Mi et al. (2023). Genetic Characterization and Pathogenesis of H5N1 High Pathogenicity Avian Influenza Virus Isolated in South Korea during 2021–2022. Viruses. |
| AS-b.1.3 | II | [Cha Ra Mi et al., 2023](https://doi.org/10.3390/v15061403)<br>Cha Ra Mi et al. (2023). Genetic Characterization and Pathogenesis of H5N1 High Pathogenicity Avian Influenza Virus Isolated in South Korea during 2021–2022. Viruses. |
| AS-c.1 | BD-G1 | [Barman Subrata et al., 2024](https://doi.org/10.1080/22221751.2024.2432351)<br>Barman Subrata et al. (2024). Reassortment of newly emergent clade 2.3.4.4b A(H5N1) highly pathogenic avian influenza A viruses in Bangladesh. Emerging Microbes &amp; Infections. |
| AS-c.1.2 | G2c-2 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.1.2 | N1.2 | [Zhang Xinkui et al., 2025](https://doi.org/10.1080/22221751.2025.2502005)<br>Zhang Xinkui et al. (2025). Unique phenomenon of H5 highly pathogenic avian influenza virus in China: co-circulation of Clade 2.3.4.4b H5N1 and H5N6 results in diversity of H5 Virus. Emerging Microbes &amp; Infections. |
| AS-c.1.2 | G10 | [Cui Pengfei et al., 2022](https://doi.org/10.1080/22221751.2022.2088407)<br>Cui Pengfei et al. (2022). Global dissemination of H5N1 influenza viruses bearing the clade 2.3.4.4b HA gene and biologic analysis of the ones detected in China. Emerging Microbes &amp; Infections. |
| AS-c.1.2 | IV | [Cha Ra Mi et al., 2023](https://doi.org/10.3390/v15061403)<br>Cha Ra Mi et al. (2023). Genetic Characterization and Pathogenesis of H5N1 High Pathogenicity Avian Influenza Virus Isolated in South Korea during 2021–2022. Viruses. |
| AS-c.1.2 | 22G1 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-c.1.2.1 | G2c-10 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.1.2.1 | Kor22-23E | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| AS-c.1.2.1 | 22G3 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-c.2 | BD-G2 | [Barman Subrata et al., 2024](https://doi.org/10.1080/22221751.2024.2432351)<br>Barman Subrata et al. (2024). Reassortment of newly emergent clade 2.3.4.4b A(H5N1) highly pathogenic avian influenza A viruses in Bangladesh. Emerging Microbes &amp; Infections. |
| AS-c.2 | N1.1 | [Zhang Xinkui et al., 2025](https://doi.org/10.1080/22221751.2025.2502005)<br>Zhang Xinkui et al. (2025). Unique phenomenon of H5 highly pathogenic avian influenza virus in China: co-circulation of Clade 2.3.4.4b H5N1 and H5N6 results in diversity of H5 Virus. Emerging Microbes &amp; Infections. |
| AS-c.2 | G2c-7 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.2 | G2c-8 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.2 | VI | [Hew Lim Yik et al., 2024](https://doi.org/10.1155/2024/1199876)<br>Hew Lim Yik et al. (2024). Continuous Introduction of H5 High Pathogenicity Avian Influenza Viruses in Hokkaido, Japan: Characterization of Viruses Isolated in Winter 2022–2023 and Early Winter 2023–2024. Transboundary and Emerging Diseases. |
| AS-c.2 | South Korean genotype III | [Lee Kyungmoon et al., 2024](https://doi.org/10.1080/22221751.2023.2290835)<br>Lee Kyungmoon et al. (2024). Characterization of highly pathogenic avian influenza A (H5N1) viruses isolated from cats in South Korea, 2023. Emerging Microbes &amp; Infections. |
| AS-c.2 | Kor22-23D | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| AS-c.2 | 22G7 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-c.2.1 | G2c-6 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.2.1 | 22G6 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-c.2.1.1 | G2c-3 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.2.1.1 | Kor22-23K | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| AS-c.2.1.1 | 22G5 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-c.2.1.1.1 | G2c-11 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.2.1.1.1 | Kor22-23C | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| AS-c.2.1.1.1 | 22G8 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-c.2.1.1.2 | G2c-1 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.2.1.1.2 | 22G11 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-c.2.1.1.3 | G2c-4 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.2.1.1.3.1 | G2c-9 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-c.2.1.1.3.1 | Kor22-23J | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| AS-c.2.1.1.4 | Kor22-23O | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| AS-c.2.2 | BD-G4 | [Barman Subrata et al., 2024](https://doi.org/10.1080/22221751.2024.2432351)<br>Barman Subrata et al. (2024). Reassortment of newly emergent clade 2.3.4.4b A(H5N1) highly pathogenic avian influenza A viruses in Bangladesh. Emerging Microbes &amp; Infections. |
| AS-c.3 | 22G4 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-c.3.1 | G2c-13 | [Takadate Yoshihiro et al., 2026](https://doi.org/10.1128/spectrum.00293-26)<br>Takadate Yoshihiro et al. (2026). High pathogenicity avian influenza A (H5N1) viruses isolated from poultry and wild birds in Japan during the 2024–2025 season. Microbiology Spectrum. |
| AS-c.3.1 | Genotype 2 | [Si Young-Jae et al., 2025](https://doi.org/10.3389/fvets.2025.1638067)<br>Si Young-Jae et al. (2025). First detection of clade 2.3.4.4b H5N1 highly pathogenic avian influenza virus in a wild leopard cat (Prionailurus bengalensis) in South Korea. Frontiers in Veterinary Science. |
| AS-c.3.1.1 | G2c-17 | [Takadate Yoshihiro et al., 2026](https://doi.org/10.1128/spectrum.00293-26)<br>Takadate Yoshihiro et al. (2026). High pathogenicity avian influenza A (H5N1) viruses isolated from poultry and wild birds in Japan during the 2024–2025 season. Microbiology Spectrum. |
| AS-c.4 | G2c-12 | [Nishiura Hayate et al., 2024](https://doi.org/10.3390/v16121956)<br>Nishiura Hayate et al. (2024). Phylogenetic and Pathogenic Analysis of H5N1 and H5N6 High Pathogenicity Avian Influenza Virus Isolated from Poultry Farms (Layer and Broiler Chickens) in Japan in the 2023/2024 Season. Viruses. |
| AS-c.4 | 23G2 | [Cha Ra Mi et al., 2026](https://doi.org/10.1155/tbed/8053623)<br>Cha Ra Mi et al. (2026). Emergence and Genetic Characteristics of H5N1, H5N6, and H5N3 Clade 2.3.4.4b High Pathogenicity Avian Influenza Viruses in South Korea During the 2023–2024 and 2024–2025 Winter Seasons. Transboundary and Emerging Diseases. |
| AS-d.1 | G2d-0 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-d.1 | I | [Hew Lim Yik et al., 2024](https://doi.org/10.1155/2024/1199876)<br>Hew Lim Yik et al. (2024). Continuous Introduction of H5 High Pathogenicity Avian Influenza Viruses in Hokkaido, Japan: Characterization of Viruses Isolated in Winter 2022–2023 and Early Winter 2023–2024. Transboundary and Emerging Diseases. |
| AS-d.1 | G1 | [Cui Pengfei et al., 2022](https://doi.org/10.1080/22221751.2022.2088407)<br>Cui Pengfei et al. (2022). Global dissemination of H5N1 influenza viruses bearing the clade 2.3.4.4b HA gene and biologic analysis of the ones detected in China. Emerging Microbes &amp; Infections. |
| AS-d.1 | 22G0 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| AS-d.1.1 | G2d-1 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-d.1.1 | II | [Hew Lim Yik et al., 2024](https://doi.org/10.1155/2024/1199876)<br>Hew Lim Yik et al. (2024). Continuous Introduction of H5 High Pathogenicity Avian Influenza Viruses in Hokkaido, Japan: Characterization of Viruses Isolated in Winter 2022–2023 and Early Winter 2023–2024. Transboundary and Emerging Diseases. |
| AS-d.1.2(N2) | G2d-2 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| AS-d.1.2(N2) | III | [Hew Lim Yik et al., 2024](https://doi.org/10.1155/2024/1199876)<br>Hew Lim Yik et al. (2024). Continuous Introduction of H5 High Pathogenicity Avian Influenza Viruses in Hokkaido, Japan: Characterization of Viruses Isolated in Winter 2022–2023 and Early Winter 2023–2024. Transboundary and Emerging Diseases. |
| AS-d.1.3 | IV | [Hew Lim Yik et al., 2024](https://doi.org/10.1155/2024/1199876)<br>Hew Lim Yik et al. (2024). Continuous Introduction of H5 High Pathogenicity Avian Influenza Viruses in Hokkaido, Japan: Characterization of Viruses Isolated in Winter 2022–2023 and Early Winter 2023–2024. Transboundary and Emerging Diseases. |
| NA.1(B3.2) | 22G2 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| minor1(N6) | G2 | [Gu Wenli et al., 2022](https://doi.org/10.1080/22221751.2022.2063076)<br>Gu Wenli et al. (2022). Novel H5N6 reassortants bearing the clade 2.3.4.4b HA gene of H5N8 virus have been detected in poultry and caused multiple human infections in China. Emerging Microbes &amp; Infections. |
| minor10(N6) | G5 | [Gu Wenli et al., 2022](https://doi.org/10.1080/22221751.2022.2063076)<br>Gu Wenli et al. (2022). Novel H5N6 reassortants bearing the clade 2.3.4.4b HA gene of H5N8 virus have been detected in poultry and caused multiple human infections in China. Emerging Microbes &amp; Infections. |
| minor11(N6) | G4 | [Gu Wenli et al., 2022](https://doi.org/10.1080/22221751.2022.2063076)<br>Gu Wenli et al. (2022). Novel H5N6 reassortants bearing the clade 2.3.4.4b HA gene of H5N8 virus have been detected in poultry and caused multiple human infections in China. Emerging Microbes &amp; Infections. |
| minor12(N6) | G6 | [Gu Wenli et al., 2022](https://doi.org/10.1080/22221751.2022.2063076)<br>Gu Wenli et al. (2022). Novel H5N6 reassortants bearing the clade 2.3.4.4b HA gene of H5N8 virus have been detected in poultry and caused multiple human infections in China. Emerging Microbes &amp; Infections. |
| minor14 | G7 | [Cui Pengfei et al., 2022](https://doi.org/10.1080/22221751.2022.2088407)<br>Cui Pengfei et al. (2022). Global dissemination of H5N1 influenza viruses bearing the clade 2.3.4.4b HA gene and biologic analysis of the ones detected in China. Emerging Microbes &amp; Infections. |
| minor15 | BD-G1 | [Barman Subrata et al., 2024](https://doi.org/10.1080/22221751.2024.2432351)<br>Barman Subrata et al. (2024). Reassortment of newly emergent clade 2.3.4.4b A(H5N1) highly pathogenic avian influenza A viruses in Bangladesh. Emerging Microbes &amp; Infections. |
| minor23 | G06 | [Yang Kang et al., 2025](https://doi.org/10.1128/jvi.01145-24)<br>Yang Kang et al. (2025). Genetic diversity of highly pathogenic avian influenza H5N6 and H5N8 viruses in poultry markets in Guangdong, China, 2020-2022. Journal of Virology. |
| minor27 | 22G9 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| minor30 | 22G10 | [Cha Ra Mi et al., 2025](https://doi.org/10.1016/j.virusres.2025.199541)<br>Cha Ra Mi et al. (2025). Genetic characteristics and pathogenesis of clade 2.3.4.4b H5N1 high pathogenicity avian influenza virus isolated from poultry in South Korea, 2022–2023. Virus Research. |
| minor31 | Kor22-23F | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor32 | Kor22-23B | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor33 | G2b-3 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| minor34 | G2c-5 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| minor35 | Kor22-23L | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor36 | Kor22-23C | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor38 | Kor22-23N | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor39 | Kor22-23P | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor39 | N1.3 | [Zhang Xinkui et al., 2025](https://doi.org/10.1080/22221751.2025.2502005)<br>Zhang Xinkui et al. (2025). Unique phenomenon of H5 highly pathogenic avian influenza virus in China: co-circulation of Clade 2.3.4.4b H5N1 and H5N6 results in diversity of H5 Virus. Emerging Microbes &amp; Infections. |
| minor4 | b.G5 | [Li X, Lv X, Li Y, et al., 2026](https://doi.org/10.1038/s41467-026-76039-9)<br>Li X, Lv X, Li Y, et al. (2026). Evolving dynamics of H5Nx avian influenza in China revealed by long-term wild bird surveillance. Nature Communications 17:9011. |
| minor41 | Kor22-23D | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor42 | Kor22-23B | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor43 | Kor22-23D | [Seo Ye-Ram et al., 2024](https://doi.org/10.3201/eid3002.231274)<br>Seo Ye-Ram et al. (2024). Evolution and Spread of Highly Pathogenic Avian Influenza A(H5N1) Clade 2.3.4.4b Virus in Wild Birds, South Korea, 2022–2023. Emerging Infectious Diseases. |
| minor44 | G2d-3 | [Takadate Yoshihiro et al., 2024](https://doi.org/10.1016/j.virusres.2024.199425)<br>Takadate Yoshihiro et al. (2024). Genetic diversity of H5N1 and H5N2 high pathogenicity avian influenza viruses isolated from poultry in Japan during the winter of 2022–2023. Virus Research. |
| minor48 | BD-G3 | [Barman Subrata et al., 2024](https://doi.org/10.1080/22221751.2024.2432351)<br>Barman Subrata et al. (2024). Reassortment of newly emergent clade 2.3.4.4b A(H5N1) highly pathogenic avian influenza A viruses in Bangladesh. Emerging Microbes &amp; Infections. |
| minor6(N6) | G01 | [Yang Kang et al., 2025](https://doi.org/10.1128/jvi.01145-24)<br>Yang Kang et al. (2025). Genetic diversity of highly pathogenic avian influenza H5N6 and H5N8 viruses in poultry markets in Guangdong, China, 2020-2022. Journal of Virology. |
| minor64(N6) | N6.3 | [Zhang Xinkui et al., 2025](https://doi.org/10.1080/22221751.2025.2502005)<br>Zhang Xinkui et al. (2025). Unique phenomenon of H5 highly pathogenic avian influenza virus in China: co-circulation of Clade 2.3.4.4b H5N1 and H5N6 results in diversity of H5 Virus. Emerging Microbes &amp; Infections. |
| minor24 | H5N1-III | [Esaki Mana et al., 2025](https://doi.org/10.3201/eid3105.241410)<br>Esaki Mana et al. (2025). Highly Pathogenic Avian Influenza A(H5N1) Outbreak in Endangered Cranes, Izumi Plain, Japan, 2022–23. Emerging Infectious Diseases. |
| minor25 | H5N1-IV | [Esaki Mana et al., 2025](https://doi.org/10.3201/eid3105.241410)<br>Esaki Mana et al. (2025). Highly Pathogenic Avian Influenza A(H5N1) Outbreak in Endangered Cranes, Izumi Plain, Japan, 2022–23. Emerging Infectious Diseases. |
| minor26 | H5N1-VI | [Esaki Mana et al., 2025](https://doi.org/10.3201/eid3105.241410)<br>Esaki Mana et al. (2025). Highly Pathogenic Avian Influenza A(H5N1) Outbreak in Endangered Cranes, Izumi Plain, Japan, 2022–23. Emerging Infectious Diseases. |
| minor28 | H5N1-VIII | [Esaki Mana et al., 2025](https://doi.org/10.3201/eid3105.241410)<br>Esaki Mana et al. (2025). Highly Pathogenic Avian Influenza A(H5N1) Outbreak in Endangered Cranes, Izumi Plain, Japan, 2022–23. Emerging Infectious Diseases. |
| minor3(N6) | G1 | [Zhao Wanchen et al., 2023](https://doi.org/10.1080/21505594.2023.2250065)<br>Zhao Wanchen et al. (2023). Virulence and transmission characteristics of clade 2.3.4.4b H5N6 subtype avian influenza viruses possessing different internal gene constellations. Virulence. |
| minor67 | G2d-7 | [Takadate Yoshihiro et al., 2026](https://doi.org/10.1128/spectrum.00293-26)<br>Takadate Yoshihiro et al. (2026). High pathogenicity avian influenza A (H5N1) viruses isolated from poultry and wild birds in Japan during the 2024–2025 season. Microbiology Spectrum. |
| minor69 | G2c-15 | [Takadate Yoshihiro et al., 2026](https://doi.org/10.1128/spectrum.00293-26)<br>Takadate Yoshihiro et al. (2026). High pathogenicity avian influenza A (H5N1) viruses isolated from poultry and wild birds in Japan during the 2024–2025 season. Microbiology Spectrum. |
| minor70 | G2d-8 | [Takadate Yoshihiro et al., 2026](https://doi.org/10.1128/spectrum.00293-26)<br>Takadate Yoshihiro et al. (2026). High pathogenicity avian influenza A (H5N1) viruses isolated from poultry and wild birds in Japan during the 2024–2025 season. Microbiology Spectrum. |
| minor71 | G2c-15 | [Takadate Yoshihiro et al., 2026](https://doi.org/10.1128/spectrum.00293-26)<br>Takadate Yoshihiro et al. (2026). High pathogenicity avian influenza A (H5N1) viruses isolated from poultry and wild birds in Japan during the 2024–2025 season. Microbiology Spectrum. |
| minor72 | G2d-9 | [Takadate Yoshihiro et al., 2026](https://doi.org/10.1128/spectrum.00293-26)<br>Takadate Yoshihiro et al. (2026). High pathogenicity avian influenza A (H5N1) viruses isolated from poultry and wild birds in Japan during the 2024–2025 season. Microbiology Spectrum. |

</details>

## Installation

GenoFLU-Asia can be used in a Conda environment on Linux or Ubuntu on WSL. Install Conda through Miniforge or Miniconda.

- **Windows users:** open the Ubuntu terminal and run the commands there. Conda must be available inside Ubuntu; installing Conda only on Windows is not sufficient.
- **Command entry:** paste a command and press Enter. Do not copy a terminal prompt such as `(base) user@computer:~$`.
- **Already installed?** If your existing setup works, keep it and go to [Input and execution](#input-and-execution).

### Understand the folders

The project files, Conda environment, and analysis files serve different purposes.

| Item | Purpose | Example |
| --- | --- | --- |
| Project folder | Stores the scripts, reference sequences, and genotype definitions | `~/projects/GenoFLU-Asia` |
| Conda environment | Provides Python, BLAST, and required packages | Environment named `genoflu-asia` |
| Analysis folder | Stores input FASTA files and output workbooks | `~/genoflu_asia_analysis` |

- **Project location:** keep the project in a working folder; it does not need to be inside Conda's `envs` directory.
- **`~`:** your Linux home folder, for example `/home/user`.
- **`cd`:** changes your current folder. **`conda activate`:** selects an environment without changing folders.
- **Paths:** folder and file names may contain spaces, parentheses, or Korean characters on Linux/WSL. Enclose paths containing spaces in double quotes, for example `--input "/home/user/my data/input"`.

### 1. Clone the repository — once

Cloning downloads the complete project, including the scripts, reference sequences, and genotype definitions. First check that Git is available in your Linux or Ubuntu terminal:

```bash
git --version
```

If Ubuntu reports `git: command not found`, install Git, then continue:

```bash
sudo apt update
sudo apt install git
```

When prompted by `sudo`, enter your Ubuntu password; no characters appear while you type.


```bash
mkdir -p ~/projects
git clone https://github.com/KDCA-KNU-VirusResearch/GenoFLU-Asia.git ~/projects/GenoFLU-Asia
cd ~/projects/GenoFLU-Asia
ls
```

- **`mkdir -p`:** creates the parent folder if needed.
- **`git clone`:** downloads the repository into `~/projects/GenoFLU-Asia`.
- **`cd`:** moves into the downloaded project folder.
- **`ls`:** lists its contents; check for `genoflu.py`, `run_genoflu.sh`, `install_command.sh`, and `dependencies/`. Keep them together.
- **Existing copy:** if this folder already contains your project, skip cloning and enter it with `cd`.

### 2. Create the Conda environment — once

First check Conda and existing environments:

```bash
conda --version
conda env list
```

If `genoflu-asia` already exists with the required packages, skip the creation command. Otherwise, run this single-line command:

```bash
conda create -n genoflu-asia --override-channels -c conda-forge -c bioconda python=3.13 pandas=2.3.2 openpyxl=3.1.5 blast=2.17.0
```

- **`-n genoflu-asia`:** names the environment.
- **Packages:** Python runs the code; pandas and openpyxl handle tables and Excel files; BLAST compares sequences.
- **Confirmation:** if prompted with `Proceed ([y]/n)?`, review the installation list, enter `y`, and wait for installation to finish.
- **Validation:** the release files were tested in the existing Ubuntu 24.04 Conda environment with BLAST 2.17.0, pandas 2.3.2, Biopython 1.85, and openpyxl 3.1.5. A test input containing 14,432 sequences from 1,804 virus IDs produced 1,804 result rows, matching the existing code. Repeated execution and Asia reference defaults were also checked.

- **Input-accounting regression:** Current input-accounting regression tests retained all expected results in two repeated 20-row batches (two 10-genotype files per run), retained no-hit viruses, and rejected malformed input without producing a workbook. These checks used the existing Linux/WSL environment; a fresh Conda solve was not performed.

### 3. Activate the environment and register the command — once

Run the installer from the project folder after activating the environment:

```bash
conda activate genoflu-asia
cd ~/projects/GenoFLU-Asia
bash install_command.sh
genoflu-asia --help
```

- **Registration:** creates the `genoflu-asia` command in the activated environment, so you can run it from other folders.
- **Check:** `--help` displays usage instructions without starting an analysis; it does not test the full analysis workflow.
- **Already registered:** do not repeat registration. If `Command already exists` appears, first check `genoflu-asia --help`.
- **Project location:** keep the project at its registered location. The installer does not overwrite an existing command if you move the project.

## Input and execution

Use the same input and output folders for each analysis. The analysis folder, `~/genoflu_asia_analysis`, is separate from the program folder, `~/projects/GenoFLU-Asia`.

### Prepare folders

Create the analysis folder and its input/output folders once. No intermediate run folders are needed:

```bash
mkdir -p ~/genoflu_asia_analysis/input ~/genoflu_asia_analysis/output
cd ~/genoflu_asia_analysis
pwd
```

```text
~/genoflu_asia_analysis/
├── input/
│   ├── sample01.fasta
│   └── sample02.fasta
└── output/
```

- **`mkdir -p`:** creates folders if they do not exist. **`pwd`:** shows your current working directory.
- **Copy files:** place your assembled nucleotide FASTA files directly in `input`. On WSL, run `explorer.exe input` from `~/genoflu_asia_analysis` to open that folder in Windows File Explorer.
- **Files:** all lowercase `.fasta` files directly inside the input folder are analyzed; each may contain one or multiple viruses.
- **Extensions:** `.fa`, `.fna`, `.FASTA`, and `.fasta.txt` are not selected by the batch script. Renaming a spreadsheet to `.fasta` does not convert it into sequence data.

### Prepare FASTA headers

All segments of a virus must share the same ID before the first `|`.

- Use IDs without spaces and a distinct ID for each virus.
- Include all eight segments: **PB2, PB1, PA, HA, NP, NA, MP, and NS**.
- Follow each header with its corresponding nucleotide sequence.

### Input FASTA example

```text
>A/wild_duck/Korea/H503/2022|EPI_ISL_19453422|1
ATGGAGAGAATGAAAGAACTAAGAG...
>A/wild_duck/Korea/H503/2022|EPI_ISL_19453422|2
ATGGATGTCAATCCGACTTTACTTT...
>A/wild_duck/Korea/H503/2022|EPI_ISL_19453422|3
ATGATTGTCGAGCTTGCGGAAAAAGC...
```

Abbreviated example showing three sequence records from one virus. Each header starts with `>` on its own line, followed by the nucleotide sequence on the next line. The sequences above are excerpts; use the actual nucleotide sequences without ellipses (`...`) in the input file.


### Run

```bash
conda activate genoflu-asia
cd ~/genoflu_asia_analysis
genoflu-asia --input ./input --output ./output
```

- **`conda activate genoflu-asia`:** selects the required environment; repeat this in each new terminal session.
- **`--input ./input`:** reads the `input` folder inside your current directory, not a particular filename.
- **`--output ./output`:** saves results in the `output` folder inside your current directory.
- **Progress:** wait for `All files processed.` and check for errors. Run only one analysis at a time per project folder.

To avoid depending on your current folder, specify the paths explicitly:

```bash
genoflu-asia --input ~/genoflu_asia_analysis/input --output ~/genoflu_asia_analysis/output
```

### Open the results

Each run uses its start date/time and a unique suffix, for example `genoflu_results_20260916_153025_123456_a1b2c3d4.xlsx`. `DATE_TIME_ID` below represents those automatically generated values.

Open `~/genoflu_asia_analysis/output/genoflu_results_DATE_TIME_ID.xlsx` in Excel and select the **All Results** sheet. On WSL, open the output folder with:

```bash
explorer.exe ~/genoflu_asia_analysis/output
```

Confirm that all expected virus IDs appear, then use [Interpreting results](#interpreting-results) below to read the assignments.

### Run another analysis

Reuse the same folders; do not recreate the environment, register the command again, or create a new run folder.

1. Move any FASTA files you no longer want to analyze out of `input`, then copy the new files into it. Every `.fasta` file left in this folder will be analyzed.
2. Each run creates a new `genoflu_results_DATE_TIME_ID.xlsx` in `output`; previous results are retained automatically.
3. Activate the environment and run:

```bash
conda activate genoflu-asia
cd ~/genoflu_asia_analysis
genoflu-asia --input ./input --output ./output
```

- **Interrupted runs:** restart with the same command. Previous workbooks are never read or appended; a new workbook is saved only after all input files finish successfully.
- **Without command registration:** run `bash ~/projects/GenoFLU-Asia/run_genoflu.sh --input ~/genoflu_asia_analysis/input --output ~/genoflu_asia_analysis/output` with the environment activated.

## Test the installation

The `test/` folder contains `example_10_genotypes.fasta` (10 viruses, eight segments each) and `expected_results.tsv`. The example covers five distinct major and five distinct minor genotypes. Expected assignments were verified with the bundled Asia references and genotype definitions; they are software test results, not an independent biological validation.

Run the example using your activated environment:

```bash
conda activate genoflu-asia
genoflu-asia --input ~/projects/GenoFLU-Asia/test --output ~/genoflu_asia_analysis/output
```

- **Previous output:** existing workbooks are preserved; this test creates a new timestamped workbook.
- **Expected output:** 10 rows in the **All Results** sheet. Compare each virus ID and its `Genotype` with `test/expected_results.tsv`; the output `sample` field adds a full input filename stem (without `.fasta`) followed by `__` before the virus ID.
- **Major genotypes:** `AS-a.1(N6)`, `AS-b.1`, `AS-c.1`, `AS-d.1`, `NA.1(B3.2)`.
- **Minor genotypes:** `minor1(N6)`, `minor3(N6)`, `minor4`, `minor5(N6)`, `minor6(N6)`.
- **Input provenance:** the selected records retain their original FASTA headers, accession identifiers, and nucleotide sequences from the supplied dataset. Major/minor labels follow the study genotype definitions, not the number of examples in this test file.

## Interpreting results

![Example output workbook](docs/docs/output_workbook_example.svg?v=4)

*Example output from the All Results sheet. The H503 result and all nine output columns are shown. The genotype prefix has been removed from the sample name; other result values are unchanged.*

A genotype is assigned when all eight accepted segment groups match an entry in `genotype_key_asia.xlsx`.

- **Alignment selection:** within each virus and gene, select the highest BLAST bitscore; break ties by alignment length, then percent identity. Apply the fixed 97% identity threshold to the selected alignment.
- **Identity threshold:** BLAST nucleotide identity **≥97%** for each accepted segment. This is a fixed study criterion.
- **Alignment scope:** the threshold applies to local alignments; no minimum alignment-coverage filter is applied.

- **Why 97%?** Manual segment-cluster assignment in this study used a 97% pairwise nucleotide identity criterion, with values below 97% treated as evidence of distinct clusters. The fixed cutoff maintains consistency with that manual classification framework. Pairwise identity used for manual clustering and identity over a BLAST local alignment are not identical measurements; the cutoff is an operational assignment criterion, not a universal cluster boundary.
| Result or column | Meaning |
| --- | --- |
| `Genotype` | Assigned genotype; a `minor` name is also a valid assignment. |
| `Not assigned: No Matching Genotypes` | Eight accepted segments form a combination absent from the key; this alone does not establish a novel genotype. |
| `Not assigned: Only ... segments ...` | Fewer than eight segments pass the threshold; check missing segments, sequence quality, and FASTA IDs. |
| `Genotype Percent Match List` | Percent identities of the selected reference alignments. |
| `Genotype Mismatch List` | Mismatching-base counts within the corresponding alignments. |

- **List order:** match identity and mismatch entries to gene labels in `Genotype Sample Title List`; do not assume a fixed segment order.
- **Completeness:** confirm that all expected virus IDs appear in the workbook.
- **Date:** `date` records the analysis date.
- **Read depth:** unavailable from FASTA input.
- **Setup errors:** check environment activation, dependencies, and lowercase `.fasta` extensions.

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

## Reference Database Structure

GenoFLU-Asia follows the reference-sequence and genotype-definition approach described in [GenoFLU](https://github.com/USDA-VS/GenoFLU#-reference-database-structure).

```text
dependencies/
├── asia_fastas/
│   ├── PB2.fasta
│   ├── PB1.fasta
│   ├── PA.fasta
│   ├── HA.fasta
│   ├── NP.fasta
│   ├── NA.fasta
│   ├── MP.fasta
│   └── NS.fasta
└── genotype_key_asia.xlsx
```

### Reference FASTA files

Each FASTA file contains reference nucleotide sequences for one segment.

- All reference FASTA files are combined to build the BLAST database.
- Reference headers use three `|`-separated fields: `segment_group|reference_id|gene`.
- Illustrative header: `>PB2_group1|reference_001|PB2`, followed by its nucleotide sequence.
- `PB2_group1` identifies the segment group; `reference_001` identifies the reference; `PB2` identifies the gene.
- Reference headers differ from the input-virus headers described [above](#prepare-fasta-headers).

### Genotype definitions (genotype_key_asia.xlsx)

`genotype_key_asia.xlsx` maps genotype names to their eight-segment combinations.

- **Columns:** `Genotype`, `PB2`, `PB1`, `PA`, `HA`, `NP`, `NA`, `MP`, and `NS`.
- **Identifiers:** segment-group values must exactly match the reference FASTA headers.
- **Matching:** The accepted eight-segment constellation determines the genotype assignment.
- **Updates:** keep reference sequences and the key consistent; segment-group identifiers are distinct from whole-virus genotype names such as `AS-d.1`.

## Acknowledgments and license

Developed in collaboration with the **Korea Disease Control and Prevention Agency (KDCA), Republic of Korea**, and based on [USDA-VS/GenoFLU](https://github.com/USDA-VS/GenoFLU).

- **Software:** based on USDA-VS/GenoFLU; the upstream GPL-3.0 license is included in [LICENSE](LICENSE). This adaptation adds Asia-specific reference sequences and genotype definitions, batch processing, and combined Excel output.
- **Sequence data:** follow source-specific terms and acknowledgments, including GISAID where applicable.
- **Citation:** cite the GenoFLU-Asia repository and the version or commit used; the study citation will be added when available. Software citation metadata is provided in `CITATION.cff`.
- **Upstream publication:** Youk S, et al. (2023). H5N1 highly pathogenic avian influenza clade 2.3.4.4b in wild and domestic birds: Introductions into the United States and reassortments, December 2021–April 2022. *Virology* 587:109860. [doi:10.1016/j.virol.2023.109860](https://doi.org/10.1016/j.virol.2023.109860).
