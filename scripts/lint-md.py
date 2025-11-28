#!/usr/bin/env python3
"""
Markdown linting 脚本

调用系统级 markdownlint 命令检查 Markdown 文件格式。
与 Cursor IDE 的 markdownlint 扩展保持一致。
同时验证项目特定规则（数字前缀、标题层级等）。
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# 常量定义
MARKDOWN_EXTENSIONS = {".md", ".mdc"}
CONFIG_FILE_NAME = ".markdownlint.json"
COMMAND_TIMEOUT = 60
VERSION_CHECK_TIMEOUT = 5
MAX_HEADER_LEVEL = 4

# markdownlint 命令优先级：优先使用 Homebrew 安装的 markdownlint
MARKDOWNLINT_COMMANDS = ["markdownlint", "markdownlint-cli2"]

# 规则文件路径关键词（用于识别规则文件）
RULE_FILE_KEYWORDS = ["rulesets", "rules", "coderules"]

# 正则表达式模式
FILENAME_PATTERN = re.compile(r"^\d{2}-[a-z0-9-]+\.md$")
HEADER_PATTERN = re.compile(r"^(#{1,6})\s+", re.MULTILINE)
CODE_BLOCK_PATTERN = re.compile(r"```(\w+)?\n")
# 匹配完整的代码块（包括 ``` 和 `````，用于移除代码块内容）
# 匹配 ``` 或 ````` 开头的代码块，直到对应的结束标记
FULL_CODE_BLOCK_PATTERN = re.compile(r"```+[^\n]*\n.*?```+", re.DOTALL)


class MarkdownLintNotFoundError(Exception):
    """markdownlint 命令未找到异常"""

    pass


class MarkdownLintExecutionError(Exception):
    """markdownlint 执行错误异常"""

    pass


class FileReadError(Exception):
    """文件读取错误异常"""

    pass


def find_markdownlint_command() -> str | None:
    """
    检测系统中可用的 markdownlint 命令

    Returns:
        可用的命令名，如果未找到则返回 None
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


def build_markdownlint_command(cmd: str, files: list[Path]) -> list[str]:
    """
    构建 markdownlint 命令参数

    Args:
        cmd: markdownlint 命令名
        files: 要检查的文件列表

    Returns:
        完整的命令参数列表
    """
    cmd_args = [cmd]

    # 添加配置文件（如果存在）
    # 注意：两个命令都使用相同的 --config 参数格式
    config_file = Path(CONFIG_FILE_NAME)
    if config_file.exists():
        cmd_args.extend(["--config", str(config_file)])

    # 添加文件列表
    file_paths = [str(f) for f in files]
    cmd_args.extend(file_paths)

    return cmd_args


def check_markdownlint(files: list[Path]) -> tuple[int, str]:
    """
    使用 markdownlint 检查文件格式

    Args:
        files: 要检查的文件列表

    Returns:
        (退出码, 输出信息) 元组

    Raises:
        MarkdownLintNotFoundError: 未找到 markdownlint 命令
        MarkdownLintExecutionError: 执行 markdownlint 时出错
    """
    cmd = find_markdownlint_command()

    if not cmd:
        error_msg = (
            "错误: 未找到 markdownlint 命令\n"
            "请安装: brew install markdownlint-cli 或 npm install -g markdownlint-cli"
        )
        raise MarkdownLintNotFoundError(error_msg)

    cmd_args = build_markdownlint_command(cmd, files)

    try:
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT,
        )

        output = result.stdout + result.stderr
        return result.returncode, output
    except subprocess.TimeoutExpired as e:
        raise MarkdownLintExecutionError(f"markdownlint 执行超时: {e}") from e
    except subprocess.SubprocessError as e:
        raise MarkdownLintExecutionError(f"执行 markdownlint 时出错: {e}") from e


def read_file_content(file: Path) -> str:
    """
    读取文件内容

    Args:
        file: 文件路径

    Returns:
        文件内容字符串

    Raises:
        FileReadError: 文件读取失败
    """
    try:
        return file.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise FileReadError(f"文件不存在: {e}") from e
    except PermissionError as e:
        raise FileReadError(f"无权限读取文件: {e}") from e
    except UnicodeDecodeError as e:
        raise FileReadError(f"文件编码错误: {e}") from e
    except OSError as e:
        # OSError 是文件操作相关的其他系统错误的基类
        raise FileReadError(f"读取文件失败: {e}") from e


def is_rule_file(file_path: Path) -> bool:
    """
    判断是否为规则文件

    Args:
        file_path: 文件路径

    Returns:
        如果是规则文件返回 True，否则返回 False
    """
    path_str = str(file_path)
    return any(keyword in path_str for keyword in RULE_FILE_KEYWORDS)


def check_filename_format(file: Path) -> str | None:
    """
    检查文件名格式（仅对规则文件）

    Args:
        file: 文件路径

    Returns:
        如果格式错误返回错误信息，否则返回 None
    """
    if not is_rule_file(file):
        return None

    filename = file.name
    if not FILENAME_PATTERN.match(filename):
        return f"文件名格式错误: {filename} (应为: 数字前缀-小写短横线.md)"

    return None


