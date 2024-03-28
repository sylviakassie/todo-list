
from datetime import datetime
from typing import List


class Task:
    def __init__(self, name: str, due_date: datetime, is_done=False) -> None:
        self.name = name
        self.due_date: datetime = due_date
        self.is_done = is_done

    def __str__(self) -> str:
        done = 'Done' if self.is_done else 'Not Done'
        return f'{self.name} - {self.due_date} - {done}'

    def __repr__(self) -> str:
        done = 'Done' if self.is_done else 'Not Done'
        return f'{self.name} - {self.due_date} - {done}'


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
