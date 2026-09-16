# GenoFLU-Asia 설치와 실행: 처음 사용하는 분을 위한 안내

이 안내는 Windows에서 Ubuntu(WSL)와 Conda를 이미 사용할 수 있는 경우를 기준으로 합니다. 아래 명령은 Ubuntu 터미널에서 실행합니다. 현재 사용 중인 설치가 정상 작동한다면 새로 설치하거나 기존 폴더를 옮길 필요가 없습니다.

## 1. 먼저 구분할 세 가지

| 이름 | 의미 |
| --- | --- |
| 프로그램 폴더 | Git으로 내려받은 `genoflu.py`, 스크립트, 참조 파일을 보관하는 곳 |
| Conda 환경 | Python, BLAST 등 실행에 필요한 프로그램을 모아 둔 환경 |
| 분석 폴더 | 분석할 FASTA와 결과 Excel을 보관하는 곳 |

프로그램 폴더를 Conda의 `envs` 폴더 안에 넣을 필요는 없습니다. `conda activate`는 사용할 프로그램 환경을 선택하며, 현재 폴더를 이동시키지 않습니다. 폴더 이동에는 `cd`를 사용합니다.

아래 예시에서는 프로그램을 `~/projects/GenoFLU-Asia`, 분석 파일을 `~/genoflu_asia_analysis`에 둡니다. `~`는 현재 Ubuntu 사용자의 홈 폴더를 뜻합니다. 예를 들어 사용자 이름이 `skykjiyun`이면 `~`는 `/home/skykjiyun`입니다.

## 2. Ubuntu 열기와 Conda 확인

Windows 시작 메뉴에서 Ubuntu를 검색해 실행합니다. 명령을 한 줄씩 붙여 넣고 Enter를 누릅니다. 화면에 이미 보이는 `(base) 사용자@컴퓨터:~$` 부분은 입력하지 않습니다.

```bash
conda --version
conda env list
```

첫 명령은 Conda 버전, 두 번째는 기존 환경 목록을 보여 줍니다. `genoflu-asia`가 이미 있고 필요한 패키지가 설치되어 있다면 환경 생성은 건너뜁니다. 현재 선택된 환경은 목록에 `*`로 표시됩니다. [Conda 환경 안내](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)

`conda: command not found`가 나오면 지금 사용하는 Ubuntu에서 Conda를 사용할 수 없는 상태입니다. Windows에만 설치된 Conda와 WSL 내부의 Conda는 별개입니다. 이미 설치한 Conda의 설정을 먼저 확인하고, 없다면 Ubuntu 내부에 Linux용 Miniforge 또는 Miniconda를 설치해야 합니다.

## 3. Git으로 프로그램 받기 — 처음 한 번

조직 ID는 KDCA-KNU-VirusResearch이며 아래 명령으로 GenoFLU-Asia 저장소를 내려받습니다. 이미 사용 중인 로컬 프로젝트가 있으면 다시 내려받지 않고 기존 폴더를 사용합니다. 새로 설치할 때는 먼저 Ubuntu에서 Git이 있는지 확인합니다.

```bash
git --version
```

Git이 없다고 나오면 설치합니다.

```bash
sudo apt update
sudo apt install git
```

sudo가 비밀번호를 요청하면 Ubuntu 비밀번호를 입력합니다. 입력 중 화면에 글자가 나타나지 않는 것은 정상입니다.

다음 명령을 순서대로 실행하세요.

```bash
mkdir -p ~/projects
git clone https://github.com/KDCA-KNU-VirusResearch/GenoFLU-Asia.git ~/projects/GenoFLU-Asia
cd ~/projects/GenoFLU-Asia
ls
```

- `mkdir -p`: 프로젝트를 둘 상위 폴더를 만듭니다.
- `git clone`: 코드·참조 파일·genotype key를 함께 내려받습니다.
- `cd`: 프로그램 폴더로 이동합니다.
- `ls`: 파일 목록을 봅니다. genoflu.py, run_genoflu.sh, install_command.sh, dependencies가 있는지 확인합니다.

프로그램 폴더와 분석 폴더 `~/genoflu_asia_analysis`는 서로 다른 폴더입니다. 현재 프로그램 폴더가 다른 위치에 있다면 예시의 경로를 실제 위치에 맞추세요.

## 4. Conda 환경 생성 — 처음 한 번

기존에 필요한 패키지가 설치된 `genoflu-asia` 환경이 있으면 생성 명령은 생략하세요.

