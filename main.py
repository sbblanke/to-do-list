# main.py
import csv
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
p = SCRIPT_DIR / "tasks.csv"

next_selection = "What would you like to do next?"


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


def _format_row(row: list[str], widths: list[int]) -> str:
    return "".join(cell.ljust(widths[i]) for i, cell in enumerate(row))


def display_tasks(show_menu: bool = True, show_completed: bool = False) -> None:
    no_tasks = "No tasks have been created yet."
    if not p.exists():
        print(no_tasks)
    else:
        with open(p, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            if not rows:
                print(no_tasks)
                return

            column_widths = []
            for fieldname in reader.fieldnames:
                header_len = len(fieldname)
                max_length = max((len(row[fieldname]) for row in rows), default=0)
                column_widths.append(max(header_len, max_length) + 2)

            formatted_header = ""
            for idx, fieldname in enumerate(reader.fieldnames):
                formatted_header += fieldname.ljust(column_widths[idx])
            print(formatted_header)
            print("-" * sum(column_widths))

            row_counter = 0
            for row in rows:
                is_completed = row["Completed"] == "True"

                if show_completed != is_completed:
                    continue  # skip rows that don't match intent from show_completed

                print(_format_row(list(row.values()), column_widths))
                row_counter += 1

            if row_counter == 0:
                print("No tasks are currently pending.")

    if show_menu:
        print(next_selection)


def add_task():
    add_name = input("What would you like to call this task? ")
    while not add_name:
        add_name = input("Please enter a name for this task: ")

    # Optional - null input should be accepted
    add_description = input("Add any relevant details about this task. ")

    accepted_workbands = ["Now", "Next", "Later", "Blocked"]
    accepted_workbands_lower = []
    for wb in accepted_workbands:
        accepted_workbands_lower.append(wb.lower())

    raw_workband = input("Which workband status applies to this task? ")

    while raw_workband.lower() not in accepted_workbands_lower:
        raw_workband = input(f"Value must be in {accepted_workbands}: ")

    for idx, workband in enumerate(accepted_workbands):
        if raw_workband.lower() == workband.lower():
            add_workband = workband
    print("Task Added!")

    if p.exists():
        with open(p, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 1
            for row in reader:
                counter += 1

        with open(p, "a", newline="") as tasks:
            fieldnames = [
                "Task Number",
                "Task Name",
                "Description",
                "Workband",
                "Completed",
            ]
            writer = csv.DictWriter(tasks, fieldnames=fieldnames)
            writer.writerow(
                {
                    "Task Number": counter,
                    "Task Name": add_name,
                    "Description": add_description,
                    "Workband": add_workband,
                    "Completed": False,
                }
            )

    else:
        with open(p, "w", newline="") as tasks:
            fieldnames = [
                "Task Number",
                "Task Name",
                "Description",
                "Workband",
                "Completed",
            ]
            writer = csv.DictWriter(tasks, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(
                {
                    "Task Number": "1",
                    "Task Name": add_name,
                    "Description": add_description,
                    "Workband": add_workband,
                    "Completed": False,
                }
            )

    print(next_selection)


def complete_task():
    if p.exists():
        display_tasks(show_completed=False, show_menu=False)
        with open(p, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            pending_task_exists = False
            selected_task_found = False

            for row in rows:
                if row["Completed"] == "False":
                    pending_task_exists = True

            if pending_task_exists:
                selection = input("Which task did you complete?\n")
                for row in rows:
                    if row["Task Number"] == selection and row["Completed"] == False:
                        row["Completed"] = "True"
                        selected_task_found = True

                if selected_task_found:
                    with open(p, "w", newline="") as csvfile:
                        fieldnames = [
                            "Task Number",
                            "Task Name",
                            "Description",
                            "Workband",
                            "Completed",
                        ]
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(rows)

                        print("Task completed. Nice job!")

                else:
                    print("Selected task not pending. Task not adjusted.")
    else:
        print("Add a task first!")

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
            add_task()
        elif selection == "4":
            complete_task()
        else:
            print("Please select a valid number.")

    print("Be productive and come back soon!")


if __name__ == "__main__":
    main()
