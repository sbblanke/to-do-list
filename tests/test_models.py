from models import Task, Workband


def test_workband_values() -> None:
    assert Workband.NOW.value == "Now"
    assert Workband.BLOCKED.value == "Blocked"


def test_task_defaults() -> None:
    t = Task(number=1, name="x", description="", workband=Workband.NOW)
    assert not t.completed
