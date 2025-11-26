#!/usr/bin/env python3
"""
测试 lint-md.py 脚本
"""

import importlib.util
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.tmpdir import TempPathFactory

# 动态导入 scripts 模块
scripts_dir = Path(__file__).parent.parent / "scripts"
spec = importlib.util.spec_from_file_location("lint_md", scripts_dir / "lint-md.py")
lint_md = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint_md)

# 导入函数和异常类
check_markdownlint = lint_md.check_markdownlint
check_project_specific_rules = lint_md.check_project_specific_rules
find_markdownlint_command = lint_md.find_markdownlint_command
build_markdownlint_command = lint_md.build_markdownlint_command
read_file_content = lint_md.read_file_content
is_rule_file = lint_md.is_rule_file
check_filename_format = lint_md.check_filename_format
check_header_levels = lint_md.check_header_levels
check_header_skipping = lint_md.check_header_skipping
check_code_block_language_tags = lint_md.check_code_block_language_tags
filter_markdown_files = lint_md.filter_markdown_files
lint_markdown_files = lint_md.lint_markdown_files
main = lint_md.main
MarkdownLintNotFoundError = lint_md.MarkdownLintNotFoundError
MarkdownLintExecutionError = lint_md.MarkdownLintExecutionError
FileReadError = lint_md.FileReadError


class TestFindMarkdownlintCommand:
    """测试命令检测功能"""

    @patch("lint_md.subprocess.run")
    def test_find_markdownlint_success(self, mock_run: MagicMock) -> None:
        """测试成功找到 markdownlint 命令"""
        mock_run.return_value = MagicMock(returncode=0)
        result = find_markdownlint_command()
        assert result == "markdownlint"
        mock_run.assert_called()

    @patch("lint_md.subprocess.run")
    def test_find_markdownlint_not_found(self, mock_run: MagicMock) -> None:
        """测试未找到任何命令"""
        mock_run.side_effect = FileNotFoundError()
        result = find_markdownlint_command()
        assert result is None


class TestBuildMarkdownlintCommand:
    """测试命令构建功能"""

    def test_build_command_with_config(self, tmp_path: Path) -> None:
        """测试构建包含配置文件的命令"""
        # 创建临时配置文件
        config_file = tmp_path / ".markdownlint.json"
        config_file.write_text('{"default": true}')

        # 切换到临时目录
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            files = [Path("test.md")]
            cmd_args = build_markdownlint_command("markdownlint", files)

            assert cmd_args[0] == "markdownlint"
            assert "--config" in cmd_args
            assert ".markdownlint.json" in cmd_args
            assert "test.md" in cmd_args
        finally:
            os.chdir(old_cwd)


class TestReadFileContent:
    """测试文件读取功能"""

    def test_read_file_content_success(self, tmp_path: Path) -> None:
        """测试成功读取文件"""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test content")

        content = read_file_content(test_file)
        assert content == "# Test content"

    def test_read_file_content_not_found(self, tmp_path: Path) -> None:
        """测试文件不存在"""
        test_file = tmp_path / "nonexistent.md"

        with pytest.raises(FileReadError) as exc_info:
            read_file_content(test_file)

        assert "文件不存在" in str(exc_info.value)


class TestIsRuleFile:
    """测试规则文件判断功能"""

    def test_is_rule_file_rulesets(self) -> None:
        """测试 rulesets 路径"""
        file_path = Path("rulesets/01-general.md")
        assert is_rule_file(file_path) is True

    def test_is_rule_file_rules(self) -> None:
        """测试 rules 路径"""
        file_path = Path(".cursor/rules/01-general.md")
        assert is_rule_file(file_path) is True

    def test_is_rule_file_coderules(self) -> None:
        """测试 coderules 路径（向后兼容）"""
        file_path = Path(".cursor/coderules/01-general.md")
        assert is_rule_file(file_path) is True

    def test_is_rule_file_non_rule(self) -> None:
        """测试非规则文件"""
        file_path = Path("docs/guide.md")
        assert is_rule_file(file_path) is False


