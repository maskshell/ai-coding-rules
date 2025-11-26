#!/usr/bin/env python3
"""
PR 质量报告生成器

生成 PR 质量报告，包括变更统计、验证结果、质量评分等。

用法:
    python scripts/generate-pr-report.py [选项]

选项:
    --base: 基础 commit SHA（默认：从环境变量获取）
    --head: 头部 commit SHA（默认：从环境变量获取）
    --json: 输出 JSON 格式
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("错误: 需要安装 PyYAML 库")
    print("安装命令: pip install pyyaml 或 uv add pyyaml")
    sys.exit(1)


def run_command(cmd: list[str], capture_output: bool = True) -> tuple[int, str, str]:
    """
    运行命令并返回结果

    Args:
        cmd: 命令列表
        capture_output: 是否捕获输出

    Returns:
        (返回码, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def get_changed_files(base_sha: str, head_sha: str) -> dict[str, list[str]]:
    """
    获取变更文件列表

    Args:
        base_sha: 基础 commit SHA
        head_sha: 头部 commit SHA

    Returns:
        包含新增、修改、删除文件的字典
    """
    _, output, _ = run_command(
        [
            "git",
            "diff",
            "--name-status",
            "--diff-filter=ACMRTUXB",
            f"{base_sha}..{head_sha}",
        ]
    )

    added = []
    modified = []
    deleted = []

    for line in output.strip().split("\n"):
        if not line:
            continue

        status = line[0]
        file_path = line[1:].strip()

        if status == "A":
            added.append(file_path)
        elif status == "M":
            modified.append(file_path)
        elif status == "D":
            deleted.append(file_path)

    return {"added": added, "modified": modified, "deleted": deleted}


def check_rule_files(changed_files: dict[str, list[str]]) -> dict[str, Any]:
    """
    检查规则文件

    Args:
        changed_files: 变更文件字典

    Returns:
        规则文件检查结果
    """
    all_files = changed_files["added"] + changed_files["modified"]
    rule_files = [
        f
        for f in all_files
        if (f.endswith(".mdc") or f.endswith(".md"))
        and "README.md" not in f
        and not f.startswith("docs/")
    ]

    if not rule_files:
        return {"has_rules": False, "count": 0, "files": []}

    # 运行 lint-rules.py 检查
    errors = []
    warnings = []

    for rule_file in rule_files:
        if not Path(rule_file).exists():
            continue

        returncode, stdout, stderr = run_command(
            ["python", "scripts/lint-rules.py", rule_file, "--json"]
        )

        if returncode != 0:
            try:
                result = json.loads(stdout)
                if not result.get("valid", True):
                    errors.extend(result.get("errors", []))
                    warnings.extend(result.get("warnings", []))
            except json.JSONDecodeError:
                errors.append({"file": rule_file, "message": stderr or stdout})

    return {
        "has_rules": True,
        "count": len(rule_files),
        "files": rule_files,
        "errors": errors,
        "warnings": warnings,
        "valid": len(errors) == 0,
    }


def check_documentation(changed_files: dict[str, list[str]]) -> dict[str, Any]:
    """
    检查文档更新

    Args:
        changed_files: 变更文件字典

    Returns:
        文档检查结果
    """
    all_files = changed_files["added"] + changed_files["modified"]
    has_rule_changes = any(
        (f.endswith(".mdc") or f.endswith(".md"))
        and "README.md" not in f
        and not f.startswith("docs/")
        for f in all_files
    )

    docs_updated = any(
        f in ["CHANGELOG.md", "README.md", "README.cn.md"] for f in all_files
    )

    return {
        "has_rule_changes": has_rule_changes,
        "docs_updated": docs_updated,
        "recommendation": "建议更新 CHANGELOG.md" if has_rule_changes and not docs_updated else "文档已更新",
    }


def check_token_consumption(changed_files: dict[str, list[str]]) -> dict[str, Any]:
    """
    检查 Token 消耗

    Args:
        changed_files: 变更文件字典

    Returns:
        Token 消耗检查结果
    """
    all_files = changed_files["added"] + changed_files["modified"]
    has_full_rules = any(f.startswith("full-rules/") and f.endswith(".mdc") for f in all_files)

    if not has_full_rules:
        return {"checked": False, "message": "未检测到完整版规则变更"}

    # 运行 calculate-tokens.py
    returncode, stdout, stderr = run_command(
        ["python", "scripts/calculate-tokens.py", "full-rules/", "--compare", "--json"]
    )

    if returncode != 0:
        return {"checked": False, "message": "Token 计算失败", "error": stderr}

    try:
        result = json.loads(stdout)
        summary = result.get("summary", {})

        total_files = summary.get("total_files", 0)
        avg_reduction = summary.get("avg_reduction", 0)
        meets_target_count = summary.get("meets_target_count", 0)

        return {
            "checked": True,
            "total_files": total_files,
            "avg_reduction": avg_reduction,
            "meets_target_count": meets_target_count,
            "meets_target": avg_reduction >= 70,
        }
    except (json.JSONDecodeError, KeyError):
        return {"checked": False, "message": "无法解析 Token 计算结果"}


def calculate_quality_score(
    rule_check: dict[str, Any],
    doc_check: dict[str, Any],
    token_check: dict[str, Any],
) -> int:
    """
    计算质量评分（0-100）

    Args:
        rule_check: 规则检查结果
        doc_check: 文档检查结果
        token_check: Token 检查结果

    Returns:
        质量评分（0-100）
    """
    score = 100

    # 规则验证（40分）
    if rule_check.get("has_rules", False):
        if not rule_check.get("valid", True):
            score -= 40
        elif rule_check.get("warnings"):
            score -= len(rule_check["warnings"]) * 5
            score = max(0, score)

    # 文档更新（20分）
    if doc_check.get("has_rule_changes", False) and not doc_check.get("docs_updated", False):
        score -= 20

    # Token 消耗（40分）
    if token_check.get("checked", False):
        if not token_check.get("meets_target", False):
            reduction = token_check.get("avg_reduction", 0)
            if reduction < 50:
                score -= 40
            elif reduction < 70:
                score -= 20

    return max(0, min(100, score))


def generate_markdown_report(report: dict[str, Any]) -> str:
    """
    生成 Markdown 格式的报告

    Args:
        report: 报告数据

    Returns:
        Markdown 格式的报告
    """
    score = report["quality_score"]
    score_emoji = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"

    md = f"""# 📊 PR 质量报告

{score_emoji} **质量评分**: {score}/100

---

## 📝 变更文件统计

- **新增**: {len(report['changed_files']['added'])} 个文件
- **修改**: {len(report['changed_files']['modified'])} 个文件
- **删除**: {len(report['changed_files']['deleted'])} 个文件

"""

    # 规则验证结果
    rule_check = report["rule_check"]
    if rule_check.get("has_rules", False):
        md += f"""## ✅ 规则验证结果

- **规则文件数量**: {rule_check['count']}
- **验证状态**: {'✅ 通过' if rule_check.get('valid', True) else '❌ 失败'}

"""
        if rule_check.get("errors"):
            md += "### ❌ 错误\n\n"
            for error in rule_check["errors"]:
                md += f"- {error.get('message', '未知错误')}\n"
            md += "\n"

        if rule_check.get("warnings"):
            md += "### ⚠️ 警告\n\n"
            for warning in rule_check["warnings"][:5]:  # 最多显示5个警告
                md += f"- {warning.get('message', '未知警告')}\n"
            md += "\n"
    else:
        md += "## ℹ️ 规则验证\n\n未检测到规则文件变更\n\n"

    # 文档检查
    doc_check = report["documentation_check"]
    if doc_check.get("has_rule_changes", False):
        md += f"""## 📚 文档更新检查

- **状态**: {'✅ 已更新' if doc_check.get('docs_updated', False) else '⚠️ 未更新'}
- **建议**: {doc_check.get('recommendation', '')}

"""
    else:
        md += "## 📚 文档更新检查\n\n未检测到规则变更，无需更新文档\n\n"

    # Token 消耗
    token_check = report["token_check"]
    if token_check.get("checked", False):
        avg_reduction = token_check.get("avg_reduction", 0)
        meets_target = token_check.get("meets_target", False)
        status_emoji = "✅" if meets_target else "⚠️"

        md += f"""## 🎯 Token 消耗分析

{status_emoji} **平均减少比例**: {avg_reduction:.2f}%
- **目标**: ≥ 70%
- **状态**: {'✅ 达标' if meets_target else '⚠️ 未达标'}
- **达标文件数**: {token_check.get('meets_target_count', 0)}/{token_check.get('total_files', 0)}

"""
    else:
        md += f"""## 🎯 Token 消耗分析

ℹ️ {token_check.get('message', '未检测到完整版规则变更')}

"""

    # 改进建议
    suggestions = []
    if rule_check.get("has_rules", False) and not rule_check.get("valid", True):
        suggestions.append("修复规则文件中的错误")
    if doc_check.get("has_rule_changes", False) and not doc_check.get("docs_updated", False):
        suggestions.append("更新 CHANGELOG.md 记录变更")
    if token_check.get("checked", False) and not token_check.get("meets_target", False):
        suggestions.append("优化精简版规则，减少 token 消耗")

    if suggestions:
        md += "## 💡 改进建议\n\n"
        for i, suggestion in enumerate(suggestions, 1):
            md += f"{i}. {suggestion}\n"
        md += "\n"

    md += "---\n\n"
    md += "*此报告由 PR 质量门禁自动生成*"

    return md


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="生成 PR 质量报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--base",
        type=str,
        default=os.getenv("GITHUB_BASE_SHA", "HEAD~1"),
        help="基础 commit SHA",
    )
    parser.add_argument(
        "--head",
        type=str,
        default=os.getenv("GITHUB_SHA", "HEAD"),
        help="头部 commit SHA",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON 格式",
    )

    args = parser.parse_args()

    # 获取变更文件
    changed_files = get_changed_files(args.base, args.head)

    # 检查规则文件
    rule_check = check_rule_files(changed_files)

    # 检查文档更新
    doc_check = check_documentation(changed_files)

    # 检查 Token 消耗
    token_check = check_token_consumption(changed_files)

    # 计算质量评分
    quality_score = calculate_quality_score(rule_check, doc_check, token_check)

    # 生成报告
    report = {
        "changed_files": changed_files,
        "rule_check": rule_check,
        "documentation_check": doc_check,
        "token_check": token_check,
        "quality_score": quality_score,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(generate_markdown_report(report))

    return 0 if quality_score >= 60 else 1


if __name__ == "__main__":
    sys.exit(main())

