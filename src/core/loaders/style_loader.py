"""
该模块用于加载样式文件
"""

from pathlib import Path


class StyleLoader:
    def __init__(self, style_name: str):
        """
        初始化样式加载器

        Args:
            style_name: 样式文件名称，例如 'main.qss' 或 'dark.qss'
        """
        # 获取项目根目录
        self.root_dir = Path(__file__).parent.parent.parent
        # 构建样式文件的完整路径
        self.style_path = self.root_dir / "ui" / "styles" / style_name

    def load_style(self) -> str:
        """
        加载样式文件内容

        Returns:
            str: 样式文件的内容

        Raises:
            FileNotFoundError: 当样式文件不存在时抛出
        """
        if not self.style_path.exists():
            raise FileNotFoundError(f"样式文件未找到: {self.style_path}")

        with open(self.style_path, "r", encoding="utf-8") as file:
            return file.read()

    @classmethod
    def load_all_styles(cls) -> str:
        """
        加载 styles 目录下的所有 QSS 文件并合并

        Returns:
            str: 合并后的样式内容
        """
        root_dir = Path(__file__).parent.parent.parent.parent
        styles_dir = root_dir / "ui" / "styles"

        all_styles = []
        for qss_file in styles_dir.glob("*.qss"):
            with open(qss_file, "r", encoding="utf-8") as file:
                all_styles.append(file.read())

        return "\n".join(all_styles)
