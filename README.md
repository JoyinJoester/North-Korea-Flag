# North Korea Contributor Flag

[English](README.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md)

A GitHub Action that generates a configurable North Korea flag SVG with your project's top contributors displayed on the flag.

![Example](output.svg)

---

## What This Does

This action automatically generates an SVG image that looks like the North Korea national flag, but with two customizations:

1. **The star can be replaced** with your project's logo/icon
2. **The top contributors** (by commit count) are shown as circular avatars on the red stripe

The SVG updates automatically every week, so the contributor list stays current.

### Visual Layout

```
┌──────────────────────────────────────────────────┐
│  ┌─── blue stripe ────┐                          │
│  │                    │                          │
│  ├─── white stripe ───┤                          │
│  │                    │                          │
│  │    ┌──────────┐    │    ┌───┐  ┌───┐  ┌───┐  │
│  │    │          │    │    │   │  │   │  │   │  │
│  │    │  icon/   │    │    │ 👤│  │ 👤│  │ 👤│  │
│  │    │  star    │    │    │   │  │   │  │   │  │
│  │    │          │    │    └───┘  └───┘  └───┘  │
│  │    └──────────┘    │    user1  user2  user3   │
│  │       white disc   │    372     49     13     │
│  │                    │    commits               │
│  ├─── white stripe ───┤                          │
│  │                    │                          │
│  └─── blue stripe ────┘                          │
│                                                  │
│         ← flag (660×400px) →                     │
└──────────────────────────────────────────────────┘
```

- **Left side**: White disc with your icon (or a red star by default)
- **Right side**: Top contributors' GitHub avatars, automatically clipped into circles, with their username and commit count below

---

## Quick Start (3 Steps)

### Step 1: Create the workflow file

In your GitHub repository, create a file at `.github/workflows/contributors.yml`:

```yaml
name: Update Contributor Flag
on:
  workflow_dispatch:        # allows manual trigger
  schedule:
    - cron: '17 3 * * 1'   # runs every Monday at 03:17 UTC

permissions:
  contents: write           # needed to commit the SVG file

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: JoyinJoester/North-Korea-Flag@main
        with:
          repo: 'your-username/your-repo'   # ← change this to your repo
```

> **Tip**: Replace `your-username/your-repo` with your actual GitHub repository, e.g. `octocat/Hello-World`.

### Step 2: Run the workflow

Go to your repo → **Actions** tab → click **Update Contributor Flag** → **Run workflow**.

Wait about 30 seconds for it to complete. It will create a `North Korea/output.svg` file in your repo.

### Step 3: Add to your README

In your `README.md`, add this line where you want the flag to appear:

```markdown
![Contributors](North-Korea-Flag/output.svg)
```

That's it! The flag will update automatically every week.

---

## Configuration

### Minimal (just the repo)

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: 'owner/repo'
```

This uses the default North Korea flag colors (blue/red/white) with a red star.

### Custom colors

Change the flag stripe colors to match your project's theme:

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: 'owner/repo'
    blue: '#1a365d'     # dark navy blue
    red: '#c53030'      # dark red
    white: '#ffffff'    # white
```

Color values are in hex format (e.g. `#FF0000` for red). You can use any hex color picker online to find the right values.

### Custom icon (replacing the star)

Replace the red star with your project's logo:

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: 'owner/repo'
    icon-url: 'https://raw.githubusercontent.com/owner/repo/main/icon.png'
```

**Important notes about the icon**:
- The image must be accessible via a public URL
- Any shape will be automatically clipped into a circle
- For best results, use a square image (e.g. 256×256 or 512×512)
- GitHub raw URLs work well: `https://raw.githubusercontent.com/owner/repo/branch/path/to/icon.png`
- The icon scale defaults to 0.8 (80% of the disc). Set `icon-scale: '1.0'` to fill the entire disc

### Full example with all options

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: 'owner/repo'
    blue: '#024FA2'
    red: '#ED1C27'
    white: '#FFFFFF'
    icon-url: 'https://raw.githubusercontent.com/owner/repo/main/logo.png'
    icon-scale: '0.8'
    count: '5'
    output: 'North Korea/output.svg'
```

---

## All Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `repo` | No | GitHub repository in `owner/repo` format. If not set, uses the current repository. | `${{ github.repository }}` |
| `blue` | No | Hex color for the top and bottom blue stripes | `#024FA2` |
| `red` | No | Hex color for the center red stripe | `#ED1C27` |
| `white` | No | Hex color for the thin white stripes and disc | `#FFFFFF` |
| `icon-url` | No | Public URL of an image to replace the red star. Any shape is auto-clipped to a circle. | Red 5-pointed star |
| `icon-scale` | No | How large the icon is relative to the white disc (0.0 to 1.0) | `0.8` |
| `count` | No | Number of top contributors to display on the flag | `3` |
| `output` | No | Path where the generated SVG will be saved | `North Korea/output.svg` |

---

## How It Works

1. The action fetches the top contributors from the GitHub API (sorted by total commit count)
2. It generates an SVG with the flag stripes, the icon/star, and circular avatar images
3. Avatar images are loaded directly from GitHub's CDN (`github.com/username.png`) — no downloads needed
4. The SVG is committed to your repository automatically
5. Your README references the SVG file, which GitHub renders inline

### What gets committed?

Only two files are created/updated in your repo:
- `North Korea/output.svg` — the main composite image (flag + contributors)
- `North Korea/flag.svg` — standalone flag (for separate use)

---

## Standalone Usage (Without GitHub Actions)

If you prefer to run the script locally or in a different CI system:

```bash
# Basic usage
python "North-Korea-Flag/generate.py" --repo owner/repo

# With custom colors
python "North-Korea-Flag/generate.py" --repo owner/repo --blue "#0055aa" --red "#cc0000"

# With a custom icon
python "North-Korea-Flag/generate.py" --repo owner/repo --icon-url "https://example.com/icon.png"

# Show 5 contributors instead of 3
python "North-Korea-Flag/generate.py" --repo owner/repo --count 5

# Custom output path
python "North-Korea-Flag/generate.py" --repo owner/repo --output "./my-flag.svg"
```

Requirements: Python 3.7+ (no pip packages needed — uses only stdlib).

---

## Troubleshooting

### The SVG shows placeholder names instead of real contributors

This means the GitHub API request failed. Common causes:
- **Private repository**: The action needs access to the repo's contributor list. For private repos, you may need to provide a `GITHUB_TOKEN` in the workflow.
- **Rate limiting**: Unauthenticated API requests are limited to 60/hour. If you're testing frequently, wait or use a token.

### The icon doesn't show up

- Make sure the `icon-url` is a direct link to an image file (not a webpage)
- The URL must be publicly accessible (try opening it in an incognito browser window)
- Supported formats: PNG, JPG, SVG, WebP

### The workflow doesn't run on schedule

- GitHub disables scheduled workflows in repos with no activity for 60 days
- Push any commit to re-enable it
- You can always trigger manually via **Actions** → **Run workflow**

### Avatars look broken or don't load

- Avatars are loaded from `github.com/username.png` — this only works when the SVG is viewed on GitHub (in READMEs, issues, etc.)
- If viewing the SVG locally in a browser, avatars may not load due to CORS restrictions

---

## License

MIT
