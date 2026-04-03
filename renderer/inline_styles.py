# -*- coding: utf-8 -*-
"""内联样式应用器 - 将主题 CSS 作为内联样式应用到 HTML 元素"""

from bs4 import BeautifulSoup
from .image_grid import group_consecutive_images


# 标题内部行内元素的样式覆盖
# 确保标题内部的 strong/em/a/code 继承标题颜色
HEADING_INLINE_OVERRIDES = {
    'strong': 'font-weight: 700; color: inherit !important; background-color: transparent !important;',
    'em': 'font-style: italic; color: inherit !important;',
    'a': 'color: inherit !important; text-decoration: none; border-bottom: none;',
    'code': 'color: inherit !important; background-color: transparent !important; font-size: inherit; padding: 0;',
}

HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


def apply_inline_styles(html, styles):
    """将主题样式作为内联样式应用到 HTML 元素

    Args:
        html: HTML 字符串
        styles: 样式字典，键为元素名，值为 CSS 字符串

    Returns:
        应用了内联样式的 HTML 字符串
    """
    if not styles:
        return html

    soup = BeautifulSoup(html, 'html.parser')

    # 先处理图片分组
    group_consecutive_images(soup)

    # 应用样式到各元素
    for tag_name, css_string in styles.items():
        if tag_name == 'container':
            continue  # container 样式单独处理

        elements = soup.find_all(tag_name)
        for el in elements:
            # 如果元素已有 style 属性，合并样式
            existing_style = el.get('style', '')
            if existing_style:
                # 已有样式优先级更高，追加到主题样式之后
                el['style'] = css_string + '; ' + existing_style
            else:
                el['style'] = css_string

            # 处理标题内部的行内元素覆盖
            if tag_name in HEADING_TAGS:
                for inline_tag, override_css in HEADING_INLINE_OVERRIDES.items():
                    for inline_el in el.find_all(inline_tag):
                        inline_el['style'] = override_css

    # 处理 pre > code 的特殊情况：pre 内部的 code 不应用 code 样式
    for pre in soup.find_all('pre'):
        for code in pre.find_all('code'):
            # 移除 code 的独立样式，保留 pre 的样式
            if code.get('style'):
                code['style'] = 'background-color: transparent !important; padding: 0; border: none; font-size: inherit; color: inherit !important;'

    # 包裹到容器 div
    container_style = styles.get('container', '')
    if container_style:
        content_html = str(soup)
        wrapped = f'<div style="{container_style}">{content_html}</div>'
        return wrapped

    return str(soup)
