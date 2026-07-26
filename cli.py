# cli.py

from pathlib import Path

from models import Task, Workband
from storage import TaskManager

SCRIPT_DIR = Path(__file__).parent
manager = TaskManager(SCRIPT_DIR / "tasks.csv")
next_selection = "What would you like to do next?"


def _format_row(row: list[str], widths: list[int]) -> str:
    return "".join(cell.ljust(widths[i]) for i, cell in enumerate(row))


def display_tasks(show_menu: bool = True, show_completed: bool = False) -> None:
    tasks = manager.load_tasks()

    if not tasks:
        print("No tasks have been created yet.")
        if show_menu:
            print(next_selection)
        return

    column_widths: list[int] = []
    for fieldname in manager.fieldnames:
        header_len: int = len(fieldname)
        data_max: int = 0
        for task in tasks:
            if fieldname == "Task Number":
                val = str(task.number)
            elif fieldname == "Task Name":
                val = task.name
            elif fieldname == "Description":
                val = task.description
            elif fieldname == "Workband":
                val = task.workband.value
            elif fieldname == "Completed":
                val = "True" if task.completed else "False"
            data_max = max(data_max, len(val))
        column_widths.append(max(header_len, data_max) + 2)

    formatted_header: str = ""
    for idx, fieldname in enumerate(manager.fieldnames):
        formatted_header += fieldname.ljust(column_widths[idx])
    print(formatted_header)
    print("-" * sum(column_widths))

    row_counter: int = 0
    for task in tasks:
        if show_completed != task.completed:
            continue
        row = [
            str(task.number),
            task.name,
            task.description,
            task.workband.value,
            "True" if task.completed else "False",
        ]
        print(_format_row(row, column_widths))
        row_counter += 1

    if row_counter == 0:
        if show_completed:
            print("No tasks have been completed yet.")
        else:
            print("No tasks are currently pending.")

    if show_menu:
        print(next_selection)


def menu() -> str | None:
    selection = input(
        "\n"
        "1. View all pending tasks\n"
        "2. View all completed tasks\n"
        "3. Add a task\n"
        "4. Complete a task\n\n"
        "D. Delete a task\n"
        "Q. Exit program\n"
        "\n"
        "Enter your selection: "
    )
    if not selection:
        return None

    return selection


def add_task_cli() -> None:
    name = input("What would you like to call this task? ")
    while not name:
        name = input("Please enter a name for this task: ")

    description = input("Add any relevant details about this task. ")

    while True:
        raw = input("Which workband status applies to this task? ").capitalize()
        try:
            add_workband = Workband(raw)
            break
        except ValueError:
            valid = ", ".join(wb.value for wb in Workband)
            print(f"Value must be one of: {valid}")

    task = Task(
        number=manager.next_task_number(),
        name=name,
        description=description,
        workband=add_workband,
    )
    manager.add_task(task)
    print("Task Added!")
    print(next_selection)


def delete_task_cli() -> None:
    display_tasks(show_completed=False, show_menu=False)
    raw = input("Which task do you want to delete? ")
    if not raw:
        print("Task not deleted.")
        print(next_selection)
        return

    confirmed = input("Are you sure? (y/N) ")
    if confirmed.lower() not in ("y", "yes"):
        print("Task not deleted.")
        print(next_selection)
        return

    if manager.delete_task(int(raw)):
        print("Task deleted.")
    else:
        print("Task not found.")

    print(next_selection)


def complete_task_cli() -> None:
    tasks: list[Task] = manager.load_tasks()
    pending: list[Task] = [t for t in tasks if not t.completed]

    if not pending:
        print("Add a task first!")
        print(next_selection)
        return

    display_tasks(show_completed=False, show_menu=False)
    selection: str = input("Which task did you complete?\n")

    for task in tasks:
        if str(task.number) == selection and not task.completed:
            task.completed = True
            manager.update_task(task)
            print("Task completed. Nice job!")
            print(next_selection)
            return

    print("Selected task not pending. Task not adjusted.")
    print(next_selection)


def main() -> None:
    print("Welcome to your to-do list!\n")
    print("What would you like to do first?")
    while True:
        selection = menu()
        valid = ["1", "2", "3", "4", "d", "q"]
        if selection is None or selection.lower() not in valid:
            print("Please select a valid option.")
            continue

        selection = selection.lower()
        if selection == "q":
            break
        elif selection == "1":
            display_tasks(show_completed=False)
        elif selection == "2":
            display_tasks(show_completed=True)
        elif selection == "3":
            add_task_cli()
        elif selection == "4":
            complete_task_cli()
        elif selection == "d":
            delete_task_cli()

    print("Be productive and come back soon!")


if __name__ == "__main__":
    main()
