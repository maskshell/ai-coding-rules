#!/usr/bin/env python3
"""
Markdown 格式化脚本

调用系统级 markdownlint 命令格式化 Markdown 文件。
与 Cursor IDE 的 markdownlint 扩展保持一致。
"""

import argparse
import subprocess
import sys
from pathlib import Path

# 常量定义
MARKDOWN_EXTENSIONS = {".md", ".mdc"}
CONFIG_FILE_NAME = ".markdownlint.json"
COMMAND_TIMEOUT = 60
VERSION_CHECK_TIMEOUT = 5

# markdownlint 命令优先级：优先使用 Homebrew 安装的 markdownlint
MARKDOWNLINT_COMMANDS = ["markdownlint", "markdownlint-cli2"]


class MarkdownLintNotFoundError(Exception):
    """markdownlint 命令未找到异常"""

    pass


class MarkdownLintExecutionError(Exception):
    """markdownlint 执行错误异常"""

    pass


def find_markdownlint_command() -> str | None:
    """
    检测系统中可用的 markdownlint 命令

    Returns:
        可用的命令名，如果未找到则返回 None

    Raises:
        不抛出异常，仅返回 None 表示未找到
    """
    for cmd in MARKDOWNLINT_COMMANDS:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=VERSION_CHECK_TIMEOUT,
            )
            if result.returncode == 0:
                return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # 继续尝试下一个命令
            continue

    return None


def build_markdownlint_command(
    cmd: str, files: list[Path], fix: bool = True
) -> list[str]:
    """
    构建 markdownlint 命令参数

    Args:
        cmd: markdownlint 命令名
        files: 要处理的文件列表
        fix: 是否自动修复

    Returns:
        完整的命令参数列表
    """
    cmd_args = [cmd]

    # 添加 --fix 参数（如果支持修复）
    if fix:
        cmd_args.append("--fix")

    # 添加配置文件（如果存在）
    # 注意：两个命令都使用相同的 --config 参数格式
    config_file = Path(CONFIG_FILE_NAME)
    if config_file.exists():
        cmd_args.extend(["--config", str(config_file)])

    # 添加文件列表
    file_paths = [str(f) for f in files]
    cmd_args.extend(file_paths)

    return cmd_args


def format_markdown_files(files: list[Path], fix: bool = True) -> int:
    """
    格式化 Markdown 文件

    Args:
        files: 要格式化的文件列表
        fix: 是否自动修复格式问题

    Returns:
        退出码：0 表示成功，非 0 表示失败

    Raises:
        MarkdownLintNotFoundError: 未找到 markdownlint 命令
        MarkdownLintExecutionError: 执行 markdownlint 时出错
    """
    cmd = find_markdownlint_command()

    if not cmd:
        raise MarkdownLintNotFoundError(
            "未找到 markdownlint 命令。\n"
            "请安装 markdownlint:\n"
            "  macOS: brew install markdownlint-cli\n"
            "  其他: npm install -g markdownlint-cli"
        )

    cmd_args = build_markdownlint_command(cmd, files, fix=fix)

    try:
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT,
        )

        # 输出标准输出和标准错误
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        return result.returncode
    except subprocess.TimeoutExpired as e:
        raise MarkdownLintExecutionError(f"markdownlint 执行超时: {e}") from e
    except subprocess.SubprocessError as e:
        raise MarkdownLintExecutionError(f"执行 markdownlint 时出错: {e}") from e


def filter_markdown_files(files: list[Path]) -> list[Path]:
    """
    过滤出有效的 Markdown 文件

    Args:
        files: 输入文件列表

    Returns:
        有效的 Markdown 文件列表
    """
    existing_files = [f for f in files if f.exists()]
    markdown_files = [f for f in existing_files if f.suffix in MARKDOWN_EXTENSIONS]
    return markdown_files


def main() -> int:
    """
    主函数：解析命令行参数并执行格式化

    Returns:
        退出码：0 表示成功，非 0 表示失败
    """
    parser = argparse.ArgumentParser(
        description="格式化 Markdown 文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s file.md              # 格式化单个文件
  %(prog)s *.md                  # 格式化所有 .md 文件
  %(prog)s --check file.md       # 仅检查，不修复
        """,
    )

    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="要格式化的 Markdown 文件",
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="仅检查格式，不自动修复",
    )

    args = parser.parse_args()

    # 过滤有效的 Markdown 文件
    markdown_files = filter_markdown_files(args.files)

    if not markdown_files:
        print("错误: 没有找到有效的 Markdown 文件", file=sys.stderr)
        return 1

    try:
        return format_markdown_files(markdown_files, fix=not args.check)
    except MarkdownLintNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except MarkdownLintExecutionError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
