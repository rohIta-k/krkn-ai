import subprocess
from unittest.mock import patch, Mock, mock_open
from krkn_ai.dashboard.manager import DashboardManager


def test_start_background_success():
    with patch("subprocess.Popen") as mock_popen, patch("builtins.open", mock_open()):
        mock_process = Mock()
        mock_process.wait.side_effect = subprocess.TimeoutExpired(cmd="cmd", timeout=2)
        mock_popen.return_value = mock_process

        result = DashboardManager.start("/tmp", 8080, background=True)
        assert result is mock_process
        mock_popen.assert_called_once()


def test_start_background_immediate_exit():
    with (
        patch("subprocess.Popen") as mock_popen,
        patch("builtins.open", mock_open(read_data="error msg")),
    ):
        mock_process = Mock()
        mock_process.wait.return_value = 1
        mock_popen.return_value = mock_process

        result = DashboardManager.start("/tmp", 8080, background=True)
        assert result is None
        mock_popen.assert_called_once()


def test_start_foreground_success():
    with patch("subprocess.run") as mock_run:
        result = DashboardManager.start("/tmp", 8080, background=False)
        assert result is None
        mock_run.assert_called_once()


def test_start_foreground_keyboard_interrupt():
    with patch("subprocess.run", side_effect=KeyboardInterrupt):
        result = DashboardManager.start("/tmp", 8080, background=False)
        assert result is None


def test_start_exception():
    with patch("subprocess.run", side_effect=Exception("Failed")):
        result = DashboardManager.start("/tmp", 8080, background=False)
        assert result is None
