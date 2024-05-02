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


# Project helpers
def list_projects():
    projects = Project.get_all()

    table = Table(title="Projects")
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Description")
    
    for project in projects:
        table.add_row(str(project.id), project.name, project.description)

    console.print(table)


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
        print(f'Success: {project}')
    except Exception as exc:
        print("Error creating project: ", exc)


def update_project():
    id_ = input("Enter the project's id: ")
    if project := Project.find_by_id(id_):
        try:
            name = input("Enter the project's new name: ")
            project.name = name
            description = input("Enter the project's new description: ")
            project.description = description

            project.update()
            print(f'Success: {project}')
        except Exception as exc:
            print("Error updating project: ", exc)
    else:
        print(f'Project {id_} not found')


def delete_project():
    id_ = input("Enter the project's id: ")
    if project := Project.find_by_id(id_):
        project.delete()
        print(f'Project {id_} deleted')
    else:
        print(f'Project {id_} not found')


def list_project_tasks():
    projects = Project.get_all()
    table = Table(title="Projects")
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Description")
    
    for project in projects:
        table.add_row(str(project.id), project.name, project.description)

    console.print(table)

    project_id = input("Enter the project's id: ")
    project = Project.find_by_id(project_id)
    
    if project:
        print(f"Listing tasks for Project {project_id}: {project.name}")
        tasks = project.tasks()
        if tasks:

            table = Table(title=f'{project.name}')
            table.add_column("#")
            table.add_column("Name")
            table.add_column("Description")

            for task in tasks:
                table.add_row(str(task.id), task.name, task.description)
            print("*" * 100)
            console.print(table)
        else:
            print("No tasks found in this project.")
    else:
        print(f"Project with ID {project_id} not found")

# Task helpers
def list_tasks():
    tasks = Task.get_all()

    table = Table(title="Tasks")
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Project")
    
    for task in tasks:
        table.add_row(str(task.id), task.name, task.description, str(task.project_id))

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


def create_task():
    name = input("Enter the task's name: ")
    description = input("Enter the task's description: ")
    project_id = input("Enter the task's project id: ")
    try:
        task = Task.create(name, description, project_id)
        print(f'Success: {task}')
    except Exception as exc:
        print("Error creating task: ", exc)


def update_task():
    id_ = input("Enter the task's id: ")
    if task := Task.find_by_id(id_):
        try:
            name = input("Enter the task's new name: ")
            task.name = name
            description = input("Enter the task's new description: ")
            task.description = description

            task.update()
            print(f'Success: {task}')
        except Exception as exc:
            print("Error updating task: ", exc)
    else:
        print(f'Task {id_} not found')


def delete_task():
    id_ = input("Enter the task's id: ")
    if task := Task.find_by_id(id_):
        task.delete()
        print(f'Task {id_} deleted')
    else:
        print(f'Task {id_} not found')

