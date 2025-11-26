#!/usr/bin/env python3
"""
测试 format-md.py 脚本
"""

import importlib.util
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture

# 动态导入 scripts 模块
scripts_dir = Path(__file__).parent.parent / "scripts"
spec = importlib.util.spec_from_file_location("format_md", scripts_dir / "format-md.py")
format_md = importlib.util.module_from_spec(spec)
spec.loader.exec_module(format_md)

# 导入函数和异常类
find_markdownlint_command = format_md.find_markdownlint_command
build_markdownlint_command = format_md.build_markdownlint_command
format_markdown_files = format_md.format_markdown_files
filter_markdown_files = format_md.filter_markdown_files
main = format_md.main
MarkdownLintNotFoundError = format_md.MarkdownLintNotFoundError
MarkdownLintExecutionError = format_md.MarkdownLintExecutionError


class TestFindMarkdownlintCommand:
    """测试命令检测功能"""

    @patch("format_md.subprocess.run")
    def test_find_markdownlint_success(self, mock_run: MagicMock) -> None:
        """测试成功找到 markdownlint 命令"""
        mock_run.return_value = MagicMock(returncode=0)
        result = find_markdownlint_command()
        assert result == "markdownlint"
        mock_run.assert_called()

    @patch("format_md.subprocess.run")
    def test_find_markdownlint_cli2_fallback(self, mock_run: MagicMock) -> None:
        """测试回退到 markdownlint-cli2"""
        # 第一次调用失败（markdownlint 不存在）
        # 第二次调用成功（markdownlint-cli2 存在）
        mock_run.side_effect = [
            FileNotFoundError(),
            MagicMock(returncode=0),
        ]
        result = find_markdownlint_command()
        assert result == "markdownlint-cli2"
        assert mock_run.call_count == 2

    @patch("format_md.subprocess.run")
    def test_find_markdownlint_not_found(self, mock_run: MagicMock) -> None:
        """测试未找到任何命令"""
        mock_run.side_effect = FileNotFoundError()
        result = find_markdownlint_command()
        assert result is None

    @patch("format_md.subprocess.run")
    def test_find_markdownlint_timeout(self, mock_run: MagicMock) -> None:
        """测试命令执行超时"""
        mock_run.side_effect = subprocess.TimeoutExpired("markdownlint", 5)
        result = find_markdownlint_command()
        assert result is None


class TestBuildMarkdownlintCommand:
    """测试命令构建功能"""

    def test_build_command_with_fix(self) -> None:
        """测试构建包含 --fix 的命令"""
        files = [Path("test.md")]
        cmd_args = build_markdownlint_command("markdownlint", files, fix=True)

        assert cmd_args[0] == "markdownlint"
        assert "--fix" in cmd_args
        assert "test.md" in cmd_args

    def test_build_command_without_fix(self) -> None:
        """测试构建不包含 --fix 的命令"""
        files = [Path("test.md")]
        cmd_args = build_markdownlint_command("markdownlint", files, fix=False)

        assert cmd_args[0] == "markdownlint"
        assert "--fix" not in cmd_args
        assert "test.md" in cmd_args

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
            cmd_args = build_markdownlint_command("markdownlint", files, fix=True)

            assert "--config" in cmd_args
            assert ".markdownlint.json" in cmd_args
        finally:
            os.chdir(old_cwd)

    def test_build_command_without_config(self, tmp_path: Path) -> None:
        """测试构建不包含配置文件的命令"""
        # 确保配置文件不存在
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            files = [Path("test.md")]
            cmd_args = build_markdownlint_command("markdownlint", files, fix=True)

            assert "--config" not in cmd_args
        finally:
            os.chdir(old_cwd)


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


