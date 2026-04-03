# WeChat Editor - 微信公众号 Markdown 排版工具

将 Markdown 转换为适合微信公众号的富文本 HTML，支持 19 种精美样式主题。

## 快速开始

```bash
# 基本转换
python main.py article.md

# 指定样式
python main.py article.md -s wechat-tech

# 输出到文件
python main.py article.md -s wechat-anthropic -o output.html

# 微信兼容导出（图片转 Base64、Grid 转 Table 等）
python main.py article.md --wechat -o wechat_output.html

# 从标准输入读取
cat article.md | python main.py --from-stdin -s wechat-nyt

# 查看所有样式
python main.py --list-styles
```

## 19 种样式主题

| 样式键名 | 名称 | 风格特点 |
|---------|------|---------|
| `wechat-default` | 默认公众号风格 | 经典蓝色调，通用性强 |
| `latepost-depth` | 晚点风格 | 红色系，深度报道感 |
| `wechat-ft` | 金融时报 | 粉色纸底，专业财经 |
| `wechat-anthropic` | Claude | 暖橙渐变，AI 品牌感 |
| `wechat-tech` | 技术风格 | 蓝绿色系，代码友好 |
| `wechat-elegant` | 优雅简约 | 宋体排版，文学气质 |
| `wechat-deepread` | 深度阅读 | 黑白灰调，专注阅读 |
| `wechat-nyt` | 纽约时报 | Georgia 字体，新闻风 |
| `wechat-jonyive` | Jony Ive | 超轻字重，Apple 设计 |
| `wechat-medium` | Medium 长文 | 经典博客，阅读体验 |
| `wechat-apple` | Apple 极简 | 灰色调，极致简洁 |
| `kenya-emptiness` | 原研哉·空 | 超大留白，禅意设计 |
| `hische-editorial` | Hische·编辑部 | 红黑色系，编辑排版 |
| `ando-concrete` | 安藤·清水 | 灰色调，建筑质感 |
| `gaudi-organic` | 高迪·有机 | 多彩渐变，有机形态 |
| `guardian` | Guardian 卫报 | 深蓝黄色，新闻报道 |
| `nikkei` | Nikkei 日経 | 紧凑排版，日式商务 |
| `warm-docs` | 焦橙文档 | 暖色调，技术文档 |
| `lemonde` | Le Monde 世界报 | 法式排版，衬线字体 |

## 核心功能

- **Markdown 渲染**: 支持表格、围栏代码、代码高亮、有序列表
- **macOS 代码装饰**: 代码块自动添加红黄绿三色圆点
- **图片网格**: 连续图片自动排列为 Grid 布局
- **图片压缩**: 最大 1920px，JPEG 85% 质量
- **图片存储**: 本地文件系统 + JSON 元数据管理
- **微信导出**: Grid→Table、图片→Base64、代码简化
- **X Articles 导出**: 标题重映射、标签白名单过滤

## 项目结构

```
skill/
├── main.py                    # CLI 入口
├── styles/themes.py           # 样式主题配置
├── renderer/
│   ├── markdown_renderer.py   # Markdown→HTML
│   ├── inline_styles.py       # 内联样式应用
│   └── image_grid.py          # 图片网格布局
├── image/
│   ├── compressor.py          # 图片压缩
│   └── store.py               # 图片存储
├── export/
│   ├── wechat_export.py       # 微信导出
│   └── x_articles_export.py   # X Articles 导出
└── utils/helpers.py           # 工具函数
```

## 依赖安装

```bash
pip install markdown beautifulsoup4 Pillow
```

## 版本

v2.0.0 - Python 重写版本
