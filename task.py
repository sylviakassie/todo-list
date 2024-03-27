
from typing import List


class Task:
    def __init__(self, name: str, due_date, is_done=False) -> None:
        self.name = name
        self.due_date = due_date
        self.is_done = is_done


class TaskManager:
    def __init__(self) -> None:
        self.__tasks: List[Task] = []

    def add_task(self, task: Task):
        self.__tasks.append(task)

    def delete_task(self, task: Task):
        self.__tasks.remove(task)

    def update_task(self, index, new_task: Task):
        self.__tasks[index] = new_task

    def _get_task(self, index) -> Task:
        return self.__tasks[index]

    def toggle_task(self, index):
        task = self._get_task(index)
        if task.is_done:
            task.is_done = False
        else:
            task.is_done = True

    def get_tasks(self):
        return self.__tasks