class TestCheckFilenameFormat:
    """测试文件名格式检查功能"""

    def test_check_filename_format_valid(self, tmp_path: Path) -> None:
        """测试有效的文件名格式"""
        test_file = tmp_path / "rulesets" / "01-general.md"
        test_file.parent.mkdir()

        error = check_filename_format(test_file)
        assert error is None

    def test_check_filename_format_invalid(self, tmp_path: Path) -> None:
        """测试无效的文件名格式"""
        test_file = tmp_path / "rulesets" / "general.md"  # 缺少数字前缀
        test_file.parent.mkdir()

        error = check_filename_format(test_file)
        assert error is not None
        assert "文件名格式错误" in error

    def test_check_filename_format_non_rule_file(self, tmp_path: Path) -> None:
        """测试非规则文件不检查文件名格式"""
        test_file = tmp_path / "docs" / "guide.md"
        test_file.parent.mkdir()

        error = check_filename_format(test_file)
        assert error is None


class TestCheckHeaderLevels:
    """测试标题层级检查功能"""

    def test_check_header_levels_valid(self) -> None:
        """测试有效的标题层级"""
        content = """# Level 1
## Level 2
### Level 3
#### Level 4
"""
        errors = check_header_levels(content)
        assert len(errors) == 0

    def test_check_header_levels_too_deep(self) -> None:
        """测试标题层级过深"""
        content = """# Level 1
## Level 2
### Level 3
#### Level 4
##### Level 5
"""
        errors = check_header_levels(content)
        assert len(errors) > 0
        assert any("标题层级过深" in err for err in errors)


class TestCheckHeaderSkipping:
    """测试标题跳级检查功能"""

    def test_check_header_skipping_valid(self) -> None:
        """测试有效的标题层级（无跳级）"""
        content = """# Level 1
## Level 2
### Level 3
"""
        errors = check_header_skipping(content)
        assert len(errors) == 0

    def test_check_header_skipping_invalid(self) -> None:
        """测试标题跳级"""
        content = """# Level 1
### Level 3  # 跳过了 Level 2
"""
        errors = check_header_skipping(content)
        assert len(errors) > 0
        assert any("标题跳级" in err for err in errors)


class TestCheckCodeBlockLanguageTags:
    """测试代码块语言标签检查功能"""

    def test_check_code_block_with_lang(self) -> None:
        """测试代码块有语言标签"""
        content = """Some text

```python
code with language
```
"""
        errors = check_code_block_language_tags(content)
        assert len(errors) == 0

    def test_check_code_block_missing_lang(self) -> None:
        """测试代码块缺少语言标签"""
        content = """Some text

```
code without language
```

```python
code with language
```
"""
        errors = check_code_block_language_tags(content)
        assert len(errors) > 0
        assert any("代码块缺少语言标签" in err for err in errors)


class TestCheckMarkdownlint:
    """测试 markdownlint 检查功能"""

    @patch("lint_md.find_markdownlint_command")
    @patch("lint_md.subprocess.run")
    def test_check_success(self, mock_run: MagicMock, mock_find_cmd: MagicMock) -> None:
        """测试成功检查文件"""
        mock_find_cmd.return_value = "markdownlint"
        mock_run.return_value = MagicMock(
            returncode=0, stdout="", stderr=""
        )

        test_file = Path("test.md")
        returncode, output = check_markdownlint([test_file])

        assert returncode == 0
        mock_run.assert_called_once()

    @patch("lint_md.find_markdownlint_command")
    def test_check_command_not_found(self, mock_find_cmd: MagicMock) -> None:
        """测试命令未找到时抛出异常"""
        mock_find_cmd.return_value = None

        test_file = Path("test.md")
        with pytest.raises(MarkdownLintNotFoundError) as exc_info:
            check_markdownlint([test_file])

        assert "未找到 markdownlint 命令" in str(exc_info.value)

    @patch("lint_md.find_markdownlint_command")
    @patch("lint_md.subprocess.run")
    def test_check_with_errors(self, mock_run: MagicMock, mock_find_cmd: MagicMock) -> None:
        """测试检查发现错误"""
        mock_find_cmd.return_value = "markdownlint"
        mock_run.return_value = MagicMock(
            returncode=1, stdout="error message", stderr=""
        )

        test_file = Path("test.md")
        returncode, output = check_markdownlint([test_file])

        assert returncode == 1
        assert "error message" in output

    @patch("lint_md.find_markdownlint_command")
    @patch("lint_md.subprocess.run")
    def test_check_timeout(self, mock_run: MagicMock, mock_find_cmd: MagicMock) -> None:
        """测试执行超时"""
        mock_find_cmd.return_value = "markdownlint"
        mock_run.side_effect = subprocess.TimeoutExpired("markdownlint", 60)

        test_file = Path("test.md")
        with pytest.raises(MarkdownLintExecutionError) as exc_info:
            check_markdownlint([test_file])

        assert "执行超时" in str(exc_info.value)


