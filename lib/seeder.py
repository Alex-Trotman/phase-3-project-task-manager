#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.project import Project
from models.task import Task

def seed_database():
    Project.drop_table()
    Task.drop_table()
    Project.create_table()
    Task.create_table()

    # Create seed data
    project_1 = Project.create("Project 1", "Building A, 5th Floor")
    project_2 = Project.create(
        "Project 2", "Building C, East Wing")
    Task.create("Example Name 1", "Accountant", project_1.id)
    Task.create("Example Name 2", "Manager", project_1.id)
    Task.create("Example Name 3", "Manager", project_1.id)
    Task.create("Example Name 4", "Benefits Coordinator", project_2.id)
    Task.create("Example Name 5", "New Hires Coordinator", project_2.id)


seed_database()
print("Seeded database")
