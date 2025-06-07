import json
import os
from taskforge.task import Task  # Import the Task class from your local module

# File path where tasks will be stored as JSON
TASK_FILE = "data/tasks.json"

class TaskManager:
    def __init__(self):
        # Initialize the task manager by loading tasks from file
        self.tasks = self.load_tasks()

    def add_task(self, task):
        """Add a new task and save the updated list."""
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        """Return the current list of tasks."""
        return self.tasks

    def delete_task(self, index):
        """Delete a task by index, if it exists."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def save_tasks(self):
        """Write the task list to the JSON file."""
        with open(TASK_FILE, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.status = 'Completed' if task.status != 'Completed' else 'Pending'
            self.save_tasks()


    def load_tasks(self):
        """
        Load tasks from the JSON file.
        Return an empty list if the file is missing, empty, or invalid.
        """
        if os.path.exists(TASK_FILE):
            try:
                with open(TASK_FILE, "r") as f:
                    content = f.read().strip()
                    if not content:
                        return []  # File is empty
                    data = json.loads(content)
                    return [Task.from_dict(d) for d in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading tasks: {e}")
                return []  # Return empty list if JSON is invalid or file can't be read
        return []  # Return empty list if file does not exist