class TestCheckProjectSpecificRules:
    """测试项目特定规则检查"""

    def test_check_filename_format_valid(self, tmp_path: Path) -> None:
        """测试有效的文件名格式"""
        test_file = tmp_path / "rulesets" / "01-general.md"
        test_file.parent.mkdir()
        test_file.write_text("# Test")

        errors = check_project_specific_rules(test_file)
        assert len(errors) == 0

    def test_check_filename_format_invalid(self, tmp_path: Path) -> None:
        """测试无效的文件名格式"""
        test_file = tmp_path / "rulesets" / "general.md"  # 缺少数字前缀
        test_file.parent.mkdir()
        test_file.write_text("# Test")

        errors = check_project_specific_rules(test_file)
        assert len(errors) > 0
        assert any("文件名格式错误" in err for err in errors)

    def test_check_header_level_too_deep(self, tmp_path: Path) -> None:
        """测试标题层级过深"""
        test_file = tmp_path / "test.md"
        content = """# Level 1
## Level 2
### Level 3
#### Level 4
##### Level 5
"""
        test_file.write_text(content)

        errors = check_project_specific_rules(test_file)
        assert len(errors) > 0
        assert any("标题层级过深" in err for err in errors)

    def test_check_header_skip_level(self, tmp_path: Path) -> None:
        """测试标题跳级"""
        test_file = tmp_path / "test.md"
        content = """# Level 1
### Level 3  # 跳过了 Level 2
"""
        test_file.write_text(content)

        errors = check_project_specific_rules(test_file)
        assert len(errors) > 0
        assert any("标题跳级" in err for err in errors)

    def test_check_code_block_missing_lang(self, tmp_path: Path) -> None:
        """测试代码块缺少语言标签"""
        test_file = tmp_path / "test.md"
        content = """Some text

```
code without language
```

```python
code with language
```
"""
        test_file.write_text(content)

        errors = check_project_specific_rules(test_file)
        assert len(errors) > 0
        assert any("代码块缺少语言标签" in err for err in errors)

    def test_check_code_block_with_lang(self, tmp_path: Path) -> None:
        """测试代码块有语言标签"""
        test_file = tmp_path / "test.md"
        content = """Some text

```python
code with language
```
"""
        test_file.write_text(content)

        errors = check_project_specific_rules(test_file)
        # 不应该有代码块相关的错误
        code_block_errors = [e for e in errors if "代码块" in e]
        assert len(code_block_errors) == 0

    def test_check_non_rule_file_ignores_filename(self, tmp_path: Path) -> None:
        """测试非规则文件不检查文件名格式"""
        test_file = tmp_path / "docs" / "guide.md"
        test_file.parent.mkdir()
        test_file.write_text("# Guide")

        errors = check_project_specific_rules(test_file)
        # 不应该有文件名格式错误
        filename_errors = [e for e in errors if "文件名格式错误" in e]
        assert len(filename_errors) == 0

    def test_check_file_read_error(self, tmp_path: Path) -> None:
        """测试文件读取错误"""
        test_file = tmp_path / "nonexistent.md"
        # 文件不存在

        errors = check_project_specific_rules(test_file)
        assert len(errors) > 0
        assert "无法读取文件" in errors[0]


