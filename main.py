# main.py
import csv
from pathlib import Path

tasks: list[str] = []
p = Path("tasks.csv")


def menu():
    selection = input(
        "1. View all pending tasks\n"
        "2. View all completed tasks\n"
        "3. Add a task\n"
        "4. Remove a task\n"
        "5. Edit an existing task\n"
        "0. Exit program\n"
        "User Selection: "
    )
    if not selection:
        raise ValueError("\nMust select an option\n")

    selection = selection.lower()
    selection = selection.lstrip()
    selection = selection.rstrip()

    print(f"selection == {selection}")

    if selection == "view all pending tasks" or selection == "1":
        view_pending_tasks()
    elif selection == "view all completed tasks" or selection == "2":
        view_completed_tasks()
    elif selection == "add a task" or selection == "3":
        add_task()
    elif selection == "edit an existing task" or selection == "4":
        edit_task()
    elif selection == "delete a task" or selection == "5":
        delete_task()
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


def view_pending_tasks():
    print("view_tasks() called")  # debugging

    # TODO: May need to do a "completed" boolean
    # TODO(cont.): filter later to keep older, completed tasks.

    if p.exists() is False:
        print("No tasks have been created yet!")
    else:
        with open("tasks.csv", newline="") as csvfile:
            contents = csv.reader(csvfile, delimiter=",", quotechar="|")
            for row in contents:
                counter = 0
                # row[2] = "Completed"
                if row[2] == "False":
                    print(", ".join(row))
                    counter += 1
            if counter == 0:
                print("No tasks are currently pending.")

    secondary_menu()


def view_completed_tasks():
    print("view_completed_tasks() called")  # debug

    if p.exists() is False:
        print("No tasks have been created yet!")
    else:
        with open("tasks.csv", newline="") as csvfile:
            contents = csv.reader(csvfile, delimiter=",", quotechar="|")
            for row in contents:
                counter = 0
                # row[2] = "Completed"
                if row[2] == "True":
                    print(", ".join(row))
                    counter += 1
            if counter == 0:
                print("No tasks have been completed yet.")

    secondary_menu()


def add_task():
    print("add_task called")  # debug statement only

    add_name = input("What would you like to call this task? ")
    while not add_name:
        add_name = input("Please enter a name for this task: ")

    # Optional - null input should be accepted
    add_description = input("Add any relevant details about this task. ")

    if p.exists() is True:
        with open("tasks.csv", "a", newline="") as tasks:
            fieldnames = ["Task Name", "Description", "Completed"]
            writer = csv.DictWriter(tasks, fieldnames=fieldnames)
            writer.writerow(
                {
                    "Task Name": add_name,
                    "Description": add_description,
                    "Completed": False,
                }
            )

    if p.exists() is False:
        with open("tasks.csv", "w", newline="") as tasks:
            fieldnames = ["Task Name", "Description", "Completed"]
            writer = csv.DictWriter(tasks, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(
                {
                    "Task Name": add_name,
                    "Description": add_description,
                    "Completed": False,
                }
            )

    secondary_menu()


def delete_task():
    print("remove_task() called")

    secondary_menu()


def edit_task():
    print("edit_task called")

    secondary_menu()


def complete_task():
    pass


def main():
    print("Welcome to your to-do list!")
    print("What would you like to do first?")

    menu()

    print("done")


if __name__ == "__main__":
    main()
