# -*- coding: utf-8 -*-
"""X Articles 导出器 - 将 HTML 转换为 X Articles 兼容的简洁格式"""

from bs4 import BeautifulSoup, NavigableString

# 允许的标签白名单
ALLOWED_TAGS = {'h2', 'h3', 'p', 'strong', 'em', 'del', 'a', 'ul', 'ol', 'li',
                'blockquote', 'br', 'b', 'i', 's'}


def _remap_headings(soup):
    """重映射标题层级: h1→h2, h4-h6→h3"""
    # h1 → h2
    for h1 in soup.find_all('h1'):
        h1.name = 'h2'

    # h4, h5, h6 → h3
    for tag_name in ['h4', 'h5', 'h6']:
        for tag in soup.find_all(tag_name):
            tag.name = 'h3'


def _code_to_blockquote(soup):
    """将代码块转换为 blockquote"""
    for pre in soup.find_all('pre'):
        code = pre.find('code')
        text = code.get_text() if code else pre.get_text()

        bq = soup.new_tag('blockquote')
        # 将代码文本按行分段
        lines = text.strip().split('\n')
        for i, line in enumerate(lines):
            p = soup.new_tag('p')
            p.string = line if line.strip() else '\u200b'  # 空行用零宽空格
            bq.append(p)

        pre.replace_with(bq)

    # 内联 code 标签解包
    for code in soup.find_all('code'):
        code.unwrap()


def _table_to_blockquote(soup):
    """将表格转换为 blockquote"""
    for table in soup.find_all('table'):
        bq = soup.new_tag('blockquote')

        # 提取表头
        headers = []
        for th in table.find_all('th'):
            headers.append(th.get_text(strip=True))

        if headers:
            p = soup.new_tag('p')
            p_strong = soup.new_tag('strong')
            p_strong.string = ' | '.join(headers)
            p.append(p_strong)
            bq.append(p)

        # 提取表格行
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if tds:
                p = soup.new_tag('p')
                p.string = ' | '.join(td.get_text(strip=True) for td in tds)
                bq.append(p)

        table.replace_with(bq)


def _images_to_placeholder(soup):
    """将图片替换为占位文本"""
    for img in soup.find_all('img'):
        alt = img.get('alt', '图片')
        p = soup.new_tag('p')
        em = soup.new_tag('em')
        em.string = f'[{alt}]'
        p.append(em)
        img.replace_with(p)

    # 移除图片网格容器
    for grid in soup.find_all('div', class_='image-grid'):
        grid.unwrap()


def _hr_to_separator(soup):
    """将 hr 替换为文本分隔符"""
    for hr in soup.find_all('hr'):
        p = soup.new_tag('p')
        p.string = '---'
        hr.replace_with(p)


def _remove_styles_and_classes(soup):
    """移除所有 style 和 class 属性"""
    for tag in soup.find_all(True):
        if tag.get('style'):
            del tag['style']
        if tag.get('class'):
            del tag['class']
        # 保留 a 标签的 href
        attrs_to_keep = set()
        if tag.name == 'a':
            attrs_to_keep.add('href')

        attrs_to_remove = [attr for attr in tag.attrs if attr not in attrs_to_keep]
        for attr in attrs_to_remove:
            del tag[attr]


def _unwrap_disallowed_tags(soup):
    """解包不在白名单中的标签"""
    for tag in soup.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()


def export_for_x_articles(html):
    """将 HTML 导出为 X Articles 兼容格式

    Args:
        html: 已应用样式的 HTML 字符串

    Returns:
        X Articles 兼容的简洁 HTML 字符串
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 依次进行转换
    _remap_headings(soup)
    _code_to_blockquote(soup)
    _table_to_blockquote(soup)
    _images_to_placeholder(soup)
    _hr_to_separator(soup)
    _remove_styles_and_classes(soup)
    _unwrap_disallowed_tags(soup)

    return str(soup)