```bash
conda create -n genoflu-asia --override-channels -c conda-forge -c bioconda python=3.13 pandas=2.3.2 biopython=1.85 openpyxl=3.1.5 blast=2.17.0
```

이것은 한 줄 명령입니다. `Proceed ([y]/n)?`가 표시되면 설치 목록을 확인한 뒤 `y`를 입력하고 Enter를 누릅니다. 설치가 끝나 입력 가능한 프롬프트가 다시 나타날 때까지 기다립니다.

- `-n genoflu-asia`: 환경 이름을 정합니다.
- `--override-channels -c conda-forge -c bioconda`: 패키지를 가져올 저장소를 지정합니다.
- `python`: 분석 코드를 실행합니다.
- `pandas`, `openpyxl`: 표와 Excel 파일을 처리합니다.
- `biopython`: 서열 데이터를 처리합니다.
- `blast`: 입력 서열과 참조 서열을 비교합니다.
- `=숫자`: 설치할 버전입니다. 현재 로컬 구성의 버전이며, 새 환경 설치 검증은 아직 완료하지 않았습니다.

환경을 활성화합니다.

```bash
conda activate genoflu-asia
```

필요한 프로그램을 확인할 수 있습니다.

```bash
python -c "import pandas, Bio, openpyxl; print('Python dependencies available')"
blastn -version
makeblastdb -version
```

오류 없이 확인 문구와 버전이 나오면 해당 의존성을 사용할 수 있습니다. 이것이 전체 분석 성공을 보장하는 검사는 아닙니다.

## 5. 짧은 실행 명령 등록 — 처음 한 번

```bash
cd ~/projects/GenoFLU-Asia
conda activate genoflu-asia
bash install_command.sh
genoflu-asia --help
```

설치 스크립트는 활성화된 환경에 `genoflu-asia`라는 실행 명령을 등록합니다. `Registered:`가 보이고 마지막 명령에서 사용법이 표시되면 등록을 확인한 것입니다. `--help`는 분석을 시작하지 않습니다.

이미 등록했다면 반복할 필요가 없습니다. `Command already exists`는 같은 이름의 명령이 이미 있다는 뜻입니다. 우선 `genoflu-asia --help`를 확인하세요. 현재 설치 스크립트는 기존 명령을 덮어쓰지 않으므로, 프로그램 폴더를 옮긴 뒤 단순히 재실행하는 것만으로 경로가 갱신되지는 않습니다. 등록 후 폴더 위치를 유지하세요.

## 6. 입력·출력 폴더 만들기 — 처음 한 번

```bash
mkdir -p ~/genoflu_asia_analysis/input ~/genoflu_asia_analysis/output
cd ~/genoflu_asia_analysis
pwd
```

`pwd`는 현재 위치를 보여 줍니다. 다음 구조가 만들어집니다.

```text
~/genoflu_asia_analysis/
├── input/       ← 분석할 FASTA 파일
└── output/      ← 분석 후 결과 Excel
```

입력 폴더를 탐색기로 엽니다.

```bash
explorer.exe input
```

여기에 실제 분석할 FASTA 파일을 복사합니다. 예: `sample01.fasta`, `sample02.fasta`. 파일명만 바꾼 Excel이나 Word 문서는 FASTA가 아닙니다. `.fa`, `.fna`, `.FASTA`, `.fasta.txt`는 현재 일괄 실행 스크립트의 대상이 아닙니다. 확장자를 포함한 전체 파일명을 확인하세요.

FASTA 안에서는 각 서열의 제목이 `>`로 시작하고 그 아래에 실제 염기서열이 옵니다. 한 바이러스의 모든 분절은 첫 `|` 앞에 같은 ID를 사용해야 합니다. 제목 예시는 `>sample01|PB2`, `>sample01|PB1`입니다. 이 두 제목만 복사한 파일은 분석 입력으로 사용할 수 없습니다.

완전한 genotype 판정에는 PB2, PB1, PA, HA, NP, NA, MP, NS의 8개 분절이 필요합니다. 서로 다른 바이러스는 서로 다른 ID를 사용합니다. 한 FASTA에 여러 바이러스가 있어도 되며, `input` 바로 아래의 모든 소문자 `.fasta` 파일을 분석합니다. 하위 폴더는 검색하지 않습니다.

파일을 확인합니다.

```bash
ls ~/genoflu_asia_analysis/input
```

## 7. 분석 실행

