# main.py
import csv
from pathlib import Path

p = Path("tasks.csv")


def menu():
    selection = input(
        "\n"
        "1. View all pending tasks\n"
        "2. View all completed tasks\n"
        "3. Add a task\n"
        "4. Complete a task\n"
        "0. Exit program\n"
        "\n"
        "User Selection: "
    )
    if not selection:
        raise ValueError("\nMust select an option\n")

    selection = selection.lower()
    selection = selection.lstrip()
    selection = selection.rstrip()

    if selection == "view all pending tasks" or selection == "1":
        view_pending_tasks()
    elif selection == "view all completed tasks" or selection == "2":
        view_completed_tasks()
    elif selection == "add a task" or selection == "3":
        add_task()
    elif selection == "complete a task" or selection == "4":
        complete_task()
    elif selection == "exit program" or selection == "0":
        return "Session Ended by User."
    else:
        print("Invalid selection. Please try again.")
        print()
        menu()
        print()


def secondary_menu():
    print("What would you like to do next?")
    menu()


def view_pending_tasks(show_menu=True):
    if not p.exists():
        print("No tasks have been created yet!")
    else:
        with open("tasks.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            rows = list(reader)

            if not rows:
                print("No tasks have been created yet!")
                secondary_menu()
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
                if row[3] == "False":
                    formatted_row = ""
                    for index, cell in enumerate(row):
                        formatted_row += cell.ljust(column_widths[index])
                    print(formatted_row)
                    row_counter += 1

            if row_counter == 0:
                print("All tasks have already been completed!")

    if show_menu:
        secondary_menu()


def view_completed_tasks(show_menu=True):
    if not p.exists():
        print("No tasks have been created yet!")
    else:
        with open("tasks.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            rows = list(reader)

            if not rows:
                print("No tasks have been created yet!")
                secondary_menu()
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
        secondary_menu()


def add_task():
    add_name = input("What would you like to call this task? ")
    while not add_name:
        add_name = input("Please enter a name for this task: ")

    # Optional - null input should be accepted
    add_description = input("Add any relevant details about this task. ")

    if p.exists() is True:
        with open("tasks.csv", "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 1
            for row in reader:
                counter += 1

        with open("tasks.csv", "a", newline="") as tasks:
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

    if p.exists() is False:
        with open("tasks.csv", "w", newline="") as tasks:
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

    secondary_menu()


def complete_task():
    view_pending_tasks(show_menu=False)
    selection = input("Which task did you complete?\n")

    with open("tasks.csv", "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        for row in rows:
            if row["Task Number"] == selection:
                row["Completed"] = "True"

    with open("tasks.csv", "w", newline="") as csvfile:
        fieldnames = ["Task Number", "Task Name", "Description", "Completed"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    secondary_menu()


def main():
    print("Welcome to your to-do list!\n")
    print("What would you like to do first?")

    menu()

    print("Come back when you complete something!")


if __name__ == "__main__":
    main()
