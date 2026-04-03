# -*- coding: utf-8 -*-
"""工具函数"""

import re
import html as html_module


def extract_background_color(style_string):
    """从 CSS 样式字符串中提取 background-color 值

    Args:
        style_string: CSS 样式字符串

    Returns:
        背景颜色值字符串，未找到则返回 None
    """
    if not style_string:
        return None

    # 匹配 background-color: xxx
    match = re.search(r'background-color:\s*([^;!]+)', style_string)
    if match:
        return match.group(1).strip()

    # 匹配简写 background: xxx（仅颜色值）
    match = re.search(r'background:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|[a-zA-Z]+)', style_string)
    if match:
        return match.group(1).strip()

    return None


def format_size(size_bytes):
    """格式化文件大小为人类可读格式

    Args:
        size_bytes: 字节数

    Returns:
        格式化后的字符串
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def escape_html(text):
    """转义 HTML 特殊字符

    Args:
        text: 原始文本

    Returns:
        转义后的安全文本
    """
    return html_module.escape(text)
