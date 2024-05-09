import os
from models.project import Project
from models.task import Task
from rich.console import Console
from rich.table import Table

console = Console()

def exit_program():
    print("Goodbye!")
    exit()

def clear():
    os.system("clear")


def list_projects():
    projects = Project.get_all()

    table = Table(title="Projects")
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Description")
    
    for index, project in enumerate(projects, start=1):
        table.add_row(str(index), project.name, project.description)
    clear()
    console.print(table)

def open_project():
    from cli import main
    projects = Project.get_all()
    index_to_id = {}
    
    table = Table(title="Projects")
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Description")
    
    for index, project in enumerate(projects, start=1):
        table.add_row(str(index), project.name, project.description)
    
    clear()
    console.print(table)
    
    selected_index_input = input("Select project to enter (hit Enter to skip): ").strip()

    if not selected_index_input:
        clear()
        main()
        
    project = projects[int(selected_index_input) - 1]
    print(project)
    
    try:
        return project
    except ValueError:
        print("Invalid input. Please enter a valid number or hit Enter to skip.")
        return open_project()

def find_project_by_id():
    id_ = input("Enter the project's id: ")
    project = Project.find_by_id(id_)
    if project:
        table = Table(title="Projects")
        table.add_column("#")
        table.add_column("Name")
        table.add_column("Description")

        table.add_row(str(project.id), project.name, project.description)
        print("*" * 100)
        console.print(table)
    else:
         print(f'Project {id_} not found')

def create_project():
    while True:
        name = input("Enter the project's name: ")
        description = input("Enter the project's description: ")
        break

    try:
        project = Project.create(name, description)
        clear()
        list_projects()
        print(f'Success: Project {project.name} created')
    except Exception as exc:
        print("Error creating project: ", exc)




def edit_project():
    name_to_id = {}
    projects = Project.get_all()
    for index, project in enumerate(projects, start=1):
        name_to_id[str(index)] = project.id

    selected_index = input("Enter the number of the project to edit: ")
    selected_project_id = name_to_id.get(selected_index)
    if selected_project_id:
        project = Project.find_by_id(selected_project_id)
        try:
            new_name = input(f"Enter the project's new name (current name: {project.name}): ") or project.name
            new_description = input(f"Enter the project's new description (current description: {project.description}): ") or project.description
            project.name = new_name
            project.description = new_description
            project.update()
            clear()
            list_projects()
            print(f'Success: Project {project.name} updated')
        except Exception as exc:
            print("Error updating project: ", exc)
    else:
        print("Invalid project selection.")


def delete_project():
    name_to_id = {}
    projects = Project.get_all()

    for index, project in enumerate(projects, start=1):
        name_to_id[str(index)] = project.id

    selected_index = input("Enter the number of the project to delete: ")
    selected_project_id = name_to_id.get(selected_index)
    if selected_project_id:
        project = Project.find_by_id(selected_project_id)
        try:
            confirmation = input(f"Are you sure you want to delete project '{project.name}'? (yes/no): ").strip().lower()
            if confirmation == "yes":
                project.delete()
                clear()
                list_projects()
                print(f'Project {project.name} deleted')
            else:
                print("Deletion cancelled.")
        except Exception as exc:
            print("Error deleting project: ", exc)
    else:
        print("Invalid project selection.")


def list_project_tasks(project):
    if project:
        tasks = project.tasks()
        table = Table(title=f'{project.name} Tasks')
        table.add_column("#")
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Priority")
        table.add_column("Completed")
        
        for index, task in enumerate(tasks, start=1):
            completed_status = "✔" if task.completed else "✘"
            table.add_row(str(index), task.name, task.description, str(task.priority), completed_status)
        print("*" * 100)
        console.print(table)
    else:
        print(f"Project with ID {project_id} not found")

