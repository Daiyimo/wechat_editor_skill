# -*- coding: utf-8 -*-
"""Markdown 渲染器 - 将 Markdown 转换为 HTML"""

import re
import markdown


def preprocess_markdown(content):
    """预处理 Markdown 内容，修复格式问题"""
    # 标准化水平分割线
    content = re.sub(r'^(\s*)([-*_])\s*\2\s*\2[\s\2]*$', r'\1---', content, flags=re.MULTILINE)

    # 修复加粗跨段落断裂的问题
    # 处理未闭合的 ** 对
    lines = content.split('\n')
    result_lines = []
    open_bold = False
    for line in lines:
        count = line.count('**')
        if open_bold and count % 2 == 1:
            # 闭合加粗
            open_bold = False
        elif not open_bold and count % 2 == 1:
            open_bold = True
        result_lines.append(line)

    return '\n'.join(result_lines)


def _add_macos_code_decoration(html):
    """为代码块添加 macOS 风格的三色圆点装饰"""
    macos_dots = (
        '<div style="display: flex; align-items: center; gap: 6px; padding: 10px 12px; '
        'background: #2a2c33; border-bottom: 1px solid #1e1f24;">'
        '<span style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f56;"></span>'
        '<span style="width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e;"></span>'
        '<span style="width: 12px; height: 12px; border-radius: 50%; background: #27c93f;"></span>'
        '</div>'
    )

    # 匹配 <pre> 标签并在其内容前添加装饰
    def replace_pre(match):
        pre_tag = match.group(0)
        # 在 <pre> 开标签之后插入装饰
        pre_open_end = pre_tag.find('>') + 1
        return pre_tag[:pre_open_end] + macos_dots + pre_tag[pre_open_end:]

    html = re.sub(r'<pre[^>]*>.*?</pre>', replace_pre, html, flags=re.DOTALL)
    return html


def render_markdown(md_text):
    """将 Markdown 文本渲染为 HTML

    Args:
        md_text: Markdown 格式的文本

    Returns:
        渲染后的 HTML 字符串
    """
    # 预处理
    md_text = preprocess_markdown(md_text)

    # 配置 Markdown 扩展
    extensions = [
        'tables',
        'fenced_code',
        'codehilite',
        'sane_lists',
    ]

    extension_configs = {
        'codehilite': {
            'css_class': 'highlight',
            'guess_lang': True,
            'noclasses': True,
        }
    }

    # 渲染 Markdown
    html = markdown.markdown(
        md_text,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format='html5'
    )

    # 添加 macOS 代码块装饰
    html = _add_macos_code_decoration(html)

    return html
