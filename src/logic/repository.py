from __future__ import annotations

from abc import ABC, abstractmethod

from src.logic.entities import Task


class TaskRepository(ABC):
    @abstractmethod
    def load(self) -> list[Task]:
        pass

    @abstractmethod
    def save(self, tasks: list[Task]) -> None:
        pass
