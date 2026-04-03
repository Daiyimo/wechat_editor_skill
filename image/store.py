# -*- coding: utf-8 -*-
"""图片存储器 - 基于文件系统 + JSON 元数据的图片管理"""

import os
import json
import uuid
import base64
import shutil
from pathlib import Path


class ImageStore:
    """图片存储管理器

    存储目录: ~/.wechat_editor/images/
    元数据文件: ~/.wechat_editor/images/metadata.json
    """

    def __init__(self, storage_dir=None):
        """初始化图片存储器

        Args:
            storage_dir: 自定义存储目录，默认为 ~/.wechat_editor/images/
        """
        if storage_dir:
            self.storage_dir = Path(storage_dir)
        else:
            self.storage_dir = Path.home() / '.wechat_editor' / 'images'

        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.storage_dir / 'metadata.json'
        self._load_metadata()

    def _load_metadata(self):
        """加载元数据"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.metadata = {}
        else:
            self.metadata = {}

    def _save_metadata(self):
        """保存元数据"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    @staticmethod
    def generate_image_id():
        """生成唯一图片 ID

        Returns:
            UUID 字符串
        """
        return str(uuid.uuid4())

    def save_image(self, source_path, image_id=None, metadata=None):
        """保存图片到存储

        Args:
            source_path: 源图片路径
            image_id: 图片 ID，默认自动生成
            metadata: 附加元数据字典

        Returns:
            图片 ID
        """
        if image_id is None:
            image_id = self.generate_image_id()

        source_path = Path(source_path)
        ext = source_path.suffix.lower()
        dest_path = self.storage_dir / f"{image_id}{ext}"

        # 复制文件
        shutil.copy2(str(source_path), str(dest_path))

        # 保存元数据
        self.metadata[image_id] = {
            'filename': source_path.name,
            'extension': ext,
            'size': os.path.getsize(str(dest_path)),
            'path': str(dest_path),
        }
        if metadata:
            self.metadata[image_id].update(metadata)

        self._save_metadata()
        return image_id

    def get_image_path(self, image_id):
        """获取图片文件路径

        Args:
            image_id: 图片 ID

        Returns:
            图片文件路径字符串，不存在则返回 None
        """
        info = self.metadata.get(image_id)
        if info and os.path.exists(info['path']):
            return info['path']
        return None

    def get_image_bytes(self, image_id):
        """获取图片二进制数据

        Args:
            image_id: 图片 ID

        Returns:
            bytes 数据，不存在则返回 None
        """
        path = self.get_image_path(image_id)
        if path:
            with open(path, 'rb') as f:
                return f.read()
        return None

    def get_image_base64(self, image_id):
        """获取图片的 Base64 编码

        Args:
            image_id: 图片 ID

        Returns:
            Base64 字符串，不存在则返回 None
        """
        data = self.get_image_bytes(image_id)
        if data:
            return base64.b64encode(data).decode('utf-8')
        return None

    def delete_image(self, image_id):
        """删除图片

        Args:
            image_id: 图片 ID

        Returns:
            是否删除成功
        """
        info = self.metadata.get(image_id)
        if info:
            path = info.get('path')
            if path and os.path.exists(path):
                os.remove(path)
            del self.metadata[image_id]
            self._save_metadata()
            return True
        return False

    def get_all_images(self):
        """获取所有图片信息

        Returns:
            元数据字典
        """
        return dict(self.metadata)

    def get_total_size(self):
        """获取存储总大小

        Returns:
            总字节数
        """
        total = 0
        for info in self.metadata.values():
            path = info.get('path')
            if path and os.path.exists(path):
                total += os.path.getsize(path)
        return total

    def clear_all(self):
        """清空所有图片"""
        for image_id in list(self.metadata.keys()):
            self.delete_image(image_id)
        self.metadata = {}
        self._save_metadata()
