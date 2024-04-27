# lib/helpers.py

from models.project import Project
from models.task import Task

def exit_program():
    print("Goodbye!")
    exit()

# Project helpers
def list_projects():
    projects = Project.get_all()
    for project in projects:
        print(project)


def find_project_by_name():
    name = input("Enter the project's name: ")
    project = Project.find_by_name(name)
    print(project) if project else print(
        f'Project {name} not found')


def find_project_by_id():
    id_ = input("Enter the project's id: ")
    project = Project.find_by_id(id_)
    print(project) if project else print(f'Project {id_} not found')


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
    project_id = input("Enter the project's id: ")
    project = Project.find_by_id(project_id)
    
    if project:
        print(f"Listing tasks for Project {project_id}: {project.name}")
        tasks = project.tasks()
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("No tasks found in this project.")
    else:
        print(f"Project with ID {project_id} not found")

# Task helpers
def list_tasks():
    tasks = Task.get_all()
    for task in tasks:
        print(task)


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

