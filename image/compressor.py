# -*- coding: utf-8 -*-
"""图片压缩器 - 使用 Pillow 压缩图片"""

import os
from PIL import Image


class ImageCompressor:
    """图片压缩器"""

    MAX_DIMENSION = 1920
    QUALITY = 85
    SKIP_FORMATS = {'.gif', '.svg'}

    def compress(self, input_path, output_path=None):
        """压缩图片文件

        Args:
            input_path: 输入图片路径
            output_path: 输出图片路径，默认为 None（覆盖原文件）

        Returns:
            dict: 包含压缩结果信息的字典
        """
        if output_path is None:
            output_path = input_path

        ext = os.path.splitext(input_path)[1].lower()

        # 跳过 GIF 和 SVG
        if ext in self.SKIP_FORMATS:
            return {
                'skipped': True,
                'reason': f'Skipped {ext} format',
                'original_size': os.path.getsize(input_path),
                'compressed_size': os.path.getsize(input_path),
            }

        original_size = os.path.getsize(input_path)

        try:
            img = Image.open(input_path)

            # 转换 RGBA 为 RGB（JPEG 不支持 alpha）
            if img.mode in ('RGBA', 'LA', 'P') and ext != '.png':
                img = img.convert('RGB')

            # 限制最大尺寸
            width, height = img.size
            if width > self.MAX_DIMENSION or height > self.MAX_DIMENSION:
                ratio = min(self.MAX_DIMENSION / width, self.MAX_DIMENSION / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # 决定输出格式
            if ext == '.png':
                # PNG 保持 PNG
                img.save(output_path, 'PNG', optimize=True)
            else:
                # 其他格式转 JPEG
                if not output_path.lower().endswith(('.jpg', '.jpeg')):
                    output_path = os.path.splitext(output_path)[0] + '.jpg'
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=self.QUALITY, optimize=True)

            compressed_size = os.path.getsize(output_path)

            # 如果压缩后更大，使用原文件
            if compressed_size >= original_size and input_path != output_path:
                import shutil
                shutil.copy2(input_path, output_path)
                compressed_size = original_size

            return {
                'skipped': False,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'saved': original_size - compressed_size,
                'ratio': (1 - compressed_size / original_size) * 100 if original_size > 0 else 0,
                'output_path': output_path,
            }

        except Exception as e:
            return {
                'skipped': True,
                'reason': str(e),
                'original_size': original_size,
                'compressed_size': original_size,
            }

    @staticmethod
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
