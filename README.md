# Python CLI To-Do List

A text-based task manager built with Python. This project represents my first implementation of a persistent application using CSV file handling and procedural programming logic.

## About
This application allows users to manage daily tasks through a Command Line Interface (CLI). Unlike in-memory scripts, this program persists data to a local CSV file, ensuring tasks are saved even after the program closes.

This project was built to master the fundamentals ofr Python control flow, file input/output, and state management.

## Features
- **Persistent Storage:**
  - Automatically creates and updates a tasks.csv file
- **Task Management:**
  - View pending tasks in a dynamically formatted table
  - View completed task history
  - Add new tasks with optional descriptions
  - Mark tasks as complete
- **Error Handling**
  - Handles missing/deleted CSV files gracefully
  - Prevents completing tasks that are already completed
  - Validates user input to prevent crashes

## Technical Highlights
- **File I/O**
  - Implementation of the `csv` library
- **Path Safety**
  - Utilized `pathlib` to check file existence and prevent runtime errors
- **Architecture**
  - Refactored to a stable while loop "Controller" pattern from unstable recursive function calls
- **Data Validation**
  - Logic ensures Task IDs are valid and states are tracked appropriately

## How to Run
1. Ensure you have Python 3.x installed.
2. Clone this repository.
3. Run the script with `python main.py`.
4. Follow the on-screen menu prompts.

### Future Roadmap
This repo is archived as a first to-do list project. This will later be rebuilt with more advanced features such as:
  - **Refactoring to OOP:** Rebuilding the logic to use classes such as `Task` and `TaskManager` classes.
  - **Database Integration:** Moving from CSV to SQLite
  - **New Features:** Deleting tasks, editing tasks, and due dates.
