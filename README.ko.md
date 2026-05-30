# 북한 국기 기여자 컴포넌트

[English](README.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md)

프로젝트의 주요 기여자 아바타가 포함된 북한 국기 SVG를 자동으로 생성하는 GitHub Action입니다.

![예시](output.svg)

---

## 이게 뭔가요?

이 Action은 북한 국기 모양의 SVG 이미지를 자동으로 생성하며, 두 가지를 커스터마이징할 수 있습니다:

1. **국기의 별을 프로젝트 아이콘으로 교체** (기본 빨간 별 유지 가능)
2. **빨간색 줄무늬 위에 기여자의 아바타 표시** (커밋 수 기준 랭킹), 다양한 아바타 모양 지원

SVG는 매주 자동 업데이트되어 기여자 목록이 최신 상태를 유지합니다.

---

## 웹 생성기

GitHub Actions를 설정하기 싫으신가요? **[온라인 생성기](https://joyinjoester.github.io/North-Korea-Flag/)**에서 웹페이지에서 직접 국기를 만들고 미리보기한 후 SVG 또는 PNG로 다운로드하세요.

기능:
- 실시간 미리보기 (변경 즉시 반영)
- 줄무늬 색상 선택기
- 커스텀 아이콘 업로드 및 크기 조절
- 다양한 아바타 모양: 원형, 정사각형, 증명사진 비율(3:4), 세로형(2:3) 등
- 기여자 텍스트 숨기기 옵션
- 공개 GitHub 저장소에서 기여자 자동 가져오기
- SVG 또는 고해상도 PNG 내보내기

---

## 빠른 시작 (3단계)

### 1단계: 워크플로우 파일 만들기

GitHub 저장소에 `.github/workflows/contributors.yml` 파일을 생성합니다:

```yaml
name: 기여자 국기 업데이트
on:
  workflow_dispatch:
  schedule:
    - cron: '17 3 * * 1'

permissions:
  contents: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: JoyinJoester/North-Korea-Flag@main
        with:
          repo: '사용자이름/저장소이름'
```

### 2단계: 워크플로우 실행

저장소 → **Actions** 탭 → **기여자 국기 업데이트** 클릭 → **Run workflow** 클릭.

약 30초 기다리면 `output.svg` 파일이 생성됩니다.

### 3단계: README에 추가

```markdown
![기여자](output.svg)
```

완료! 국기가 매주 자동 업데이트됩니다.

---

## 설정 방법

### 최소 설정

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '사용자이름/저장소이름'
```

### 색상 커스터마이징

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '사용자이름/저장소이름'
    blue: '#1a365d'
    red: '#c53030'
    white: '#ffffff'
```

### 커스텀 아이콘 (별 교체)

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '사용자이름/저장소이름'
    icon-url: 'https://raw.githubusercontent.com/사용자이름/저장소이름/main/icon.png'
```

- 어떤 모양이든 자동으로 원형으로 클리핑됩니다
- 정사각형 이미지 권장 (256×256 또는 512×512)

### 아바타 모양

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '사용자이름/저장소이름'
    shape: '3:4'    # 증명사진 비율
```

| 모양 | 설명 |
|------|------|
| `circle` | 기본 원형 |
| `roundrect` | 둥근 사각형 |
| `1:1` | 정사각형 |
| `3:4` | 증명사진 비율 |
| `2:3` | 세로형 |
| `4:5` | 사진 비율 |

### 텍스트 숨기기

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '사용자이름/저장소이름'
    no-text: 'true'
```

---

## 전체 파라미터

| 파라미터 | 필수 | 설명 | 기본값 |
|----------|------|------|--------|
| `repo` | 아니오 | GitHub 저장소 (`소유자/저장소`) | `${{ github.repository }}` |
| `blue` | 아니오 | 파란색 줄무늬 색상 | `#024FA2` |
| `red` | 아니오 | 빨간색 줄무늬 색상 | `#ED1C27` |
| `white` | 아니오 | 흰색 색상 | `#FFFFFF` |
| `icon-url` | 아니오 | 프로젝트 아이콘 URL | 빨간 별 |
| `icon-scale` | 아니오 | 아이콘 크기 비율 (0.0~1.0) | `0.8` |
| `count` | 아니오 | 기여자 수 | `3` |
| `shape` | 아니오 | 아바타 모양 | `circle` |
| `no-text` | 아니오 | 텍스트 숨기기 | (비움) |
| `output` | 아니오 | SVG 저장 경로 | `output.svg` |

---

## GitHub Actions 없이 사용하기

```bash
python generate.py --repo owner/repo
python generate.py --repo owner/repo --shape 3:4 --no-text
python generate.py --repo owner/repo --count 5 --blue "#0055aa"
```

요구사항: Python 3.7+ (표준 라이브러리만 사용).

---

## 라이선스

MIT
