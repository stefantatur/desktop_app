from __future__ import annotations

from pydantic import ValidationError

from src.logic.entities import Priority, Task, TaskStatistics
from src.logic.repository import TaskRepository
from src.logic.schemas import TaskCreateSchema


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository
        self.tasks = repository.load()

    def add_task(self, title: str, category: str, priority_text: str) -> None:
        try:
            task_data = TaskCreateSchema(
                title=title,
                category=category,
                priority=priority_text,
            )
        except ValidationError as error:
            raise ValueError("Проверьте название, категорию и приоритет") from error

        self.tasks.append(task_data.to_entity())
        self._save()

    def remove_task(self, task: Task) -> None:
        self.tasks.remove(task)
        self._save()

    def switch_status(self, task: Task) -> None:
        task.switch_status()
        self._save()

    def clear_done(self) -> int:
        old_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task.done]
        removed_count = old_count - len(self.tasks)
        self._save()
        return removed_count

    def get_filtered_tasks(self, search_text: str, status_filter: str) -> list[Task]:
        tasks = [
            task for task in self.tasks if task.matches(search_text, status_filter)
        ]

        return sorted(tasks, key=self._sort_key)

    def get_statistics(self) -> TaskStatistics:
        done = sum(task.done for task in self.tasks)
        high_priority = sum(
            task.priority == Priority.HIGH and not task.done for task in self.tasks
        )

        return TaskStatistics(
            total=len(self.tasks),
            active=len(self.tasks) - done,
            done=done,
            high_priority=high_priority,
        )

    def _sort_key(self, task: Task) -> tuple[bool, int, str]:
        priority_order = {
            Priority.HIGH: 0,
            Priority.MEDIUM: 1,
            Priority.LOW: 2,
        }
        return task.done, priority_order[task.priority], task.title.lower()

    def _save(self) -> None:
        self.repository.save(self.tasks)
