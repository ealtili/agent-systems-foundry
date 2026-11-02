from foundry.models import ToolResult
from foundry.progress_monitor import ProgressMonitor, ProgressVerdict


def test_tool_result_creation() -> None:
    res = ToolResult(success=True, output="ok")
    assert res.success is True
    assert res.output == "ok"


def test_progress_monitor_cycle() -> None:
    monitor = ProgressMonitor(max_steps=5)
    # Consecutive identical call should trigger exact repetition
    monitor.step("read_file", {"path": "a.py"}, "state_hash_1")
    verdict = monitor.step("read_file", {"path": "a.py"}, "state_hash_1")
    assert verdict == ProgressVerdict.EXACT_REPETITION
