# Phase 3 Project: Task Manager

![image](https://github.com/user-attachments/assets/4f215e61-03ff-406d-9231-3c1d59df0556)


A command-line application designed to manage tasks and projects efficiently by leveraging the power of Python. It utilizes the `rich` library to deliver visually appealing and user-friendly interfaces, providing comprehensive tables, menus, and feedback directly in the terminal. Built with object-relational mapping (ORM) methods for seamless database interactions, this tool simplifies task and project management. Users can prioritize tasks, mark tasks as complete, and handle projects with ease through an intuitive CLI interface.

## Features

- Create, edit, and delete projects
- Create, edit, and delete tasks within projects
- List and view tasks or projects in rich-format tables
- Prioritize tasks and mark them as completed

## Getting Started

### Prerequisites

- Python 3.8 or newer
- `pipenv` for managing dependencies

### Installation

1. **Fork & Clone the Repository:**
   - Click "Fork" on GitHub to fork the repository to your account.
   - Clone it to your local machine:
   ```bash
   git clone https://github.com/Alex-Trotman/phase-3-project-task-manager.git
   ```
2. **Install Dependencies:**
   - Install all the required packages using 'pipenv'.
   ```bash
   pipenv install
   ```
3. **Activate the Virtual Environment:**
   - Enter the virtual environment to start working on the project.
   ```bash
   pipenv shell
   ```
4. **Seed the Database:**
   - Seed the database with initial data by running the seed file or script:
   ```bash
   python lib/seed.py
   ```
5. **Run the Application:**
   ```bash
   python lib/cli.py
   ```

## Usage

### Basic Commands

- List Projects: Type 1 to list all projects.
- Open a Project: Type 2 to open and manage tasks within a project.
- Manage Projects: Type 3 to create, edit, or delete projects.
- Exit: Type exit or 0 to close the application.

### Managing Projects

- Create a Project: Select the "Create Project" option to add a new project.
- Edit or Delete: Choose "Edit Project" or "Delete Project" to modify or remove an existing project.

### Managing Tasks

- Create a Task: In the project's task menu, select "Create Task" to add a new task.
- Edit or Delete: Choose "Edit Task" or "Delete Task" to modify or remove an existing task.
- Complete a Task: Mark a task as completed or uncompleted.
