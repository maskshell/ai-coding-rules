#!/usr/bin/env python3
"""
MDC 格式迁移脚本

将 .md 规则文件转换为 .mdc 格式，添加 frontmatter 元数据。

用法:
    python scripts/migrate-to-mdc.py [文件或目录] [选项]

选项:
    --dry-run: 仅显示将要执行的操作，不实际修改文件
    --backup: （已废弃）不再创建备份文件
    --force: 强制覆盖已存在的 .mdc 文件

注意:
    - 转换后会删除原始 .md 文件（不保留兼容）
    - 不创建备份文件
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("错误: 需要安装 PyYAML 库")
    print("安装命令: pip install pyyaml 或 uv add pyyaml")
    sys.exit(1)


class MDCMigrator:
    """MDC 格式迁移器"""

    def __init__(
        self, dry_run: bool = False, backup: bool = False, force: bool = False
    ):
        self.dry_run = dry_run
        self.backup = backup
        self.force = force

    def infer_metadata(self, file_path: Path, content: str) -> Dict[str, any]:
        """
        根据文件路径和内容推断 frontmatter 元数据

        Args:
            file_path: 文件路径
            content: 文件内容

        Returns:
            frontmatter 字典
        """
        metadata: Dict[str, any] = {}

        # 1. 推断 description
        metadata["description"] = self._infer_description(file_path, content)

        # 2. 推断 globs
        metadata["globs"] = self._infer_globs(file_path, content)

        # 3. 推断 alwaysApply
        metadata["alwaysApply"] = self._infer_always_apply(file_path, content)

        # 4. 推断 tags
        metadata["tags"] = self._infer_tags(file_path, content)

        # 5. 可选字段
        metadata["version"] = "1.0.0"
        metadata["author"] = "ai-coding-rules-team"

        return metadata

    def _infer_description(self, file_path: Path, content: str) -> str:
        """推断规则描述"""
        # 从文件名提取
        filename = file_path.stem
        # 移除数字前缀
        name = re.sub(r"^\d+-", "", filename)
        # 转换为描述性文本
        name = name.replace("-", " ").title()

        # 从内容第一行提取标题
        lines = content.strip().split("\n")
        if lines and lines[0].startswith("#"):
            title = lines[0].lstrip("#").strip()
            if title:
                return title

        # 默认描述
        return f"{name} 规则"

    def _infer_globs(self, file_path: Path, content: str) -> List[str]:
        """推断文件匹配模式"""
        filename = file_path.stem.lower()

        # 根据文件名推断
        if "python" in filename or "fastapi" in filename:
            return ["**/*.py"]
        elif "react" in filename:
            return ["**/*.tsx", "**/*.jsx"]
        elif "vue" in filename:
            return ["**/*.vue"]
        elif "typescript" in filename or "ts" in filename:
            return ["**/*.ts", "**/*.tsx"]
        elif "javascript" in filename or "js" in filename:
            return ["**/*.js", "**/*.jsx"]
        elif "general" in filename or "meta" in filename:
            return ["**/*"]
        elif "testing" in filename or "test" in filename:
            return ["**/*test*.py", "**/*test*.ts", "**/*test*.js"]
        elif "security" in filename:
            return ["**/*"]
        else:
            # 默认：所有文件
            return ["**/*"]

    def _infer_always_apply(self, file_path: Path, content: str) -> bool:
        """推断是否总是应用"""
        filename = file_path.stem.lower()

        # 通用规则、元规则、安全规则通常总是应用
        if any(keyword in filename for keyword in ["general", "meta", "security"]):
            return True

        # 特定语言/框架规则通常按需应用
        if any(
            keyword in filename
            for keyword in [
                "python",
                "react",
                "vue",
                "typescript",
                "javascript",
                "fastapi",
            ]
        ):
            return False

        # 默认：按需应用
        return False

    def _infer_tags(self, file_path: Path, content: str) -> List[str]:
        """推断标签"""
        tags: List[str] = []
        filename = file_path.stem.lower()
        content_lower = content.lower()

        # 语言标签
        if "python" in filename or "python" in content_lower:
            tags.append("python")
        if (
            "typescript" in filename
            or "typescript" in content_lower
            or "ts" in filename
        ):
            tags.append("typescript")
        if (
            "javascript" in filename
            or "javascript" in content_lower
            or "js" in filename
        ):
            tags.append("javascript")

        # 框架标签
        if "react" in filename or "react" in content_lower:
            tags.append("react")
        if "vue" in filename or "vue" in content_lower:
            tags.append("vue")
        if "fastapi" in filename or "fastapi" in content_lower:
            tags.append("fastapi")

        # 功能标签
        if "test" in filename or "testing" in filename:
            tags.append("testing")
        if "security" in filename or "security" in content_lower:
            tags.append("security")
        if "general" in filename or "meta" in filename:
            tags.append("general")
        if "coding-standards" in filename or "coding-standards" in content_lower:
            tags.append("coding-standards")

        # 如果没有标签，添加通用标签
        if not tags:
            tags.append("general")

        return tags

    def read_file(self, file_path: Path) -> str:
        """读取文件内容"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise Exception(f"读取文件失败: {file_path}: {e}")

    def write_file(self, file_path: Path, content: str) -> None:
        """写入文件内容"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"写入文件失败: {file_path}: {e}")

    def create_backup(self, file_path: Path) -> Path:
        """创建备份文件"""
        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        if backup_path.exists():
            backup_path = backup_path.with_name(
                f"{backup_path.stem}_{len(list(backup_path.parent.glob(f'{backup_path.stem}_*.backup')))}.backup"
            )
        return backup_path

    def convert_to_mdc(self, md_file: Path) -> Tuple[Path, str]:
        """
        将 .md 文件转换为 .mdc 格式

        Args:
            md_file: 源 .md 文件路径

        Returns:
            (目标 .mdc 文件路径, 转换后的内容)
        """
        # 读取原文件
        content = self.read_file(md_file)

        # 检查是否已有 frontmatter
        if content.startswith("---"):
            # 已有 frontmatter，直接重命名
            mdc_content = content
        else:
            # 推断 frontmatter
            metadata = self.infer_metadata(md_file, content)

            # 生成 frontmatter YAML
            frontmatter = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
            frontmatter = frontmatter.strip()

            # 组合内容
            mdc_content = f"---\n{frontmatter}\n---\n\n{content}"

        # 生成目标文件路径
        mdc_file = md_file.with_suffix(".mdc")

        return mdc_file, mdc_content

    def migrate_file(self, md_file: Path) -> bool:
        """
        迁移单个文件

        Returns:
            是否成功
        """
        if not md_file.exists():
            print(f"错误: 文件不存在: {md_file}")
            return False

        if md_file.suffix != ".md":
            print(f"跳过: 不是 .md 文件: {md_file}")
            return False

        # 检查目标文件是否已存在
        mdc_file = md_file.with_suffix(".mdc")
        if mdc_file.exists() and not self.force:
            print(f"跳过: 目标文件已存在: {mdc_file} (使用 --force 强制覆盖)")
            return False

        if self.dry_run:
            print(f"[DRY RUN] 将转换: {md_file} -> {mdc_file}")
            return True

        try:
            # 注意：不再创建备份（根据用户要求）

            # 转换为 MDC
            mdc_file, mdc_content = self.convert_to_mdc(md_file)

            # 写入新文件
            self.write_file(mdc_file, mdc_content)
            print(f"✓ 已转换: {md_file} -> {mdc_file}")

            # 删除原文件（不保留兼容）
            md_file.unlink()
            print(f"  已删除原文件: {md_file}")

            return True
        except Exception as e:
            print(f"错误: 转换失败 {md_file}: {e}")
            return False

    def migrate_directory(self, directory: Path) -> Tuple[int, int]:
        """
        迁移目录中的所有 .md 文件

        Returns:
            (成功数, 失败数)
        """
        md_files = list(directory.rglob("*.md"))
        success_count = 0
        fail_count = 0

        for md_file in md_files:
            # 跳过备份文件
            if md_file.name.endswith(".backup"):
                continue

            # 跳过 README.md 文件（文档文件，不是规则文件）
            if md_file.name == "README.md":
                if not self.dry_run:
                    print(f"跳过: {md_file} (README.md 文档文件)")
                continue

            # 跳过 docs 目录下的文件（文档文件）
            if "docs" in md_file.parts:
                if not self.dry_run:
                    print(f"跳过: {md_file} (docs 目录下的文档文件)")
                continue

            if self.migrate_file(md_file):
                success_count += 1
            else:
                fail_count += 1

        return success_count, fail_count


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="将 .md 规则文件转换为 .mdc 格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换单个文件
  python scripts/migrate-to-mdc.py .cursor/rules/meta-rules.md

  # 转换整个目录
  python scripts/migrate-to-mdc.py .cursor/rules/

  #  dry-run 模式（仅显示将要执行的操作）
  python scripts/migrate-to-mdc.py .cursor/rules/ --dry-run

  # 强制覆盖已存在的文件
  python scripts/migrate-to-mdc.py .cursor/rules/ --force
        """,
    )

    parser.add_argument(
        "path",
        type=str,
        help="要转换的文件或目录路径",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅显示将要执行的操作，不实际修改文件",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="（已废弃）不再创建备份文件",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制覆盖已存在的 .mdc 文件",
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"错误: 路径不存在: {path}")
        return 1

    migrator = MDCMigrator(
        dry_run=args.dry_run,
        backup=args.backup,
        force=args.force,
    )

    if path.is_file():
        # 转换单个文件
        success = migrator.migrate_file(path)
        return 0 if success else 1
    elif path.is_dir():
        # 转换目录
        print(f"正在转换目录: {path}")
        success_count, fail_count = migrator.migrate_directory(path)
        print(f"\n转换完成: 成功 {success_count} 个, 失败 {fail_count} 个")
        return 0 if fail_count == 0 else 1
    else:
        print(f"错误: 无效的路径类型: {path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
