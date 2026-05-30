# North Korea 贡献者旗帜组件

[English](README.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md)

一个 GitHub Action，自动生成带有项目贡献者头像的朝鲜国旗 SVG 组件。

![示例](output.svg)

---

## 这是什么

这个 Action 会自动生成一张朝鲜国旗样式的 SVG 图片，并做两件事：

1. **用你的项目图标替换国旗上的红星**（也可以保留默认红星）
2. **在国旗的红色区域上显示贡献者的 GitHub 头像**（按 commit 数量排名）

SVG 每周自动更新一次，贡献者排名会随代码提交变化。

### 组件布局

```
┌──────────────────────────────────────────────────┐
│  ┌─── 蓝色条纹 ────┐                             │
│  │                  │                             │
│  ├─── 白色条纹 ────┤                             │
│  │                  │                             │
│  │    ┌──────────┐  │     ┌───┐  ┌───┐  ┌───┐   │
│  │    │          │  │     │   │  │   │  │   │   │
│  │    │  项目图标 │  │     │ 👤│  │ 👤│  │ 👤│   │
│  │    │  或红星   │  │     │   │  │   │  │   │   │
│  │    │          │  │     └───┘  └───┘  └───┘   │
│  │    └──────────┘  │     用户1  用户2  用户3     │
│  │     白色圆盘      │     372     49     13      │
│  │                  │     次提交                  │
│  ├─── 白色条纹 ────┤                             │
│  │                  │                             │
│  └─── 蓝色条纹 ────┘                             │
│                                                  │
│           ← 国旗区域 (660×400px) →               │
└──────────────────────────────────────────────────┘
```

- **左侧**：白色圆盘 + 你的图标（未设置则显示红色五角星）
- **右侧红色区域**：贡献者的 GitHub 头像（自动裁剪为圆形）+ 用户名 + commit 次数

---

## 快速开始（3 步）

### 第 1 步：创建 workflow 文件

在你的 GitHub 仓库中，创建文件 `.github/workflows/contributors.yml`：

```yaml
name: 更新贡献者旗帜
on:
  workflow_dispatch:        # 允许手动触发
  schedule:
    - cron: '17 3 * * 1'   # 每周一 03:17 UTC 自动运行

permissions:
  contents: write           # 需要写入权限来提交 SVG 文件

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: JoyinJoester/North-Korea-Flag@main
        with:
          repo: '你的用户名/你的仓库'   # ← 改成你的仓库地址
```

> **提示**：把 `你的用户名/你的仓库` 换成你的实际 GitHub 仓库，例如 `octocat/Hello-World`。

### 第 2 步：运行 workflow

进入你的仓库 → 点击 **Actions** 选项卡 → 点击左侧的 **更新贡献者旗帜** → 点击 **Run workflow** → 点击绿色的 **Run workflow** 按钮。

等待约 30 秒，workflow 会在仓库中创建 `North Korea/output.svg` 文件。

### 第 3 步：在 README 中引用

在你的 `README.md` 中，添加以下内容：

```markdown
![贡献者](North-Korea-Flag/output.svg)
```

完成！旗帜会每周自动更新。

---

## 配置说明

### 最简配置（只需仓库地址）

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '你的用户名/你的仓库'
```

使用默认朝鲜国旗配色（蓝/红/白），显示红色五角星。

### 自定义颜色

把国旗颜色换成你项目的主题色：

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '你的用户名/你的仓库'
    blue: '#1a365d'     # 深蓝色
    red: '#c53030'      # 深红色
    white: '#ffffff'    # 白色
```

颜色值使用十六进制格式（如 `#FF0000` 是纯红）。可以在网上搜索"颜色选择器"来找到想要的颜色值。

### 自定义图标（替换红星）

用你的项目 Logo 替换国旗上的五角星：

```yaml
- uses: JoyinJoester/North-Korea-Flag@main
  with:
    repo: '你的用户名/你的仓库'
    icon-url: 'https://raw.githubusercontent.com/你的用户名/你的仓库/main/icon.png'
```

