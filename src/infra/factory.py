from __future__ import annotations

from src.infra.gui import TaskApp
from src.infra.json_repository import JsonTaskRepository
from src.logic.task_service import TaskService


class ApplicationFactory:
    @staticmethod
    def create() -> TaskApp:
        repository = JsonTaskRepository()
        service = TaskService(repository)

        return TaskApp(service)
