

from datetime import datetime

class Task:
    def __init__(self, title, deadline=None, priority="Medium", status="Pending"):
        self.title = title
        self.deadline = deadline  # format: "YYYY-MM-DD"
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "deadline": self.deadline,
            "priority": self.priority,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data["title"],
            deadline=data.get("deadline"),
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Pending")
        )
