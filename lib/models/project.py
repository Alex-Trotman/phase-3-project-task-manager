# lib/models/project.py
from models.__init__ import CURSOR, CONN


class Project:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, description, id=None):
        self.id = id
        self.name = name
        self.description = description

    # def __repr__(self):
    #     return f"<Project {self.id}: {self.name}, {self.description}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if isinstance(description, str) and len(description):
            self._description = description
        else:
            raise ValueError(
                "Description must be a non-empty string"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Project instances """
        sql = """
            CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Project instances """
        sql = """
            DROP TABLE IF EXISTS projects;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and description values of the current Project instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO projects (name, description)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.description))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, description):
        """ Initialize a new Project instance and save the object to the database """
        project = cls(name, description)
        project.save()
        return project

    def update(self):
        """Update the table row corresponding to the current Project instance."""
        sql = """
            UPDATE projects
            SET name = ?, description = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.description, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Project instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM projects
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Project object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        project = cls.all.get(row[0])
        if project:
            # ensure attributes match row values in case local instance was modified
            project.name = row[1]
            project.description = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            project = cls(row[1], row[2])
            project.id = row[0]
            cls.all[project.id] = project
        return project

    @classmethod
    def get_all(cls):
        """Return a list containing a Project object per row in the table"""
        sql = """
            SELECT *
            FROM projects
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a Project object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM projects
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return a Project object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM projects
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def tasks(self):
        """Return list of tasks associated with current project"""
        from models.task import Task
        sql = """
            SELECT * FROM tasks
            WHERE project_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Task.instance_from_db(row) for row in rows
        ]
