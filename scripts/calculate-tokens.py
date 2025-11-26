#!/usr/bin/env python3
"""
Token 计算器

计算规则文件的 token 消耗，对比完整版和精简版的 token 数。

用法:
    python scripts/calculate-tokens.py [文件或目录] [选项]

选项:
    --compare: 对比完整版和精简版的 token 消耗
    --json: 输出 JSON 格式
    --markdown: 输出 Markdown 报告
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import tiktoken
except ImportError:
    print("错误: 需要安装 tiktoken 库")
    print("安装命令: pip install tiktoken 或 uv add tiktoken")
    sys.exit(1)


# 使用 cl100k_base 编码（GPT-4 和 Claude 使用）
ENCODING = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """
    计算文本的 token 数量

    Args:
        text: 要计算的文本

    Returns:
        token 数量
    """
    return len(ENCODING.encode(text))


def extract_content_from_mdc(file_path: Path) -> str:
    """
    从 MDC 文件中提取内容（排除 frontmatter）

    Args:
        file_path: MDC 文件路径

    Returns:
        提取的内容
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"错误: 读取文件失败 {file_path}: {e}", file=sys.stderr)
        return ""

    # 移除 frontmatter（以 --- 开头和结尾的 YAML 块）
    # 匹配模式：开头的 ---，然后是 YAML 内容，最后是 ---
    frontmatter_pattern = r"^---\s*\n(.*?)\n---\s*\n"
    content = re.sub(frontmatter_pattern, "", content, flags=re.DOTALL)

    return content.strip()


def calculate_file_tokens(file_path: Path) -> tuple[int, int]:
    """
    计算文件的 token 数量

    Args:
        file_path: 文件路径

    Returns:
        (总 token 数, 内容 token 数) - 对于 MDC 文件，内容 token 数排除 frontmatter
    """
    try:
        full_content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"错误: 读取文件失败 {file_path}: {e}", file=sys.stderr)
        return 0, 0

    total_tokens = count_tokens(full_content)

    # 如果是 MDC 文件，计算内容 token（排除 frontmatter）
    if file_path.suffix == ".mdc":
        content = extract_content_from_mdc(file_path)
        content_tokens = count_tokens(content)
    else:
        content_tokens = total_tokens

    return total_tokens, content_tokens


def find_matching_files(full_path: Path, concise_base: Path) -> Path | None:
    """
    在精简版目录中查找对应的文件

    Args:
        full_path: 完整版文件路径
        concise_base: 精简版基础目录

    Returns:
        对应的精简版文件路径，如果不存在则返回 None
    """
    # 获取相对于 full-rules 的路径
    if "full-rules" in full_path.parts:
        # 找到 full-rules 在路径中的位置
        full_index = full_path.parts.index("full-rules")
        relative_parts = full_path.parts[full_index + 1 :]

        # 构建精简版路径
        # full-rules/ide-layer/rulesets/01-general.mdc
        # -> .concise-rules/ide-layer/01-general.mdc
        if len(relative_parts) >= 2:
            # 移除 rulesets 目录（如果存在）
            if relative_parts[1] == "rulesets":
                concise_parts = [relative_parts[0]] + list(relative_parts[2:])
            else:
                concise_parts = list(relative_parts)

            # 处理项目模板路径
            # full-rules/project-templates/react-app/.cursor/rules/
            # 01-react-basics.mdc -> .concise-rules/project-templates/
            # react-app/01-react-basics.mdc
            if "project-templates" in concise_parts:
                # 移除 .cursor/rules 部分
                concise_parts = [
                    p for p in concise_parts if p not in (".cursor", "rules")
                ]

            concise_path = concise_base / Path(*concise_parts)
            if concise_path.exists():
                return concise_path

    return None


def compare_versions(full_path: Path, concise_path: Path) -> dict[str, any]:
    """
    对比完整版和精简版的 token 消耗

    Args:
        full_path: 完整版文件路径
        concise_path: 精简版文件路径

    Returns:
        对比结果字典
    """
    full_total, full_content = calculate_file_tokens(full_path)
    concise_total, concise_content = calculate_file_tokens(concise_path)

    reduction = (
        (full_content - concise_content) / full_content * 100 if full_content > 0 else 0
    )

    return {
        "file": full_path.name,
        "full_path": str(full_path),
        "concise_path": str(concise_path),
        "full_tokens": full_total,
        "full_content_tokens": full_content,
        "concise_tokens": concise_total,
        "concise_content_tokens": concise_content,
        "reduction": round(reduction, 2),
        "meets_target": reduction >= 70,
    }


