# lib/helpers.py
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
    # Get all projects
    projects = Project.get_all()
    # Create a dictionary to map enumerated indices to project IDs
    index_to_id = {}
    
    # Create reference table for projects
    table = Table(title="Projects")
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Description")
    
    # Populate the table and dictionary
    for index, project in enumerate(projects, start=1):
        table.add_row(str(index), project.name, project.description)
        index_to_id[index] = project.id
    
    clear()
    console.print(table)
    
    # User selects which project to enter
    selected_index = int(input("Select project to enter: "))
    # Retrieve the actual project ID from the dictionary
    selected_project_id = index_to_id.get(selected_index)
    
    # Return the id of the selected project
    return selected_project_id

def find_project_by_name():
    name = input("Enter the project's name: ")
    projects = Project.get_all()
    matching_projects = [project for project in projects if name.lower() in project.name.lower()]
    if matching_projects:
        if len(matching_projects) == 1:
            table = Table(title="Projects")
            table.add_column("#")
            table.add_column("Name")
            table.add_column("Description")

            table.add_row(str(matching_projects[0].id), matching_projects[0].name, matching_projects[0].description)

            console.print(table)

            # print(f"Project found: {matching_projects[0].name}: {matching_projects[0].description}")
        else:
            print("Did you mean one of these projects?")

            table = Table(title="Projects")
            table.add_column("#")
            table.add_column("Name")
            table.add_column("Description")
            for project in matching_projects:
                table.add_row(str(project.id), project.name, project.description)
            console.print(table)
    else:
        print(f'No projects found matching "{name}"')


# def find_project_by_name():
#     name = input("Enter the project's name: ")
#     project = Project.find_by_name(name)
#     print(project) if project else print(
#         f'Project {name} not found')


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
    name = input("Enter the project's name: ")
    description = input("Enter the project's description: ")
    try:
        project = Project.create(name, description)
        clear()
        list_projects()
        print(f'Success: {project}')
    except Exception as exc:
        print("Error creating project: ", exc)


def edit_project():
    name = input("Enter the project's name: ")
    projects = Project.get_all()
    matching_projects = [project for project in projects if name.lower() in project.name.lower()]
    if matching_projects:
        if len(matching_projects) == 1:
            project = matching_projects[0]
            try:
                new_name = input(f"Enter the project's new name (current name: {project.name}): ") or project.name
                new_description = input(f"Enter the project's new description (current description: {project.description}): ") or project.description
                project.name = new_name
                project.description = new_description
                project.update()
                clear()
                list_projects()
                print(f'Success: {project}')
            except Exception as exc:
                print("Error updating project: ", exc)
        else:
            print("Multiple projects found matching that name. Please refine your search.")
    else:
        print(f'No projects found matching "{name}"')


def delete_project():
    name = input("Enter the project's name: ")
    projects = Project.get_all()
    matching_projects = [project for project in projects if name.lower() in project.name.lower()]
    if matching_projects:
        if len(matching_projects) == 1:
            project = matching_projects[0]
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
            print("Multiple projects found matching that name. Please refine your search.")
    else:
        print(f'No projects found matching "{name}"')



def list_project_tasks(project_id):
    project = Project.find_by_id(project_id)
    
    if project:
        tasks = project.tasks()
        table = Table(title=f'{project.name} Tasks')
        table.add_column("#")
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Priority")
        table.add_column("Completed")
        
        # Using enumerate to assign an index starting from 1 to each task
        for index, task in enumerate(tasks, start=1):
            completed_status = "✔" if task.completed else "✘"
            table.add_row(str(index), task.name, task.description, str(task.priority), completed_status)
        print("*" * 100)
        console.print(table)
    else:
        print(f"Project with ID {project_id} not found")


def list_tasks():
    tasks = Task.get_all()

    table = Table(title="Tasks")
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Priority")
    table.add_column("Project")
    table.add_column("Completed")
    
    for task in tasks:
        completed_status = "✔" if task.completed else "✘"
        table.add_row(str(task.id), task.name, task.description, str(task.priority), str(task.project_id), completed_status)

    console.print(table)


def find_task_by_name():
    name = input("Enter the task's name: ")
    task = Task.find_by_name(name)
    print(task) if task else print(
        f'Task {name} not found')


