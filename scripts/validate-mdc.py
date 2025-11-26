#!/usr/bin/env python3
"""
MDC 格式验证脚本

验证 .mdc 文件的 frontmatter 格式是否正确。

用法:
    python scripts/validate-mdc.py [文件或目录]
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import yaml
except ImportError:
    print("错误: 需要安装 PyYAML 库")
    print("安装命令: pip install pyyaml 或 uv add pyyaml")
    sys.exit(1)


class MDCValidator:
    """MDC 格式验证器"""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_file(self, file_path: Path) -> Tuple[bool, List[str], List[str]]:
        """
        验证单个 MDC 文件

        Returns:
            (是否有效, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []

        if not file_path.exists():
            self.errors.append(f"文件不存在: {file_path}")
            return False, self.errors, self.warnings

        if file_path.suffix != ".mdc":
            self.errors.append(f"文件扩展名不是 .mdc: {file_path}")
            return False, self.errors, self.warnings

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(f"读取文件失败: {e}")
            return False, self.errors, self.warnings

        # 检查是否有 frontmatter
        if not content.startswith("---"):
            self.errors.append("缺少 frontmatter（文件应以 '---' 开头）")
            return False, self.errors, self.warnings

        # 解析 frontmatter
        try:
            parts = content.split("---", 2)
            if len(parts) < 3:
                self.errors.append("frontmatter 格式错误（应包含两个 '---' 分隔符）")
                return False, self.errors, self.warnings

            frontmatter_yaml = parts[1].strip()
            metadata = yaml.safe_load(frontmatter_yaml)

            if not isinstance(metadata, dict):
                self.errors.append("frontmatter 必须是 YAML 字典格式")
                return False, self.errors, self.warnings

        except yaml.YAMLError as e:
            self.errors.append(f"YAML 解析错误: {e}")
            return False, self.errors, self.warnings

        # 验证必需字段
        required_fields = ["description", "globs", "alwaysApply"]
        for field in required_fields:
            if field not in metadata:
                self.errors.append(f"缺少必需字段: {field}")

        # 验证字段类型和值
        if "description" in metadata:
            if not isinstance(metadata["description"], str):
                self.errors.append("description 必须是字符串")
            elif len(metadata["description"]) > 200:
                self.warnings.append("description 超过 200 字符，建议缩短")

        if "globs" in metadata:
            if not isinstance(metadata["globs"], list):
                self.errors.append("globs 必须是数组")
            elif len(metadata["globs"]) == 0:
                self.warnings.append("globs 为空数组")

        if "alwaysApply" in metadata:
            if not isinstance(metadata["alwaysApply"], bool):
                self.errors.append("alwaysApply 必须是布尔值")

        if "tags" in metadata:
            if not isinstance(metadata["tags"], list):
                self.warnings.append("tags 应该是数组")
            elif len(metadata["tags"]) == 0:
                self.warnings.append("tags 为空数组")

        if "version" in metadata:
            if not isinstance(metadata["version"], str):
                self.warnings.append("version 应该是字符串")
            else:
                # 简单的版本号格式检查
                import re
                if not re.match(r"^\d+\.\d+\.\d+$", metadata["version"]):
                    self.warnings.append(f"version 格式可能不符合 SemVer: {metadata['version']}")

        # 检查内容部分
        content_part = parts[2].strip() if len(parts) > 2 else ""
        if not content_part:
            self.warnings.append("内容部分为空")

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def validate_directory(self, directory: Path) -> Tuple[int, int]:
        """
        验证目录中的所有 .mdc 文件

        Returns:
            (有效文件数, 无效文件数)
        """
        mdc_files = list(directory.rglob("*.mdc"))
        valid_count = 0
        invalid_count = 0

        for mdc_file in mdc_files:
            is_valid, errors, warnings = self.validate_file(mdc_file)
            if is_valid:
                valid_count += 1
                if warnings:
                    print(f"✓ {mdc_file} (有 {len(warnings)} 个警告)")
                    for warning in warnings:
                        print(f"  警告: {warning}")
            else:
                invalid_count += 1
                print(f"✗ {mdc_file}")
                for error in errors:
                    print(f"  错误: {error}")
                if warnings:
                    for warning in warnings:
                        print(f"  警告: {warning}")

        return valid_count, invalid_count


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="验证 .mdc 文件的 frontmatter 格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 验证单个文件
  python scripts/validate-mdc.py .cursor/rules/meta-rules.mdc

  # 验证整个目录
  python scripts/validate-mdc.py .cursor/rules/
        """,
    )

    parser.add_argument(
        "path",
        type=str,
        help="要验证的文件或目录路径",
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"错误: 路径不存在: {path}")
        return 1

    validator = MDCValidator()

    if path.is_file():
        # 验证单个文件
        is_valid, errors, warnings = validator.validate_file(path)
        if is_valid:
            print(f"✓ {path} 验证通过")
            if warnings:
                for warning in warnings:
                    print(f"  警告: {warning}")
            return 0
        else:
            print(f"✗ {path} 验证失败")
            for error in errors:
                print(f"  错误: {error}")
            if warnings:
                for warning in warnings:
                    print(f"  警告: {warning}")
            return 1
    elif path.is_dir():
        # 验证目录
        print(f"正在验证目录: {path}")
        valid_count, invalid_count = validator.validate_directory(path)
        print(f"\n验证完成: 有效 {valid_count} 个, 无效 {invalid_count} 个")
        return 0 if invalid_count == 0 else 1
    else:
        print(f"错误: 无效的路径类型: {path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