class TestFormatMarkdownFiles:
    """测试格式化功能"""

    @patch("format_md.find_markdownlint_command")
    @patch("format_md.subprocess.run")
    def test_format_success(
        self, mock_run: MagicMock, mock_find_cmd: MagicMock
    ) -> None:
        """测试成功格式化文件"""
        mock_find_cmd.return_value = "markdownlint"
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        test_file = Path("test.md")
        result = format_markdown_files([test_file], fix=True)

        assert result == 0
        mock_run.assert_called_once()
        # 检查是否包含 --fix 参数
        call_args = mock_run.call_args[0][0]
        assert "--fix" in call_args

    @patch("format_md.find_markdownlint_command")
    def test_format_command_not_found(self, mock_find_cmd: MagicMock) -> None:
        """测试命令未找到时抛出异常"""
        mock_find_cmd.return_value = None

        test_file = Path("test.md")
        with pytest.raises(MarkdownLintNotFoundError) as exc_info:
            format_markdown_files([test_file], fix=True)

        assert "未找到 markdownlint 命令" in str(exc_info.value)

    @patch("format_md.find_markdownlint_command")
    @patch("format_md.subprocess.run")
    def test_format_with_config(
        self, mock_run: MagicMock, mock_find_cmd: MagicMock, tmp_path: Path
    ) -> None:
        """测试使用配置文件"""
        mock_find_cmd.return_value = "markdownlint"
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        # 创建临时配置文件
        config_file = tmp_path / ".markdownlint.json"
        config_file.write_text('{"default": true}')

        # 切换到临时目录
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            test_file = tmp_path / "test.md"
            test_file.write_text("# Test")

            result = format_markdown_files([test_file], fix=True)

            assert result == 0
            # 检查是否包含 --config 参数
            call_args = mock_run.call_args[0][0]
            assert "--config" in call_args
        finally:
            os.chdir(old_cwd)

    @patch("format_md.find_markdownlint_command")
    @patch("format_md.subprocess.run")
    def test_format_check_mode(
        self, mock_run: MagicMock, mock_find_cmd: MagicMock
    ) -> None:
        """测试检查模式（不修复）"""
        mock_find_cmd.return_value = "markdownlint"
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        test_file = Path("test.md")
        result = format_markdown_files([test_file], fix=False)

        assert result == 0
        # 检查模式不应该包含 --fix
        call_args = mock_run.call_args[0][0]
        assert "--fix" not in call_args

    @patch("format_md.find_markdownlint_command")
    @patch("format_md.subprocess.run")
    def test_format_timeout(
        self, mock_run: MagicMock, mock_find_cmd: MagicMock
    ) -> None:
        """测试执行超时"""
        mock_find_cmd.return_value = "markdownlint"
        mock_run.side_effect = subprocess.TimeoutExpired("markdownlint", 60)

        test_file = Path("test.md")
        with pytest.raises(MarkdownLintExecutionError) as exc_info:
            format_markdown_files([test_file], fix=True)

        assert "执行超时" in str(exc_info.value)

    @patch("format_md.find_markdownlint_command")
    @patch("format_md.subprocess.run")
    def test_format_subprocess_error(
        self, mock_run: MagicMock, mock_find_cmd: MagicMock
    ) -> None:
        """测试 subprocess 错误"""
        mock_find_cmd.return_value = "markdownlint"
        mock_run.side_effect = subprocess.SubprocessError("subprocess error")

        test_file = Path("test.md")
        with pytest.raises(MarkdownLintExecutionError) as exc_info:
            format_markdown_files([test_file], fix=True)

        assert "执行 markdownlint 时出错" in str(exc_info.value)


class TestMain:
    """测试主函数"""

    @patch("format_md.format_markdown_files")
    def test_main_success(self, mock_format: MagicMock) -> None:
        """测试主函数成功执行"""
        mock_format.return_value = 0

        test_file = Path("test.md")
        with patch("sys.argv", ["format-md.py", str(test_file)]):
            result = main()
            assert result == 0

    @patch("format_md.format_markdown_files")
    def test_main_with_check_flag(self, mock_format: MagicMock) -> None:
        """测试主函数使用 --check 标志"""
        mock_format.return_value = 0

        test_file = Path("test.md")
        with patch("sys.argv", ["format-md.py", "--check", str(test_file)]):
            result = main()
            assert result == 0
            # 检查是否以检查模式调用
            mock_format.assert_called_once()
            call_args = mock_format.call_args
            assert call_args[1]["fix"] is False

    def test_main_no_files(self, capsys: "CaptureFixture[str]") -> None:
        """测试主函数没有文件"""
        with patch("sys.argv", ["format-md.py", "nonexistent.md"]):
            result = main()
            assert result == 1
            captured = capsys.readouterr()
            assert "没有找到有效的文件" in captured.err

    def test_main_no_markdown_files(
        self, capsys: "CaptureFixture[str]", tmp_path: Path
    ) -> None:
        """测试主函数没有 Markdown 文件"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("not markdown")

        with patch("sys.argv", ["format-md.py", str(test_file)]):
            result = main()
            assert result == 1
            captured = capsys.readouterr()
            assert "没有找到 Markdown 文件" in captured.err

    @patch("format_md.format_markdown_files")
    def test_main_handles_markdownlint_not_found(self, mock_format: MagicMock) -> None:
        """测试主函数处理 markdownlint 未找到异常"""
        mock_format.side_effect = MarkdownLintNotFoundError("未找到命令")

        test_file = Path("test.md")
        with patch("sys.argv", ["format-md.py", str(test_file)]):
            result = main()
            assert result == 1

    @patch("format_md.format_markdown_files")
    def test_main_handles_execution_error(self, mock_format: MagicMock) -> None:
        """测试主函数处理执行错误异常"""
        mock_format.side_effect = MarkdownLintExecutionError("执行错误")

        test_file = Path("test.md")
        with patch("sys.argv", ["format-md.py", str(test_file)]):
            result = main()
            assert result == 1
