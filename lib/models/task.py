from models.__init__ import CURSOR, CONN


class Task:
    all = {}

    def __init__(self, name, description, project_id, id=None, priority=None, completed=None):
        self.id = id
        self.name = name
        self.description = description
        self.project_id = project_id
        self.priority = priority
        self.completed = completed

    # def __repr__(self):
    #     return f"<Task {self.id}: {self.name}, {self.description}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if isinstance(description, str) and len(description):
            self._description = description
        else:
            raise ValueError("Description must be a non-empty string")

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        if isinstance(project_id, int) and project_id > 0:
            self._project_id = project_id
        else:
            raise ValueError("Project ID must be a positive integer")

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        try:
            priority = int(priority)
        except ValueError:
            raise ValueError("Priority must be a valid integer")

        if 1 <= priority <= 4:
            self._priority = priority
        else:
            raise ValueError("Priority must be an integer between 1 and 4")
        
    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed):
        if isinstance(completed, bool):
            self._completed = completed
        else:
            raise ValueError("Completed must be a boolean value")



    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            project_id INTEGER,
            priority INTEGER,
            completed BOOL,
            FOREIGN KEY(project_id) REFERENCES projects(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS tasks;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO tasks (name, description, project_id, priority, completed)
            VALUES (?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.description, self.project_id, self.priority, self.completed))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    @classmethod
    def create(cls, name, description, project_id, priority, completed):
        task = cls(name, description, project_id, priority=priority, completed=completed) 
        task.save()
        return task

    def update(self):
        sql = """
            UPDATE tasks
            SET name = ?, description = ?, project_id = ?, priority = ?, completed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.description, self.project_id, self.priority, self.completed, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM tasks
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        task = cls.all.get(row[0])
        if task:
            task.name = row[1]
            task.description = row[2]
            task.project_id = row[3]
            task.priority = row[4]
            task.completed = bool(row[5])  # Convert to boolean
        else:
            task = cls(row[1], row[2], row[3], priority=row[4], completed=bool(row[5]))  # Convert to boolean
            task.id = row[0]
            cls.all[task.id] = task
        return task


    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM tasks
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM tasks
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM tasks
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

