# storage.py

import csv
from pathlib import Path

from models import Task, Workband


class TaskManager:
    """Handles all CSV I/O for the to-do list."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.fieldnames = [
            "Task Number",
            "Task Name",
            "Description",
            "Workband",
            "Completed",
        ]

    def load_tasks(self) -> list[Task]:
        """Read all tasks from CSV. Returns empty list if file doesn't exist."""
        if not self.filepath.exists():
            return []
        with open(self.filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            return [
                Task(
                    number=int(row["Task Number"]),
                    name=row["Task Name"],
                    description=row["Description"],
                    workband=Workband(row["Workband"]),
                    completed=(row["Completed"] == "True"),
                )
                for row in reader
            ]

    def _save_tasks(self, tasks: list[Task]) -> None:
        """Overwrite CSV with the given task list."""
        with open(self.filepath, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for task in tasks:
                writer.writerow(
                    {
                        "Task Number": task.number,
                        "Task Name": task.name,
                        "Description": task.description,
                        "Workband": task.workband.value,
                        "Completed": "True" if task.completed else "False",
                    }
                )

    def next_task_number(self) -> int:
        """Return the next available task number (current max + 1)."""
        tasks = self.load_tasks()
        return len(tasks) + 1

    def add_task(self, task: Task) -> None:
        """Create and save a new task."""
        tasks = self.load_tasks()
        tasks.append(task)
        self._save_tasks(tasks)

    def update_task(self, updated_task: Task) -> None:
        tasks = self.load_tasks()
        for idx, task in enumerate(tasks):
            if task.number == updated_task.number:
                tasks[idx] = updated_task
                break
        self._save_tasks(tasks)

    def delete_task(self, task_number: int) -> bool:
        tasks = self.load_tasks()
        for idx, task in enumerate(tasks):
            if task.number == task_number:
                tasks.pop(idx)
                self._save_tasks(tasks)
                return True
        return False
