
from typing import List


class Task:
    def __init__(self, name: str, due_date,is_done=False) -> None:
        self.name = name
        self.due_date = due_date
        self.is_done = is_done


class TaskManager:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    