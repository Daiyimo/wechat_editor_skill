# -*- coding: utf-8 -*-
"""微信公众号导出器 - 将 HTML 转换为微信兼容格式"""

import re
import os
import base64
import mimetypes
from bs4 import BeautifulSoup
from utils.helpers import extract_background_color


def _grid_to_table(soup):
    """将 CSS Grid 图片布局转换为 table 布局（微信兼容）"""
    for grid_div in soup.find_all('div', class_='image-grid'):
        columns = int(grid_div.get('data-columns', 2))
        images = grid_div.find_all('img')

        if not images:
            continue

        table = soup.new_tag('table')
        table['style'] = 'width: 100%; border-collapse: collapse; margin: 20px 0;'

        row = None
        for i, img in enumerate(images):
            if i % columns == 0:
                row = soup.new_tag('tr')
                table.append(row)

            td = soup.new_tag('td')
            td['style'] = f'width: {100 // columns}%; padding: 4px; vertical-align: top;'
            img_copy = img.__copy__() if hasattr(img, '__copy__') else soup.new_tag('img', src=img.get('src', ''))
            for attr in img.attrs:
                img_copy[attr] = img[attr]
            img_copy['style'] = 'width: 100%; height: auto; display: block;'
            td.append(img_copy)
            row.append(td)

        grid_div.replace_with(table)


def _images_to_base64(soup, image_store=None):
    """将图片转换为 Base64 内嵌格式"""
    for img in soup.find_all('img'):
        src = img.get('src', '')

        # 已经是 base64 的跳过
        if src.startswith('data:'):
            continue

        image_data = None
        mime_type = 'image/jpeg'

        # 尝试从 image_store 获取
        if image_store and not src.startswith(('http://', 'https://')):
            # 可能是 image_id
            data = image_store.get_image_bytes(src)
            if data:
                image_data = data
                path = image_store.get_image_path(src)
                if path:
                    mime_type = mimetypes.guess_type(path)[0] or 'image/jpeg'

        # 尝试从本地文件读取
        if image_data is None and os.path.isfile(src):
            with open(src, 'rb') as f:
                image_data = f.read()
            mime_type = mimetypes.guess_type(src)[0] or 'image/jpeg'

        if image_data:
            b64 = base64.b64encode(image_data).decode('utf-8')
            img['src'] = f'data:{mime_type};base64,{b64}'


def _wrap_sections(soup):
    """用 section 标签包裹内容块（微信编辑器兼容性）"""
    # 微信编辑器对 section 标签支持更好
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                               'blockquote', 'ul', 'ol', 'table', 'pre']):
        section = soup.new_tag('section')
        tag.wrap(section)


def _simplify_code_blocks(soup):
    """简化代码块以提高微信兼容性"""
    for pre in soup.find_all('pre'):
        # 保留基本样式，去除可能不兼容的属性
        style = pre.get('style', '')
        # 确保有 overflow 和基本样式
        if 'white-space' not in style:
            pre['style'] = style + '; white-space: pre-wrap; word-wrap: break-word;'


def _flatten_lists(soup):
    """展平嵌套列表以提高微信兼容性"""
    for ul in soup.find_all(['ul', 'ol']):
        # 确保列表项有基本样式
        for li in ul.find_all('li', recursive=False):
            if not li.get('style'):
                li['style'] = 'margin: 8px 0;'


def _fix_blockquote_dark_mode(soup, style_config=None):
    """修复 blockquote 在微信深色模式下的显示问题"""
    bg_color = '#f8f8f8'
    if style_config and 'blockquote' in style_config:
        extracted = extract_background_color(style_config['blockquote'])
        if extracted:
            bg_color = extracted

    for bq in soup.find_all('blockquote'):
        style = bq.get('style', '')
        if 'background' not in style:
            bq['style'] = style + f'; background-color: {bg_color} !important;'


def export_for_wechat(html, image_store=None, style_config=None):
    """将 HTML 导出为微信公众号兼容格式

    Args:
        html: 已应用样式的 HTML 字符串
        image_store: ImageStore 实例（可选）
        style_config: 样式配置字典（可选）

    Returns:
        微信兼容的 HTML 字符串
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 依次进行转换
    _grid_to_table(soup)
    _images_to_base64(soup, image_store)
    _simplify_code_blocks(soup)
    _flatten_lists(soup)
    _fix_blockquote_dark_mode(soup, style_config)
    _wrap_sections(soup)

    return str(soup)
