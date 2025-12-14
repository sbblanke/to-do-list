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
        "4. Complete a task\n"
        "0. Exit program\n"
        "\n"
        "Enter your desired number: "
    )
    if not selection:
        return None

    return selection


def view_pending_tasks(show_menu=True):
    if not p.exists():
        print("No tasks have been created yet.")
    else:
        with open(p, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            rows = list(reader)

            if not rows:
                print("No tasks have been created yet.")
                return

            header_row = rows[0]
            data_rows = rows[1:]
            num_columns = len(header_row)
            column_widths = []

            for col in range(num_columns):
                # Look at every cell in this column
                # and find the one with the longest value
                max_length = max(len(row[col]) for row in rows)
                column_widths.append(max_length + 2)  # added 2 for spacing

            formatted_header = ""
            for index, cell in enumerate(header_row):
                formatted_header += cell.ljust(column_widths[index])
            print(formatted_header)
            print("-" * sum(column_widths))

            row_counter = 0
            for row in data_rows:
                if row[3] == "False":
                    formatted_row = ""
                    for index, cell in enumerate(row):
                        formatted_row += cell.ljust(column_widths[index])
                    print(formatted_row)
                    row_counter += 1

            if row_counter == 0:
                print("No tasks are currently pending.")

    if show_menu:
        print(next_selection)


def view_completed_tasks(show_menu=True):
    if not p.exists():
        print("No tasks have been created yet.")
    else:
        with open(p, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            rows = list(reader)

            if not rows:
                print("No tasks have been created yet.")
                return

            header_row = rows[0]
            data_rows = rows[1:]
            num_columns = len(header_row)
            column_widths = []

            for col in range(num_columns):
                max_length = max(len(row[col]) for row in rows)
                column_widths.append(max_length + 2)

            formatted_header = ""
            for index, cell in enumerate(header_row):
                formatted_header += cell.ljust(column_widths[index])
            print(formatted_header)
            print("-" * sum(column_widths))

            row_counter = 0
            for row in data_rows:
                if row[3] == "True":
                    formatted_row = ""
                    for index, cell in enumerate(row):
                        formatted_row += cell.ljust(column_widths[index])
                    print(formatted_row)
                    row_counter += 1

            if row_counter == 0:
                print("No tasks have been completed yet.")

    if show_menu:
        print(next_selection)


def add_task():
    add_name = input("What would you like to call this task? ")
    while not add_name:
        add_name = input("Please enter a name for this task: ")

    # Optional - null input should be accepted
    add_description = input("Add any relevant details about this task. ")
    print("Task Added!")

    if p.exists():
        with open(p, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 1
            for row in reader:
                counter += 1

        with open(p, "a", newline="") as tasks:
            fieldnames = ["Task Number", "Task Name", "Description", "Completed"]
            writer = csv.DictWriter(tasks, fieldnames=fieldnames)
            writer.writerow(
                {
                    "Task Number": counter,
                    "Task Name": add_name,
                    "Description": add_description,
                    "Completed": False,
                }
            )

    else:
        with open(p, "w", newline="") as tasks:
            fieldnames = ["Task Number", "Task Name", "Description", "Completed"]
            writer = csv.DictWriter(tasks, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(
                {
                    "Task Number": "1",
                    "Task Name": add_name,
                    "Description": add_description,
                    "Completed": False,
                }
            )

    print(next_selection)


def complete_task():
    if p.exists():
        view_pending_tasks(show_menu=False)
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
                    if row["Task Number"] == selection:
                        if row["Completed"] == "False":
                            row["Completed"] = "True"
                            selected_task_found = True

                if selected_task_found:
                    with open(p, "w", newline="") as csvfile:
                        fieldnames = [
                            "Task Number",
                            "Task Name",
                            "Description",
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
        if selection == "0":
            break
        elif selection == "1":
            view_pending_tasks()
        elif selection == "2":
            view_completed_tasks()
        elif selection == "3":
            add_task()
        elif selection == "4":
            complete_task()
        else:
            print("Please select a valid number.")

    print("Be productive and come back soon!")


if __name__ == "__main__":
    main()
