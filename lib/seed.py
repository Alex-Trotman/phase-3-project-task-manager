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
    project_1 = Project.create("Household", "Day-to-day tasks and duties of our household")
    project_2 = Project.create("Finances", "Living below my means, and achieving financial freedom")
    project_3 = Project.create("Career & Professional Development", "Staying up to date in the industry and continuing to grow")
    project_4 = Project.create("Flatiron School", "Full Stack Software Engineering Bootcamp")

    Task.create("Do laundry", "Remember to count how many socks I have", project_1.id, priority=3, completed=False)
    Task.create("Do dishes", "Remember wifey appreciates it when I do them", project_1.id, priority=2, completed=True)
    Task.create("Check account balances against YNAB", "Check how much we spent on groceries last week", project_2.id, priority=4, completed=False)
    Task.create("Pay electric bill", "Has it went up or down?", project_2.id, priority=1, completed=False)
    Task.create("Update contact info on my Resume", "Got a new number", project_3.id, priority=2, completed=True)
    Task.create("Attend networking event with Sam", "Put yourself out there this time", project_3.id, priority=1, completed=False)

    Task.create("Finish coding phase 3 project ASAP", "It's about time", project_4.id, priority=1, completed=True)
    Task.create("Write blog", "Think through it, don't rush", project_4.id, priority=2, completed=True)
    Task.create("Record video", "Remember to keep it short, they don't need to see every line of code", project_4.id, priority=3, completed=True)
    Task.create("Pass Phase 3", "You can do it!", project_4.id, priority=4, completed=False)
    Task.create("Breathe", "Optional", project_4.id, priority=4, completed=False)
    Task.create("Hit the ground running with Phase 4", "Run Forest run!", project_4.id, priority=4, completed=False)



    
    # Task.create("Implement login functionality", "Implement user authentication system", project_1.id, priority=1, completed=False)
    # Task.create("Design homepage layout", "Create wireframes for the homepage design", project_1.id, priority=2, completed=False)
    # Task.create("Prepare social media posts", "Create content for Facebook, Instagram, and Twitter", project_2.id, priority=3, completed=True)
    # Task.create("Conduct market research", "Analyze market trends and customer preferences", project_2.id, priority=4, completed=False)

seed_database()
print("Seeded database")
