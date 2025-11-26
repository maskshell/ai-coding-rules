#!/usr/bin/env python3
"""
规则质量验证工具（Rule Linter）

验证规则文件的格式、结构和内容质量。

用法:
    python scripts/lint-rules.py [文件或目录] [选项]

选项:
    --check: 仅检查，不自动修复
    --json: 输出 JSON 格式
"""

import argparse
import json
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


# 文件名格式：数字前缀-小写短横线.mdc 或 .md
FILENAME_PATTERN = re.compile(r"^\d{2}-[a-z0-9-]+\.(mdc|md)$")

# 标题模式：匹配 Markdown 标题
HEADER_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

# 代码块模式
CODE_BLOCK_PATTERN = re.compile(r"```(\w+)?\n.*?```", re.DOTALL)

# Good/Bad 标注模式
GOOD_BAD_PATTERN = re.compile(r"(//|#)\s*(Good|Bad|✅|❌)", re.IGNORECASE)

MAX_HEADER_LEVEL = 4
MAX_CONCISE_LINES = 150


class RuleLinter:
    """规则质量验证器"""

    def __init__(self):
        self.errors: List[Dict[str, str]] = []
        self.warnings: List[Dict[str, str]] = []

    def check_filename(self, file_path: Path) -> list[dict[str, str]]:
        """
        检查文件名格式

        Args:
            file_path: 文件路径

        Returns:
            错误列表
        """
        errors = []
        filename = file_path.name

        # 跳过 README.md
        if filename == "README.md":
            return errors

        if not FILENAME_PATTERN.match(filename):
            errors.append(
                {
                    "type": "error",
                    "message": f"文件名格式不符合规范: {filename}。应为 '数字前缀-小写短横线.mdc' 格式",
                }
            )

        return errors

    def check_header_levels(self, content: str) -> list[dict[str, str]]:
        """
        检查标题层级

        Args:
            content: 文件内容

        Returns:
            错误和警告列表
        """
        issues = []
        headers = HEADER_PATTERN.findall(content)

        for level, title in headers:
            level_num = len(level)
            if level_num > MAX_HEADER_LEVEL:
                issues.append(
                    {
                        "type": "error",
                        "message": f"标题层级过深: {title} (最多允许 {MAX_HEADER_LEVEL} 级)",
                    }
                )

        # 检查标题跳级
        previous_level = 0
        for level, title in headers:
            current_level = len(level)
            if current_level > previous_level + 1:
                issues.append(
                    {
                        "type": "error",
                        "message": f"标题跳级: {'#' * previous_level} → {'#' * current_level} (不允许跳级)",
                    }
                )
            previous_level = current_level

        # 检查深度警告
        max_level = max((len(level) for level, _ in headers), default=0)
        if max_level > 3:
            issues.append(
                {
                    "type": "warning",
                    "message": f"标题层级较深 (最深 {max_level} 级)，建议不超过 3 级",
                }
            )

        return issues

    def check_code_examples(self, content: str) -> list[dict[str, str]]:
        """
        检查代码示例

        Args:
            content: 文件内容

        Returns:
            错误和警告列表
        """
        issues = []
        code_blocks = CODE_BLOCK_PATTERN.findall(content)

        if len(code_blocks) == 0:
            issues.append(
                {
                    "type": "error",
                    "message": "缺少代码示例（至少需要 1 个）",
                }
            )
        elif len(code_blocks) < 2:
            issues.append(
                {
                    "type": "warning",
                    "message": f"代码示例较少 ({len(code_blocks)} 个)，建议至少 2 个",
                }
            )

        # 检查 Good/Bad 标注
        good_bad_count = len(GOOD_BAD_PATTERN.findall(content))
        if good_bad_count == 0 and len(code_blocks) > 0:
            issues.append(
                {
                    "type": "warning",
                    "message": "代码示例缺少 Good/Bad 标注",
                }
            )

        return issues

    def check_concise_format(
        self, file_path: Path, content: str
    ) -> list[dict[str, str]]:
        """
        检查精简版格式

        Args:
            file_path: 文件路径
            content: 文件内容

        Returns:
            警告列表
        """
        warnings = []

        # 检查是否在精简版目录
        if ".concise-rules" in str(file_path):
            line_count = len(content.splitlines())
            if line_count > MAX_CONCISE_LINES:
                warnings.append(
                    {
                        "type": "warning",
                        "message": f"精简版文件行数过多 ({line_count} 行)，建议 < {MAX_CONCISE_LINES} 行",
                    }
                )

        return warnings

    def check_file(
        self, file_path: Path
    ) -> tuple[bool, list[dict[str, str]], list[dict[str, str]]]:
        """
        检查单个文件

        Args:
            file_path: 文件路径

        Returns:
            (是否通过, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []

        if not file_path.exists():
            self.errors.append(
                {
                    "type": "error",
                    "message": f"文件不存在: {file_path}",
                }
            )
            return False, self.errors, self.warnings

        # 跳过非规则文件
        if file_path.name == "README.md" or "docs" in file_path.parts:
            return True, [], []

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(
                {
                    "type": "error",
                    "message": f"读取文件失败: {e}",
                }
            )
            return False, self.errors, self.warnings

        # 执行各项检查
        self.errors.extend(self.check_filename(file_path))

        header_issues = self.check_header_levels(content)
        for issue in header_issues:
            if issue["type"] == "error":
                self.errors.append(issue)
            else:
                self.warnings.append(issue)

        code_issues = self.check_code_examples(content)
        for issue in code_issues:
            if issue["type"] == "error":
                self.errors.append(issue)
            else:
                self.warnings.append(issue)

        self.warnings.extend(self.check_concise_format(file_path, content))

        return len(self.errors) == 0, self.errors, self.warnings

    def check_directory(self, directory: Path) -> tuple[int, int]:
        """
        检查目录中的所有规则文件

        Args:
            directory: 目录路径

        Returns:
            (通过数, 失败数)
        """
        mdc_files = list(directory.rglob("*.mdc"))
        md_files = list(directory.rglob("*.md"))
        all_files = mdc_files + md_files

        pass_count = 0
        fail_count = 0

        for file_path in all_files:
            # 跳过 README 和 docs
            if file_path.name == "README.md" or "docs" in file_path.parts:
                continue

            is_valid, errors, warnings = self.check_file(file_path)
            if is_valid:
                pass_count += 1
            else:
                fail_count += 1

        return pass_count, fail_count


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="验证规则文件的格式、结构和内容质量",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 验证单个文件
  python scripts/lint-rules.py .cursor/rules/meta-rules.mdc

  # 验证整个目录
  python scripts/lint-rules.py .cursor/rules/

  # 输出 JSON 格式
  python scripts/lint-rules.py .cursor/rules/ --json
        """,
    )

    parser.add_argument(
        "path",
        type=str,
        help="要验证的文件或目录路径",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="仅检查，不自动修复（默认行为）",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON 格式",
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"错误: 路径不存在: {path}", file=sys.stderr)
        return 1

    linter = RuleLinter()

    if path.is_file():
        # 验证单个文件
        is_valid, errors, warnings = linter.check_file(path)
        if args.json:
            output = {
                "file": str(path),
                "valid": is_valid,
                "errors": errors,
                "warnings": warnings,
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            if is_valid:
                print(f"✓ {path} 验证通过")
                if warnings:
                    for warning in warnings:
                        print(f"  警告: {warning['message']}")
                return 0
            else:
                print(f"✗ {path} 验证失败")
                for error in errors:
                    print(f"  错误: {error['message']}")
                if warnings:
                    for warning in warnings:
                        print(f"  警告: {warning['message']}")
                return 1
    elif path.is_dir():
        # 验证目录
        if args.json:
            results = []
            mdc_files = list(path.rglob("*.mdc"))
            md_files = list(path.rglob("*.md"))
            all_files = mdc_files + md_files

            for file_path in all_files:
                if file_path.name == "README.md" or "docs" in file_path.parts:
                    continue

                is_valid, errors, warnings = linter.check_file(file_path)
                results.append(
                    {
                        "file": str(file_path),
                        "valid": is_valid,
                        "errors": errors,
                        "warnings": warnings,
                    }
                )

            output = {
                "results": results,
                "summary": {
                    "total": len(results),
                    "passed": sum(1 for r in results if r["valid"]),
                    "failed": sum(1 for r in results if not r["valid"]),
                },
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print(f"正在验证目录: {path}")
            pass_count, fail_count = linter.check_directory(path)
            print(f"\n验证完成: 通过 {pass_count} 个, 失败 {fail_count} 个")
            return 0 if fail_count == 0 else 1
    else:
        print(f"错误: 无效的路径类型: {path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

