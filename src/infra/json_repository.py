from __future__ import annotations

import json
from pathlib import Path

from src.logic.entities import Task
from src.logic.repository import TaskRepository
from src.logic.schemas import TaskFileSchema


class JsonTaskRepository(TaskRepository):
    def __init__(self, file_path: str = "tasks.json") -> None:
        self.file_path = Path(file_path)

    def load(self) -> list[Task]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [TaskFileSchema.model_validate(item).to_entity() for item in data]

    def save(self, tasks: list[Task]) -> None:
        data = [
            TaskFileSchema.from_entity(task).model_dump(mode="json")
            for task in tasks
        ]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