def create_task(project):
    name = input("Enter the task's name: ")
    description = input("Enter the task's description: ")
    while True:
        priority = input("Enter the task's priority (1-4): ")
        try:
            priority = int(priority)
            if 1 <= priority <= 4:
                break
            else:
                print("Priority must be an integer between 1 and 4.")
        except ValueError:
            print("Priority must be a valid integer.")

    completed = False

    try:
        task = Task.create(name, description, project.id, priority, completed)
        clear()
        list_project_tasks(project)
        print(f'Success task {task.name} created')
    except ValueError:
        print("Error: Priority must be a valid integer between 1 and 4")
    except Exception as exc:
        print("Error creating task: ", exc)

def edit_task(project):

    tasks = project.tasks()
    if not tasks:
        print("No tasks found for this project.")
        return

    index_to_id = {}
    for index, task in enumerate(tasks, start=1):
        index_to_id[index] = task.id

    try:
        selected_index = int(input("Enter task number to select: "))
        selected_task_id = index_to_id[selected_index]
    except (ValueError, KeyError):
        clear()
        print("Invalid task selection.")
        return

    if task := Task.find_by_id(selected_task_id):
        try:
            print("Enter the task's new name (press Enter to keep it unchanged):")
            name = input(f"Current name: {task.name}: ") or task.name

            print("Enter the task's new description (press Enter to keep it unchanged):")
            description = input(f"Current description: {task.description}: ") or task.description

            print("Enter the task's new priority (1-4) (press Enter to keep it unchanged):")
            priority = input(f"Current priority: {task.priority}: ")
            priority = int(priority) if priority else task.priority

            print("Do you want to mark the task as (C)ompleted or (U)ncompleted? (press Enter to keep it unchanged):")
            completed_action = input(f"Current completion status: {'Completed' if task.completed else 'Uncompleted'}: ").strip().lower()
            if completed_action == 'c':
                completed = True
            elif completed_action == 'u':
                completed = False
            else:
                completed = task.completed

            task.name = name
            task.description = description
            task.priority = priority
            task.completed = completed
            
            task.update()
            clear()
            list_project_tasks(project)
            print("Success: Task updated")
        except Exception as exc:
            print("Error updating task: ", exc)
    else:
        print(f"Task with ID {selected_task_id} not found")


def complete_task(project):
    tasks = project.tasks()
    if not tasks:
        print("No tasks found for this project.")
        return

    index_to_id = {}
    for index, task in enumerate(tasks, start=1):
        index_to_id[index] = task.id

    try:
        selected_index = int(input("Enter the task number to complete or uncomplete: "))
        selected_task_id = index_to_id[selected_index]
        print(f"Selected task index: {selected_index}, Task ID: {selected_task_id}")
        selected_task = Task.find_by_id(selected_task_id)
        if not selected_task:
            print(f"Task with ID {selected_task_id} not found")
            return

        print(f"Current status of task '{selected_task.name}': {'Completed' if selected_task.completed else 'Not Completed'}")

        action = input("Do you want to (C)omplete or (U)ncomplete the task? ").strip().lower()
        print(f"Selected action: {action}")
        if action == 'c':
            selected_task.completed = True

            selected_task.update()
            print(f"Task '{selected_task.name}' marked as completed")
        elif action == 'u':
            selected_task.completed = False
            selected_task.update()
            print(f"Task '{selected_task.name}' marked as not completed")
        else:
            print("Invalid action. Please choose 'C' or 'U'.")

        clear()
        list_project_tasks(project)
    except (ValueError, KeyError):
        print("Invalid task selection.")

def delete_task(project):
    tasks = project.tasks()
    if not tasks:
        print("No tasks found for this project.")
        return

    index_to_id = {}
    for index, task in enumerate(tasks, start=1):
        index_to_id[index] = task.id

    try:
        selected_index = int(input("Enter task number to delete: "))
        selected_task_id = index_to_id[selected_index]
        confirmation = input("Are you sure you want to delete this task? (yes/no): ").strip().lower()
        if confirmation == "yes":
            if task := Task.find_by_id(selected_task_id):
                task.delete()
                clear()
                list_project_tasks(project)
                print(f'Selected task: {task.name} deleted')
            else:
                print(f'Selected task: {selected_index} not found')
        else:
            clear()
            list_project_tasks(project)
            print("Deletion cancelled.")
    except (ValueError, KeyError):
        clear()
        print("Invalid task selection.")