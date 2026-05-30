# 북한 국기 기여자 컴포넌트

[English](README.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md)

프로젝트의 주요 기여자 아바타가 포함된 북한 국기 SVG를 자동으로 생성하는 GitHub Action입니다.

![예시](output.svg)

---

## 이게 뭔가요?

이 Action은 북한 국기 모양의 SVG 이미지를 자동으로 생성하며, 두 가지를 커스터마이징할 수 있습니다:

1. **국기의 별을 프로젝트 아이콘으로 교체** (기본 빨간 별 유지 가능)
2. **빨간색 줄무늬 위에 기여자의 GitHub 아바타 표시** (커밋 수 기준 랭킹)

SVG는 매주 자동 업데이트되어 기여자 목록이 최신 상태를 유지합니다.

### 레이아웃 설명

```
┌──────────────────────────────────────────────────┐
│  ┌─── 파란색 줄무늬 ────┐                         │
│  │                      │                         │
│  ├─── 흰색 줄무늬 ─────┤                         │
│  │                      │                         │
│  │    ┌──────────────┐  │   ┌───┐  ┌───┐  ┌───┐  │
│  │    │              │  │   │   │  │   │  │   │  │
│  │    │  프로젝트    │  │   │ 👤│  │ 👤│  │ 👤│  │
│  │    │  아이콘/별   │  │   │   │  │   │  │   │  │
│  │    │              │  │   └───┘  └───┘  └───┘  │
│  │    └──────────────┘  │   유저1  유저2  유저3   │
│  │      흰색 원형       │   372     49     13     │
│  │                      │   커밋                  │
│  ├─── 흰색 줄무늬 ─────┤                         │
│  │                      │                         │
│  └─── 파란색 줄무늬 ────┘                         │
│                                                  │
│          ← 국기 영역 (660×400px) →               │
└──────────────────────────────────────────────────┘
```

- **왼쪽**: 흰색 원 안에 아이콘 (미설정 시 빨간 별)
- **오른쪽 빨간 영역**: 기여자의 GitHub 아바타 (자동 원형 클리핑) + 사용자 이름 + 커밋 수

---

## 빠른 시작 (3단계)

### 1단계: 워크플로우 파일 만들기

GitHub 저장소에 `.github/workflows/contributors.yml` 파일을 생성합니다:

```yaml
name: 기여자 국기 업데이트
on:
  workflow_dispatch:        # 수동 실행 허용
  schedule:
    - cron: '17 3 * * 1'   # 매주 월요일 03:17 UTC 자동 실행

permissions:
  contents: write           # SVG 파일 커밋에 필요

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: JoyinJoester/North-Korea-Flag@main
        with:
          repo: '사용자이름/저장소이름'   # ← 여기를 변경하세요
```

> **팁**: `사용자이름/저장소이름`을 실제 GitHub 저장소로 바꾸세요. 예: `octocat/Hello-World`

### 2단계: 워크플로우 실행

저장소 → **Actions** 탭 → 왼쪽에서 **기여자 국기 업데이트** 클릭 → **Run workflow** 클릭 → 초록색 **Run workflow** 버튼 클릭.

약 30초 기다리면 `North Korea/output.svg` 파일이 생성됩니다.

### 3단계: README에 추가

`README.md`에 다음 줄을 추가합니다:

```markdown
![기여자](North-Korea-Flag/output.svg)
```

완료! 국기가 매주 자동 업데이트됩니다.

---

## 설정 방법

### 최소 설정 (저장소만 지정)

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '사용자이름/저장소이름'
```

기본 북한 국기 색상 (파랑/빨강/흰색)에 빨간 별이 표시됩니다.

### 색상 커스터마이징

국기 줄무늬 색상을 프로젝트 테마에 맞게 변경:

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '사용자이름/저장소이름'
    blue: '#1a365d'     # 진한 네이비 블루
    red: '#c53030'      # 진한 빨강
    white: '#ffffff'    # 흰색
```

색상값은 16진수(hex) 형식입니다 (예: `#FF0000` = 빨강). 온라인 "색상 선택기"로 원하는 색상을 찾을 수 있습니다.

### 커스텀 아이콘 (별 교체)

프로젝트 로고로 빨간 별을 교체:

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '사용자이름/저장소이름'
    icon-url: 'https://raw.githubusercontent.com/사용자이름/저장소이름/main/icon.png'
```

**아이콘 관련 참고사항**:
- 이미지는 공개 URL이어야 합니다
- **어떤 모양이든 자동으로 원형으로 클리핑됩니다**
- 정사각형 이미지 사용을 권장합니다 (예: 256×256 또는 512×512)
- GitHub raw 링크 형식: `https://raw.githubusercontent.com/사용자/저장소/브랜치/이미지경로`
- 기본 크기는 원의 80%. `icon-scale: '1.0'`으로 설정하면 원 전체를 채웁니다