def find_task_by_id():
    id_ = input("Enter the task's id: ")
    task = Task.find_by_id(id_)
    print(task) if task else print(f'Task {id_} not found')


def create_task(project_id):
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

    completed = False  # Default to False when creating a task

    try:
        task = Task.create(name, description, project_id, priority, completed)
        clear()
        list_project_tasks(project_id)
        print(f'Success: {task}')
    except ValueError:
        print("Error: Priority must be a valid integer between 1 and 4")
    except Exception as exc:
        print("Error creating task: ", exc)







def edit_task(project_id):
    project = Project.find_by_id(project_id)
    if not project:
        print(f"Project with ID {project_id} not found")
        return

    tasks = project.tasks()
    if not tasks:
        print("No tasks found for this project.")
        return

    # Create a mapping from index to task ID
    index_to_id = {}
    for index, task in enumerate(tasks, start=1):
        index_to_id[index] = task.id

    try:
        selected_index = int(input("Enter task number to select: "))
        selected_task_id = index_to_id[selected_index]  # Retrieve the actual task ID using the index
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

            # Updating task properties
            task.name = name
            task.description = description
            task.priority = priority
            task.completed = completed
            
            # Assuming task.update() commits the changes
            task.update()
            clear()
            list_project_tasks(project_id)
            print("Success: Task updated")
        except Exception as exc:
            print("Error updating task: ", exc)
    else:
        print(f"Task with ID {selected_task_id} not found")


def complete_task(project_id):
    project = Project.find_by_id(project_id)
    if not project:
        print(f"Project with ID {project_id} not found")
        return

    tasks = project.tasks()
    if not tasks:
        print("No tasks found for this project.")
        return

    # Create a mapping from index to task ID
    index_to_id = {}
    for index, task in enumerate(tasks, start=1):
        index_to_id[index] = task.id

    try:
        selected_index = int(input("Enter the task number to complete or uncomplete: "))
        selected_task_id = index_to_id[selected_index]  # Retrieve the actual task ID using the index
        print(f"Selected task index: {selected_index}, Task ID: {selected_task_id}")
        selected_task = Task.find_by_id(selected_task_id)
        if not selected_task:
            print(f"Task with ID {selected_task_id} not found")
            return

        # Display current status of the task
        print(f"Current status of task '{selected_task.name}': {'Completed' if selected_task.completed else 'Not Completed'}")

        # Ask the user if they want to toggle the completion status
        action = input("Do you want to (C)omplete or (U)ncomplete the task? ").strip().lower()
        print(f"Selected action: {action}")
        if action == 'c':
            selected_task.completed = True

            selected_task.update()
            print(f"Task '{selected_task.name}' marked as completed")
        elif action == 'u':
            # Toggle the completion status to False
            selected_task.completed = False
            # Update the task
            selected_task.update()
            print(f"Task '{selected_task.name}' marked as not completed")
        else:
            print("Invalid action. Please choose 'C' or 'U'.")

        # Clear the screen and list tasks after completing an action
        clear()
        list_project_tasks(project_id)
    except (ValueError, KeyError):
        print("Invalid task selection.")





def delete_task(project_id):
    project = Project.find_by_id(project_id)
    if not project:
        print(f"Project with ID {project_id} not found")
        return

    tasks = project.tasks()
    if not tasks:
        print("No tasks found for this project.")
        return

    # Create a mapping from index to task ID
    index_to_id = {}
    for index, task in enumerate(tasks, start=1):
        index_to_id[index] = task.id

    try:
        selected_index = int(input("Enter task number to delete: "))
        selected_task_id = index_to_id[selected_index]  # Retrieve the actual task ID using the index
        confirmation = input("Are you sure you want to delete this task? (yes/no): ").strip().lower()
        if confirmation == "yes":
            if task := Task.find_by_id(selected_task_id):
                task.delete()
                clear()
                list_project_tasks(project_id)
                print(f'Selected task: {task.name} deleted')
            else:
                print(f'Selected task: {selected_index} not found')
        else:
            clear()
            list_project_tasks(project_id)
            print("Deletion cancelled.")
    except (ValueError, KeyError):
        clear()
        print("Invalid task selection.")