def scan_directory(directory: Path, concise_base: Path) -> list[dict[str, any]]:
    """
    扫描目录中的所有规则文件并对比

    Args:
        directory: 要扫描的目录
        concise_base: 精简版基础目录

    Returns:
        对比结果列表
    """
    results = []
    mdc_files = list(directory.rglob("*.mdc"))
    md_files = list(directory.rglob("*.md"))

    all_files = mdc_files + md_files

    for full_file in all_files:
        # 跳过 README.md 和 docs 目录
        if full_file.name == "README.md" or "docs" in full_file.parts:
            continue

        concise_file = find_matching_files(full_file, concise_base)
        if concise_file:
            result = compare_versions(full_file, concise_file)
            results.append(result)

    return results


def generate_markdown_report(results: list[dict[str, any]]) -> str:
    """
    生成 Markdown 格式的报告

    Args:
        results: 对比结果列表

    Returns:
        Markdown 格式的报告
    """
    lines = ["# Token 消耗对比报告\n"]
    lines.append("| 文件 | 完整版 Token | 精简版 Token | 减少比例 | 状态 |")
    lines.append("|------|------------|------------|---------|------|")

    for result in sorted(results, key=lambda x: x["file"]):
        status = "✅" if result["meets_target"] else "⚠️"
        lines.append(
            f"| {result['file']} | {result['full_content_tokens']} | "
            f"{result['concise_content_tokens']} | {result['reduction']}% | {status} |"
        )

    # 统计信息
    total_full = sum(r["full_content_tokens"] for r in results)
    total_concise = sum(r["concise_content_tokens"] for r in results)
    avg_reduction = (
        (total_full - total_concise) / total_full * 100 if total_full > 0 else 0
    )
    meets_target_count = sum(1 for r in results if r["meets_target"])

    lines.append("\n## 统计信息\n")
    lines.append(f"- **总文件数**: {len(results)}")
    lines.append(f"- **完整版总 Token**: {total_full}")
    lines.append(f"- **精简版总 Token**: {total_concise}")
    lines.append(f"- **平均减少比例**: {avg_reduction:.2f}%")
    lines.append(f"- **达标文件数**: {meets_target_count}/{len(results)}")

    return "\n".join(lines)


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="计算规则文件的 token 消耗",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 计算单个文件
  python scripts/calculate-tokens.py full-rules/ide-layer/rulesets/01-general.mdc

  # 对比完整版和精简版
  python scripts/calculate-tokens.py full-rules/ --compare

  # 生成 JSON 报告
  python scripts/calculate-tokens.py full-rules/ --compare --json

  # 生成 Markdown 报告
  python scripts/calculate-tokens.py full-rules/ --compare --markdown
        """,
    )

    parser.add_argument(
        "path",
        type=str,
        help="要计算的文件或目录路径",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="对比完整版和精简版的 token 消耗",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON 格式",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="输出 Markdown 报告",
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"错误: 路径不存在: {path}", file=sys.stderr)
        return 1

    concise_base = Path(".concise-rules")

    if path.is_file():
        # 计算单个文件
        total_tokens, content_tokens = calculate_file_tokens(path)
        if args.json:
            output = {
                "file": str(path),
                "total_tokens": total_tokens,
                "content_tokens": content_tokens,
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"文件: {path}")
            print(f"总 Token 数: {total_tokens}")
            if path.suffix == ".mdc":
                print(f"内容 Token 数（排除 frontmatter）: {content_tokens}")
        return 0

    elif path.is_dir():
        # 扫描目录
        if args.compare:
            results = scan_directory(path, concise_base)
            if not results:
                print("未找到可对比的文件", file=sys.stderr)
                return 1

            if args.json:
                output = {
                    "results": results,
                    "summary": {
                        "total_files": len(results),
                        "total_full_tokens": sum(
                            r["full_content_tokens"] for r in results
                        ),
                        "total_concise_tokens": sum(
                            r["concise_content_tokens"] for r in results
                        ),
                        "avg_reduction": round(
                            (
                                sum(r["full_content_tokens"] for r in results)
                                - sum(r["concise_content_tokens"] for r in results)
                            )
                            / sum(r["full_content_tokens"] for r in results)
                            * 100,
                            2,
                        )
                        if sum(r["full_content_tokens"] for r in results) > 0
                        else 0,
                        "meets_target_count": sum(
                            1 for r in results if r["meets_target"]
                        ),
                    },
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
            elif args.markdown:
                report = generate_markdown_report(results)
                print(report)
            else:
                # 默认表格输出
                header = (
                    f"{'文件':<40} {'完整版':<10} "
                    f"{'精简版':<10} {'减少':<10} {'状态':<6}"
                )
                print(header)
                print("-" * 80)
                for result in sorted(results, key=lambda x: x["file"]):
                    status = "✅" if result["meets_target"] else "⚠️"
                    print(
                        f"{result['file']:<40} "
                        f"{result['full_content_tokens']:<10} "
                        f"{result['concise_content_tokens']:<10} "
                        f"{result['reduction']:<9}% {status}"
                    )
            return 0
        else:
            print("错误: 目录模式需要 --compare 选项", file=sys.stderr)
            return 1
    else:
        print(f"错误: 无效的路径类型: {path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
