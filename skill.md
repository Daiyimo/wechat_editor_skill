---
name: wechat-editor
description: >
  微信公众号 Markdown 排版工具。将 Markdown 转换为适合微信公众号的富文本 HTML。
  支持 19 种精美样式主题、图片压缩、智能排版、一键导出。
  触发条件：当用户要求排版微信公众号文章、转换 Markdown 为微信格式、
  或提到「公众号排版」「公众号编辑」「微信排版」时使用。
  TRIGGER when: user mentions 公众号/WeChat article formatting, Markdown to WeChat,
  or wants to convert markdown to styled HTML for WeChat Official Accounts.
version: "2.1.0"
author: "v_cxyucai"
keywords: [wechat, markdown, editor, 公众号, 排版, 微信]
---

# 微信公众号 Markdown 排版工具

将标准 Markdown 文本转换为适合微信公众号的富文本 HTML 格式，支持 19 种精心设计的样式主题。

---

## 交互流程（必须遵循）

当此 Skill 被触发时，Claude **必须**按以下步骤与用户交互，而不是直接执行：

### 第一步：确认输入来源

使用 `AskUserQuestion` 询问用户 Markdown 内容的来源：

- **粘贴内容** — 用户直接在对话中粘贴 Markdown 文本
- **指定文件** — 用户提供一个 `.md` 文件路径
- **当前目录查找** — 自动扫描当前目录下的 `.md` 文件供用户选择

> 如果用户在触发时已经明确提供了 Markdown 内容或文件路径，跳过此步。

### 第二步：选择样式主题

使用 `AskUserQuestion` 让用户从以下 **四大系列** 中选择风格：

**经典公众号系列**
- `wechat-default` — 默认公众号风格（蓝色调，适合大多数文章）
- `wechat-tech` — 技术风格（绿色左边框标题，代码友好）
- `wechat-elegant` — 优雅简约（宋体，居中标题，文艺范）
- `wechat-deepread` — 深度阅读（黑白极简，专注内容）

**传统媒体系列**
- `latepost-depth` — 晚点风格（红色强调，新闻感）
- `wechat-nyt` — 纽约时报（经典报纸排版，Georgia 字体）
- `wechat-ft` — 金融时报（米色背景，酒红色调，专业感）
- `guardian` — Guardian 卫报（深蓝+黄色高亮，英国范）
- `nikkei` — Nikkei 日経（紧凑日式排版，红色重点）
- `lemonde` — Le Monde 世界报（法式优雅，衬线字体）

**设计师系列**
- `wechat-jonyive` — Jony Ive（超轻字重，苹果设计哲学）
- `wechat-apple` — Apple 极简（SF Pro 字体，灰色正文）
- `kenya-emptiness` — 原研哉·空（大量留白，禅意设计）
- `hische-editorial` — Hische·编辑部（红色装饰，杂志感）
- `ando-concrete` — 安藤·清水（清水混凝土质感，建筑极简）
- `gaudi-organic` — 高迪·有机（彩色渐变，曲线有机形态）

**现代数字系列**
- `wechat-medium` — Medium 长文（现代博客排版）
- `wechat-anthropic` — Claude（Anthropic 品牌色，温暖渐变）（推荐）
- `warm-docs` — 焦橙文档（暖色技术文档风格）

提问时应按系列分组展示，并用简短描述帮助用户决策。如果用户不确定，推荐 `wechat-anthropic`（Claude 风格）。

### 第三步：选择导出格式

使用 `AskUserQuestion` 询问导出格式：

- **微信公众号**（推荐）— 完整兼容微信编辑器（Grid→Table、图片 Base64、深色模式适配）
- **X Articles** — 适配 Twitter/X 长文格式（标签白名单、语义化 HTML）
- **原始 HTML** — 不做兼容处理，保留 CSS Grid 等现代特性

### 第四步：选择输出方式

使用 `AskUserQuestion` 询问输出方式：

- **保存到文件** — 输出为 `.html` 文件（需指定或自动生成文件名）
- **直接显示** — 在对话中展示 HTML 代码（适合短文）
- **复制到剪贴板** — 自动复制到系统剪贴板（如果支持）

### 第五步：执行转换

根据用户选择，组装并执行命令：

```bash
cd /e/project/wechat_editor/skill
python main.py <input> -s <style> [--wechat|--x-articles] [-o <output>]
```

### 第六步：确认结果

执行完成后：
1. 告知用户输出文件的位置和大小
2. 询问是否需要**换一种样式重新生成**
3. 询问是否需要**预览效果**（用浏览器打开 HTML）

---

## 快捷模式

如果用户在一句话中已经提供了足够信息，可以跳过部分交互步骤。例如：

- "用 Claude 风格把 article.md 排版成微信公众号格式" → 跳过步骤 1-3，直接执行
- "帮我排版这段文字" + 粘贴的 Markdown → 只需问步骤 2（选样式）
- "/wechat-editor article.md" → 使用默认样式和微信格式，只需确认

---

## CLI 命令参考

```bash
# 基本渲染
python main.py article.md

# 指定样式
python main.py article.md -s wechat-anthropic

# 微信兼容格式
python main.py article.md --wechat -o output.html

# X Articles 格式
python main.py article.md --x-articles -o output.html

# 列出所有样式
python main.py --list-styles

# 标准输入
echo "# Hello" | python main.py --from-stdin -s wechat-tech

# 指定图片目录
python main.py article.md --image-dir ./images
```

## Python API

```python
from main import process_markdown

html = process_markdown(
    md_text="# 标题\n\n正文...",
    style_key="wechat-anthropic",
    export_mode="wechat"  # 'raw' | 'wechat' | 'x-articles'
)
```

---

## 项目结构

```
skill/
├── skill.md              # Skill 定义（本文件）
├── README.md             # 项目文档
├── main.py               # CLI 入口 + 处理流水线
├── styles/
│   └── themes.py         # 19 种样式主题配置
├── renderer/
│   ├── markdown_renderer.py  # Markdown → HTML
│   ├── inline_styles.py      # 内联样式应用
│   └── image_grid.py         # 图片网格布局
├── image/
│   ├── compressor.py     # 图片压缩（Pillow）
│   └── store.py          # 图片存储管理
├── export/
│   ├── wechat_export.py  # 微信公众号格式
│   └── x_articles_export.py  # X Articles 格式
└── utils/
    └── helpers.py        # 工具函数
```

## 依赖

```
markdown, pygments, beautifulsoup4, Pillow, lxml
```