**关于图标的注意事项**：
- 图片必须是公开可访问的 URL
- **任何形状的图片都会自动裁剪为圆形**
- 建议使用正方形图片（如 256×256 或 512×512），效果最佳
- GitHub raw 链接格式：`https://raw.githubusercontent.com/用户名/仓库名/分支名/图片路径`
- 默认缩放为圆盘的 80%，设置 `icon-scale: '1.0'` 可填满整个圆盘

### 完整配置示例

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

## 全部参数

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `repo` | 否 | GitHub 仓库，格式为 `用户名/仓库名`。不填则使用当前仓库。 | `${{ github.repository }}` |
| `blue` | 否 | 上下蓝色条纹的十六进制颜色值 | `#024FA2` |
| `red` | 否 | 中间红色条纹的十六进制颜色值 | `#ED1C27` |
| `white` | 否 | 白色条纹和圆盘的十六进制颜色值 | `#FFFFFF` |
| `icon-url` | 否 | 项目图标的公开图片 URL，任何形状自动裁剪为圆形 | 红色五角星 |
| `icon-scale` | 否 | 图标相对于白色圆盘的大小比例（0.0 到 1.0） | `0.8` |
| `count` | 否 | 显示的贡献者数量 | `3` |
| `output` | 否 | 生成的 SVG 保存路径 | `North Korea/output.svg` |

---

## 工作原理

1. 通过 GitHub API 获取仓库的 top 贡献者（按总 commit 数排序）
2. 生成包含国旗条纹、图标/红星、圆形头像的 SVG
3. 头像图片直接从 GitHub CDN 加载（`github.com/用户名.png`），无需下载
4. SVG 自动提交到你的仓库
5. README 引用 SVG 文件，GitHub 会自动渲染显示

### 会提交哪些文件？

只会在你的仓库中创建/更新两个文件：
- `North Korea/output.svg` — 主要的组合图片（国旗 + 贡献者）
- `North Korea/flag.svg` — 独立的国旗图片（可单独使用）

---

## 不使用 GitHub Actions 的方式

如果你想在本地或其他 CI 系统中运行：

```bash
# 基本用法
python "North-Korea-Flag/generate.py" --repo owner/repo

# 自定义颜色
python "North-Korea-Flag/generate.py" --repo owner/repo --blue "#0055aa" --red "#cc0000"

# 使用自定义图标
python "North-Korea-Flag/generate.py" --repo owner/repo --icon-url "https://example.com/icon.png"

# 显示 5 个贡献者
python "North-Korea-Flag/generate.py" --repo owner/repo --count 5

# 指定输出路径
python "North-Korea-Flag/generate.py" --repo owner/repo --output "./my-flag.svg"
```

运行要求：Python 3.7+（无需安装任何第三方包，只用标准库）。

---

## 常见问题

### SVG 显示的是占位符名字而不是真实贡献者

这说明 GitHub API 请求失败了。常见原因：
- **私有仓库**：Action 需要访问仓库的贡献者列表，私有仓库可能需要额外配置 `GITHUB_TOKEN`
- **API 频率限制**：未认证的 API 请求限制为每小时 60 次，频繁测试时请等待或使用 token

### 图标没有显示

- 确保 `icon-url` 是图片文件的直接链接（不是网页链接）
- URL 必须公开可访问（试试在无痕模式下能否打开）
- 支持的格式：PNG、JPG、SVG、WebP

### workflow 没有按计划自动运行

- GitHub 会在仓库 60 天无活动后自动禁用定时 workflow
- 推送任意 commit 即可重新启用
- 也可以随时通过 **Actions** → **Run workflow** 手动触发

### 头像显示不出来

- 头像从 `github.com/用户名.png` 加载，只有在 GitHub 上查看 SVG 时才能正常显示（README、Issue 等）
- 本地浏览器查看 SVG 时，头像可能因跨域限制无法加载

---

## 许可证

MIT
