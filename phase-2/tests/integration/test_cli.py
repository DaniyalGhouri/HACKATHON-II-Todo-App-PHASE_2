import subprocess
import pytest
import sys

def run_cli_interactive(inputs):
    """Helper to run interactive CLI via subprocess"""
    cmd = [sys.executable, "-m", "src.cli.main"]
    # Join inputs with newlines and ensure a trailing newline
    input_str = "\n".join(inputs) + "\n"
    # Use timeout to prevent hanging if logic breaks
    result = subprocess.run(
        cmd, 
        input=input_str,
        capture_output=True, 
        text=True,
        timeout=2
    )
    return result

def test_add_command():
    # 1=Add, "Buy milk"=Description, 7=Exit
    result = run_cli_interactive(["1", "Buy milk", "7"])
    assert result.returncode == 0
    assert "Task added. ID: 1" in result.stdout

def test_list_command_empty():
    # 2=List, 7=Exit
    result = run_cli_interactive(["2", "7"])
    assert result.returncode == 0
    assert "No tasks found." in result.stdout

def test_complete_command_not_found():
    # 5=Mark Complete, 999=ID, 7=Exit
    result = run_cli_interactive(["5", "999", "7"])
    assert result.returncode == 0
    assert "Error: Task ID 999 not found" in result.stderr

def test_update_command_not_found():
    # 3=Update, 999=ID, "New desc"=Description, 7=Exit
    result = run_cli_interactive(["3", "999", "New desc", "7"])
    assert result.returncode == 0
    assert "Error: Task ID 999 not found" in result.stderr

def test_delete_command_not_found():
    # 4=Delete, 999=ID, 7=Exit
    result = run_cli_interactive(["4", "999", "7"])
    assert result.returncode == 0
    assert "Error: Task ID 999 not found" in result.stderr
