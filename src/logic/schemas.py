from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from src.logic.entities import Priority, Task


class TaskCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    category: str = Field(default="Общее", max_length=40)
    priority: Priority = Priority.MEDIUM

    @field_validator("title", "category", mode="before")
    @classmethod
    def strip_text(cls, value: object) -> str:
        return str(value).strip()

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value:
            raise ValueError("Название задачи не может быть пустым")

        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        return value or "Общее"

    @field_validator("priority", mode="before")
    @classmethod
    def validate_priority(cls, value: object) -> Priority:
        if isinstance(value, Priority):
            return value

        return Priority.from_text(str(value))

    def to_entity(self) -> Task:
        return Task(
            title=self.title,
            category=self.category,
            priority=self.priority,
        )


class TaskFileSchema(TaskCreateSchema):
    done: bool = False

    @classmethod
    def from_entity(cls, task: Task) -> TaskFileSchema:
        return cls(
            title=task.title,
            category=task.category,
            priority=task.priority,
            done=task.done,
        )

    def to_entity(self) -> Task:
        return Task(
            title=self.title,
            category=self.category,
            priority=self.priority,
            done=self.done,
        )