class TestFilterMarkdownFiles:
    """测试文件过滤功能"""

    def test_filter_markdown_files(self, tmp_path: Path) -> None:
        """测试过滤 Markdown 文件"""
        md_file = tmp_path / "test.md"
        mdc_file = tmp_path / "test.mdc"
        txt_file = tmp_path / "test.txt"
        nonexistent = tmp_path / "nonexistent.md"

        md_file.write_text("# Test")
        mdc_file.write_text("# Test")
        txt_file.write_text("Not markdown")

        files = [md_file, mdc_file, txt_file, nonexistent]
        result = filter_markdown_files(files)

        assert len(result) == 2
        assert md_file in result
        assert mdc_file in result
        assert txt_file not in result
        assert nonexistent not in result


class TestLintMarkdownFiles:
    """测试 lint 主函数"""

    @patch("lint_md.check_markdownlint")
    def test_lint_success(self, mock_check: MagicMock) -> None:
        """测试成功检查"""
        mock_check.return_value = (0, "")

        test_file = Path("test.md")
        result = lint_markdown_files([test_file], check_only=True)

        assert result == 0
        mock_check.assert_called_once()

    @patch("lint_md.check_markdownlint")
    @patch("lint_md.check_project_specific_rules")
    def test_lint_with_project_errors(self, mock_project: MagicMock, mock_check: MagicMock) -> None:
        """测试项目特定规则错误"""
        mock_check.return_value = (0, "")
        mock_project.return_value = ["文件名格式错误"]

        test_file = Path("rulesets") / "invalid.md"
        result = lint_markdown_files([test_file], check_only=True)

        assert result == 1

    def test_lint_no_markdown_files(self, capsys: "CaptureFixture[str]") -> None:
        """测试没有 Markdown 文件"""
        test_file = Path("test.txt")
        result = lint_markdown_files([test_file], check_only=True)

        assert result == 1
        captured = capsys.readouterr()
        assert "没有找到 Markdown 文件" in captured.err

    @patch("lint_md.check_markdownlint")
    def test_lint_markdownlint_errors(self, mock_check: MagicMock) -> None:
        """测试 markdownlint 发现错误"""
        mock_check.return_value = (1, "formatting errors")

        test_file = Path("test.md")
        result = lint_markdown_files([test_file], check_only=True)

        assert result == 1

    @patch("lint_md.check_markdownlint")
    def test_lint_handles_markdownlint_not_found(self, mock_check: MagicMock) -> None:
        """测试处理 markdownlint 未找到异常"""
        mock_check.side_effect = MarkdownLintNotFoundError("未找到命令")

        test_file = Path("test.md")
        result = lint_markdown_files([test_file], check_only=True)

        assert result == 1

    @patch("lint_md.check_markdownlint")
    def test_lint_handles_execution_error(self, mock_check: MagicMock) -> None:
        """测试处理执行错误异常"""
        mock_check.side_effect = MarkdownLintExecutionError("执行错误")

        test_file = Path("test.md")
        result = lint_markdown_files([test_file], check_only=True)

        assert result == 1


class TestMain:
    """测试主函数"""

    @patch("lint_md.lint_markdown_files")
    def test_main_success(self, mock_lint: MagicMock) -> None:
        """测试主函数成功执行"""
        mock_lint.return_value = 0

        test_file = Path("test.md")
        with patch("sys.argv", ["lint-md.py", str(test_file)]):
            result = main()
            assert result == 0

    @patch("lint_md.lint_markdown_files")
    def test_main_with_check_flag(self, mock_lint: MagicMock) -> None:
        """测试主函数使用 --check 标志"""
        mock_lint.return_value = 0

        test_file = Path("test.md")
        with patch("sys.argv", ["lint-md.py", "--check", str(test_file)]):
            result = main()
            assert result == 0
            mock_lint.assert_called_once()
