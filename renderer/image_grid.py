# -*- coding: utf-8 -*-
"""图片网格布局 - 将连续图片分组为 CSS Grid 布局"""

from bs4 import BeautifulSoup, Tag


def _get_grid_columns(count):
    """根据图片数量决定网格列数

    Args:
        count: 图片数量

    Returns:
        列数
    """
    if count == 1:
        return 1
    elif count == 2:
        return 2
    elif count == 3:
        return 3
    elif count == 4:
        return 2  # 2x2 布局
    else:
        return 3  # 5+ 使用 3 列


def group_consecutive_images(soup):
    """将连续的 img 元素分组为 CSS Grid 布局

    直接修改传入的 BeautifulSoup 对象。

    Args:
        soup: BeautifulSoup 对象
    """
    # 查找所有顶层 img 和包含单个 img 的 p 标签
    body_elements = list(soup.children) if soup.name == '[document]' else list(soup.children)

    groups = []
    current_group = []

    for el in body_elements:
        is_image = False

        if isinstance(el, Tag):
            if el.name == 'img':
                is_image = True
            elif el.name == 'p':
                # 检查 p 标签是否只包含一个 img
                children = [c for c in el.children if isinstance(c, Tag) or (isinstance(c, str) and c.strip())]
                img_children = [c for c in children if isinstance(c, Tag) and c.name == 'img']
                if len(img_children) == 1 and len(children) == 1:
                    is_image = True

        if is_image:
            current_group.append(el)
        else:
            if len(current_group) >= 2:
                groups.append(list(current_group))
            current_group = []

    # 处理末尾的组
    if len(current_group) >= 2:
        groups.append(list(current_group))

    # 对每个组创建 grid 容器
    for group in groups:
        count = len(group)
        columns = _get_grid_columns(count)

        # 创建 grid 容器
        grid_div = soup.new_tag('div')
        grid_div['class'] = 'image-grid'
        grid_div['data-image-count'] = str(count)
        grid_div['data-columns'] = str(columns)
        grid_div['style'] = (
            f'display: grid; grid-template-columns: repeat({columns}, 1fr); '
            f'gap: 8px; margin: 20px 0;'
        )

        # 在第一个元素之前插入 grid 容器
        first_el = group[0]
        first_el.insert_before(grid_div)

        # 将所有图片移入 grid 容器
        for el in group:
            # 如果是 p>img，提取 img
            if isinstance(el, Tag) and el.name == 'p':
                img = el.find('img')
                if img:
                    img.extract()
                    # 调整图片样式适应网格
                    img['style'] = 'width: 100%; height: auto; object-fit: cover; border-radius: 4px;'
                    grid_div.append(img)
                el.decompose()
            elif isinstance(el, Tag) and el.name == 'img':
                el.extract()
                el['style'] = 'width: 100%; height: auto; object-fit: cover; border-radius: 4px;'
                grid_div.append(el)

    return soup
