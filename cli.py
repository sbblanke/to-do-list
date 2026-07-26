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
    tasks = manager._load_tasks()

    if not tasks:
        print("No tasks have been created yet.")
        if show_menu:
            print(next_selection)
        return

    column_widths = []
    for fieldname in manager.fieldnames:
        header_len = len(fieldname)
        data_max = 0
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

    formatted_header = ""
    for idx, fieldname in enumerate(manager.fieldnames):
        formatted_header += fieldname.ljust(column_widths[idx])
    print(formatted_header)
    print("-" * sum(column_widths))

    row_counter = 0
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
        print("No tasks are currently pending.")

    if show_menu:
        print(next_selection)


def menu():
    selection = input(
        "\n"
        "1. View all pending tasks\n"
        "2. View all completed tasks\n"
        "3. Add a task\n"
        "4. Complete a task\n\n"
        "Q. Exit program\n"
        "\n"
        "Enter your selection: "
    )
    if not selection:
        return None

    return selection


def add_task_cli():
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
        workband=Workband(add_workband.capitalize()),
    )
    manager.add_task(task)
    print("Task Added!")
    print(next_selection)


def complete_task_cli():
    tasks = manager.load_tasks()
    pending = [t for t in tasks if not t.completed]

    if not pending:
        print("Add a task first!")
        print(next_selection)
        return

    display_tasks(show_completed=False, show_menu=False)
    selection = input("Which task did you complete?\n")

    for task in tasks:
        if str(task.number) == selection and not task.completed:
            task.completed = True
            manager.update_task(task)
            print("Task completed. Nice job!")
            print(next_selection)
            return

    print("Selected task not pending. Task not adjusted.")
    print(next_selection)


def main():
    print("Welcome to your to-do list!\n")
    print("What would you like to do first?")
    while True:
        selection = menu()
        if selection == "Q" or selection == "q":
            break
        elif selection == "1":
            display_tasks(show_completed=False)
        elif selection == "2":
            display_tasks(show_completed=True)
        elif selection == "3":
            manager.add_task()
        elif selection == "4":
            manager.complete_task()
        else:
            print("Please select a valid number.")

    print("Be productive and come back soon!")


if __name__ == "__main__":
    main()
