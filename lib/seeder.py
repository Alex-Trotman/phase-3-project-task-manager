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
    project_1 = Project.create("Software Development", "Developing new application features")
    project_2 = Project.create("Marketing Campaign", "Launching new advertising campaign")
    Task.create("Implement login functionality", "Implement user authentication system", project_1.id)
    Task.create("Design homepage layout", "Create wireframes for the homepage design", project_1.id)
    Task.create("Prepare social media posts", "Create content for Facebook, Instagram, and Twitter", project_2.id)
    Task.create("Conduct market research", "Analyze market trends and customer preferences", project_2.id)

seed_database()
print("Seeded database")