```bash
conda activate genoflu-asia
cd ~/genoflu_asia_analysis
genoflu-asia --input ./input --output ./output
```

- `genoflu-asia`: 등록한 실행 명령입니다.
- `--input ./input`: 현재 위치 안의 `input` 폴더에서 파일을 읽습니다. 특정 파일명을 지정하는 옵션이 아닙니다.
- `--output ./output`: 현재 위치 안의 `output` 폴더에 결과를 저장합니다.
- `./`는 현재 폴더입니다. `cd`로 이동한 위치에 따라 의미가 달라집니다.

위 예시에서는 입력이 `~/genoflu_asia_analysis/input`, 출력이 `~/genoflu_asia_analysis/output`입니다. 현재 위치에 상관없이 실행하려면 다음처럼 경로를 명시할 수도 있습니다.

```bash
genoflu-asia --input ~/genoflu_asia_analysis/input --output ~/genoflu_asia_analysis/output
```

`Processing ...`가 나타나면 처리가 진행 중입니다. 오류가 없는지 확인하고 마지막에 `All files processed.`가 나올 때까지 기다립니다. 같은 프로젝트로 여러 분석을 동시에 실행하지 않습니다.

## 8. 결과 확인

```bash
explorer.exe ~/genoflu_asia_analysis/output
```

`genoflu_combined_results.xlsx`를 열어 `All Results` 시트를 확인합니다.

- `Genotype`: 지정된 genotype입니다. `minor`도 정상적인 분류명입니다.
- `Not assigned: No Matching Genotypes`: 참조 key에 일치하는 조합이 없다는 뜻이며, 이것만으로 신규 genotype이 입증되지는 않습니다.
- `Not assigned: Only ... segments ...`: 판정에 사용할 수 있는 분절이 부족합니다. 입력 분절, 품질, ID를 확인합니다.
- `Genotype Percent Match List`: 선택된 참조 정렬의 염기 일치율입니다.
- `Genotype Mismatch List`: 해당 정렬에서 불일치한 염기 개수입니다.

분석 종료 문구와 별도로 입력한 모든 바이러스 ID가 결과에 있는지 확인하세요. 목록의 값은 `Genotype Sample Title List`의 유전자 표시와 맞춰 읽습니다.

## 9. 다음 분석 때 필요한 것

같은 input과 output 폴더를 계속 사용합니다. 환경 생성·명령 등록·분석 폴더 생성을 반복할 필요가 없습니다.

1. input에서 이번에 분석하지 않을 FASTA 파일을 다른 곳으로 옮기고 새 파일을 넣습니다. 남겨 둔 모든 .fasta 파일이 다시 분석됩니다.
2. 이전 결과가 필요하면 output/genoflu_combined_results.xlsx를 다른 이름으로 바꾸거나 복사해 보관합니다. 다음 실행은 같은 결과 파일명을 사용합니다.
3. 다음 명령을 실행합니다.

```bash
conda activate genoflu-asia
cd ~/genoflu_asia_analysis
genoflu-asia --input ./input --output ./output
```

분석이 중단되었다면 프로그램 폴더에 남은 genoflu_combined_results.xlsx를 먼저 별도로 보관하고 재시작합니다. 남은 파일에 새 결과가 이어 붙을 수 있습니다. 같은 프로그램 폴더로 여러 분석을 동시에 실행하지 않습니다.

## 10. 자주 만나는 메시지

| 메시지 | 확인할 점 |
| --- | --- |
| `conda: command not found` | 현재 Ubuntu에서 Conda 설치·초기화가 되어 있는지 확인 |
| `EnvironmentNameNotFound` | `conda env list`에서 환경 이름 확인 |
| `genoflu-asia: command not found` | 환경 활성화 후 명령 등록 여부 확인 |
| `install_command.sh: No such file or directory` | `pwd`, `ls`로 실제 프로그램 폴더인지 확인 |
| `No .fasta files found` | 입력 경로와 실제 파일 확장자 확인 |
| `ModuleNotFoundError` | 올바른 환경이 활성화되어 있고 필요한 패키지가 설치되었는지 확인 |
| `Use paths with letters...` | 프로그램·입력 경로와 파일명의 한글, 공백, 괄호 등 확인 |
| `Command already exists` | 등록 명령이 이미 존재함. `--help` 확인 후 기존 설치 상태 점검 |

오류가 나면 마지막 한 줄만이 아니라 실행한 명령과 오류 메시지 전체를 보관하세요.
