# -*- coding: utf-8 -*-
"""微信公众号 Markdown 排版工具 - 主入口"""

import sys
import os

# 确保能找到本项目的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse

from styles.themes import STYLES, get_style, list_styles
from renderer.markdown_renderer import render_markdown
from renderer.inline_styles import apply_inline_styles
from export.wechat_export import export_for_wechat
from export.x_articles_export import export_for_x_articles
from image.store import ImageStore


def process_markdown(md_text, style_key='wechat-default', export_mode=None, image_store=None):
    """完整的 Markdown 处理流水线

    Args:
        md_text: Markdown 文本
        style_key: 样式主题键名
        export_mode: 导出模式 ('wechat', 'x-articles', None)
        image_store: ImageStore 实例（可选）

    Returns:
        处理后的 HTML 字符串
    """
    # 1. 获取样式
    style = get_style(style_key)
    if not style:
        print(f"警告: 未找到样式 '{style_key}'，使用默认样式", file=sys.stderr)
        style = get_style('wechat-default')

    styles = style['styles']

    # 2. 渲染 Markdown 为 HTML
    html = render_markdown(md_text)

    # 3. 应用内联样式
    html = apply_inline_styles(html, styles)

    # 4. 导出处理
    if export_mode == 'wechat':
        html = export_for_wechat(html, image_store=image_store, style_config=styles)
    elif export_mode == 'x-articles':
        html = export_for_x_articles(html)

    return html


def main():
    """CLI 主入口"""
    parser = argparse.ArgumentParser(
        description='微信公众号 Markdown 排版工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py article.md
  python main.py article.md -s wechat-tech -o output.html
  python main.py article.md --wechat
  python main.py --from-stdin -s wechat-anthropic
  python main.py --list-styles
        """
    )

    parser.add_argument('input', nargs='?', help='输入 Markdown 文件路径')
    parser.add_argument('-s', '--style', default='wechat-default',
                        help='样式主题 (默认: wechat-default)')
    parser.add_argument('-o', '--output', help='输出 HTML 文件路径')
    parser.add_argument('--wechat', action='store_true',
                        help='导出为微信公众号兼容格式')
    parser.add_argument('--x-articles', action='store_true',
                        help='导出为 X Articles 兼容格式')
    parser.add_argument('--list-styles', action='store_true',
                        help='列出所有可用样式')
    parser.add_argument('--from-stdin', action='store_true',
                        help='从标准输入读取 Markdown')
    parser.add_argument('--image-dir', help='图片存储目录')

    args = parser.parse_args()

    # 列出样式
    if args.list_styles:
        styles = list_styles()
        print("可用样式主题:")
        print("-" * 40)
        for key, name in styles.items():
            print(f"  {key:<25} {name}")
        return

    # 读取输入
    if args.from_stdin:
        md_text = sys.stdin.read()
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            md_text = f.read()
    else:
        parser.print_help()
        sys.exit(1)

    # 确定导出模式
    export_mode = None
    if args.wechat:
        export_mode = 'wechat'
    elif args.x_articles:
        export_mode = 'x-articles'

    # 图片存储
    image_store = None
    if args.image_dir:
        image_store = ImageStore(storage_dir=args.image_dir)

    # 处理
    html = process_markdown(md_text, args.style, export_mode, image_store)

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"已输出到: {args.output}", file=sys.stderr)
    else:
        # Windows 编码修复
        sys.stdout.buffer.write(html.encode('utf-8'))


if __name__ == '__main__':
    main()