### 전체 설정 예시

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: 'your-username/your-repo'
    blue: '#024FA2'
    red: '#ED1C27'
    white: '#FFFFFF'
    icon-url: 'https://raw.githubusercontent.com/your-username/your-repo/main/logo.png'
    icon-scale: '0.8'
    count: '5'
    output: 'North Korea/output.svg'
```

---

## 전체 파라미터

| 파라미터 | 필수 | 설명 | 기본값 |
|----------|------|------|--------|
| `repo` | 아니오 | `소유자/저장소` 형식의 GitHub 저장소. 미설정 시 현재 저장소 사용. | `${{ github.repository }}` |
| `blue` | 아니오 | 상하 파란색 줄무늬의 16진수 색상값 | `#024FA2` |
| `red` | 아니오 | 중앙 빨간색 줄무늬의 16진수 색상값 | `#ED1C27` |
| `white` | 아니오 | 흰색 줄무늬와 원형의 16진수 색상값 | `#FFFFFF` |
| `icon-url` | 아니오 | 빨간 별을 대체할 프로젝트 아이콘 URL. 어떤 모양이든 원형 클리핑. | 빨간 별 |
| `icon-scale` | 아니오 | 아이콘 크기 비율 (0.0 ~ 1.0) | `0.8` |
| `count` | 아니오 | 표시할 기여자 수 | `3` |
| `output` | 아니오 | 생성된 SVG 저장 경로 | `North Korea/output.svg` |

---

## 작동 방식

1. GitHub API에서 저장소의 상위 기여자를 가져옵니다 (총 커밋 수 기준 정렬)
2. 국기 줄무늬, 아이콘/별, 원형 아바타 이미지가 포함된 SVG를 생성합니다
3. 아바타 이미지는 GitHub CDN(`github.com/사용자명.png`)에서 직접 로드됩니다
4. SVG가 저장소에 자동 커밋됩니다
5. README에서 SVG 파일을 참조하면 GitHub에서 자동으로 렌더링됩니다

### 커밋되는 파일

저장소에 2개의 파일만 생성/업데이트됩니다:
- `North Korea/output.svg` — 메인 합성 이미지 (국기 + 기여자)
- `North Korea/flag.svg` — 독립 국기 이미지 (별도 사용 가능)

---

## GitHub Actions 없이 사용하기

로컬이나 다른 CI 시스템에서 실행하려면:

```bash
# 기본 사용
python "North-Korea-Flag/generate.py" --repo owner/repo

# 커스텀 색상
python "North-Korea-Flag/generate.py" --repo owner/repo --blue "#0055aa" --red "#cc0000"

# 커스텀 아이콘
python "North-Korea-Flag/generate.py" --repo owner/repo --icon-url "https://example.com/icon.png"

# 기여자 5명 표시
python "North-Korea-Flag/generate.py" --repo owner/repo --count 5

# 출력 경로 지정
python "North-Korea-Flag/generate.py" --repo owner/repo --output "./my-flag.svg"
```

요구사항: Python 3.7+ (서드파티 패키지 불필요 — 표준 라이브러리만 사용).

---

## 문제 해결

### SVG에 실제 기여자 대신 플레이스홀더 이름이 표시됨

GitHub API 요청이 실패한 것입니다. 일반적인 원인:
- **비공개 저장소**: Action은 저장소의 기여자 목록에 접근해야 합니다. 비공개 저장소는 `GITHUB_TOKEN` 추가 설정이 필요할 수 있습니다.
- **API 속도 제한**: 인증되지 않은 API 요청은 시간당 60회로 제한됩니다. 빈번하게 테스트할 때는 기다리거나 토큰을 사용하세요.

### 아이콘이 표시되지 않음

- `icon-url`이 이미지 파일의 직접 링크인지 확인하세요 (웹페이지 링크가 아닌)
- URL이 공개적으로 접근 가능해야 합니다 (시크릿 모드에서 열어보세요)
- 지원 형식: PNG, JPG, SVG, WebP

### 워크플로우가 예약대로 자동 실행되지 않음

- GitHub는 저장소 활동이 60일간 없으면 예약 워크플로우를 자동 비활성화합니다
- 아무 커밋이나 푸시하면 다시 활성화됩니다
- **Actions** → **Run workflow**로 언제든 수동 실행 가능

### 아바타가 표시되지 않음

- 아바타는 `github.com/사용자명.png`에서 로드되며, GitHub에서 SVG를 볼 때만 정상 표시됩니다 (README, 이슈 등)
- 로컬 브라우저에서 SVG를 보면 CORS 제한으로 아바타가 로드되지 않을 수 있습니다

---

## 라이선스

MIT
