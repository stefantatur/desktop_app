from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    LOW = "Низкий"
    MEDIUM = "Средний"
    HIGH = "Высокий"

    @classmethod
    def values(cls) -> list[str]:
        return [priority.value for priority in cls]

    @classmethod
    def from_text(cls, text: str) -> Priority:
        for priority in cls:
            if priority.value == text:
                return priority

        return cls.MEDIUM


@dataclass
class Task:
    title: str
    category: str = "Общее"
    priority: Priority = Priority.MEDIUM
    done: bool = False

    def mark_done(self) -> None:
        self.done = True

    def mark_active(self) -> None:
        self.done = False

    def switch_status(self) -> None:
        if self.done:
            self.mark_active()
        else:
            self.mark_done()

    def matches(self, search_text: str, status_filter: str) -> bool:
        text = search_text.strip().lower()
        text_match = text in self.title.lower() or text in self.category.lower()
        active_match = status_filter == "Активные" and not self.done
        done_match = status_filter == "Готовые" and self.done
        status_match = status_filter == "Все" or active_match or done_match

        return text_match and status_match

    def get_text(self) -> str:
        status = "✓" if self.done else " "
        return f"[{status}] {self.title} | {self.category} | {self.priority.value}"


@dataclass
class TaskStatistics:
    total: int
    active: int
    done: int
    high_priority: int

    def get_text(self) -> str:
        return (
            f"Всего: {self.total} | Активные: {self.active} | "
            f"Готовые: {self.done} | Важные: {self.high_priority}"
        )