def remove_code_blocks(content: str) -> str:
    """
    移除所有代码块内容，避免代码块中的标题被误判

    Args:
        content: 文件内容

    Returns:
        移除代码块后的内容
    """
    # 移除所有代码块（包括 ``` 和 `````）
    return FULL_CODE_BLOCK_PATTERN.sub("", content)


def check_header_levels(content: str) -> list[str]:
    """
    检查标题层级（不超过 4 级）

    Args:
        content: 文件内容

    Returns:
        错误信息列表
    """
    errors: list[str] = []
    # 先移除代码块内容，避免代码块中的标题被误判
    content_without_code = remove_code_blocks(content)
    headers = HEADER_PATTERN.findall(content_without_code)

    for header in headers:
        level = len(header)
        if level > MAX_HEADER_LEVEL:
            errors.append(f"标题层级过深: {header} (最多允许 {MAX_HEADER_LEVEL} 级)")

    return errors


def check_header_skipping(content: str) -> list[str]:
    """
    检查标题跳级（不允许跳级）

    Args:
        content: 文件内容

    Returns:
        错误信息列表
    """
    errors: list[str] = []
    # 先移除代码块内容，避免代码块中的标题被误判
    content_without_code = remove_code_blocks(content)
    headers = HEADER_PATTERN.findall(content_without_code)
    header_levels = [len(h) for h in headers]

    for i in range(1, len(header_levels)):
        current_level = header_levels[i]
        previous_level = header_levels[i - 1]

        # 检查是否跳级（当前级别大于前一级别 + 1）
        if current_level > previous_level + 1:
            errors.append(
                f"标题跳级: {'#' * previous_level} → {'#' * current_level} (不允许跳级)"
            )

    return errors


def check_code_block_language_tags(content: str) -> list[str]:
    """
    检查代码块语言标签

    Args:
        content: 文件内容

    Returns:
        错误信息列表
    """
    errors: list[str] = []
    code_blocks = CODE_BLOCK_PATTERN.findall(content)

    # 找出缺少语言标签的代码块位置
    empty_lang_blocks = [i for i, lang in enumerate(code_blocks, 1) if not lang]

    if empty_lang_blocks:
        # 只显示前 5 个错误位置，避免输出过长
        positions = ", ".join(map(str, empty_lang_blocks[:5]))
        errors.append(f"代码块缺少语言标签 (位置: {positions})")

    return errors


def check_project_specific_rules(file: Path) -> list[str]:
    """
    检查项目特定规则

    Args:
        file: 要检查的文件路径

    Returns:
        错误信息列表
    """
    errors: list[str] = []

    # 跳过 docs 目录中的文件（这些是文档文件，不是规则文件）
    if "docs" in file.parts:
        return errors

    try:
        content = read_file_content(file)
    except FileReadError as e:
        return [f"无法读取文件: {e}"]

    # 检查文件名格式（仅对规则文件）
    filename_error = check_filename_format(file)
    if filename_error:
        errors.append(filename_error)

    # 检查标题层级
    errors.extend(check_header_levels(content))

    # 检查标题跳级
    errors.extend(check_header_skipping(content))

    # 检查代码块语言标签
    errors.extend(check_code_block_language_tags(content))

    return errors


def filter_markdown_files(files: list[Path]) -> list[Path]:
    """
    过滤出有效的 Markdown 文件

    Args:
        files: 输入文件列表

    Returns:
        有效的 Markdown 文件列表
    """
    markdown_files = [
        f for f in files if f.exists() and f.suffix in MARKDOWN_EXTENSIONS
    ]
    return markdown_files


def lint_markdown_files(files: list[Path], check_only: bool = False) -> int:
    """
    检查 Markdown 文件格式

    Args:
        files: 要检查的文件列表
        check_only: 是否仅检查（当前未使用，保留用于未来扩展）

    Returns:
        退出码：0 表示成功，非 0 表示失败
    """
    # 过滤有效的 Markdown 文件
    markdown_files = filter_markdown_files(files)

    if not markdown_files:
        print("错误: 没有找到 Markdown 文件", file=sys.stderr)
        return 1

    # 使用 markdownlint 检查
    try:
        returncode, output = check_markdownlint(markdown_files)
    except MarkdownLintNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except MarkdownLintExecutionError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

    if output:
        print(output)

    # 检查项目特定规则
    project_errors: list[tuple[Path, list[str]]] = []
    for file in markdown_files:
        errors = check_project_specific_rules(file)
        if errors:
            project_errors.append((file, errors))

    if project_errors:
        print("\n项目特定规则检查:", file=sys.stderr)
        for file, errors in project_errors:
            print(f"\n📄 {file}:", file=sys.stderr)
            for error in errors:
                print(f"  ❌ {error}", file=sys.stderr)
        returncode = 1

    return returncode


def main() -> int:
    """
    主函数：解析命令行参数并执行 linting

    Returns:
        退出码：0 表示成功，非 0 表示失败
    """
    parser = argparse.ArgumentParser(
        description="检查 Markdown 文件格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s file.md              # 检查单个文件
  %(prog)s *.md                  # 检查所有 .md 文件
  %(prog)s --check file.md       # 仅检查（默认行为）
        """,
    )

    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="要检查的 Markdown 文件",
    )

    parser.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="仅检查格式（默认）",
    )

    args = parser.parse_args()

    return lint_markdown_files(args.files, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
