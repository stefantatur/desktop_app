from __future__ import annotations

import flet as ft

from src.logic.entities import Priority, Task
from src.logic.task_service import TaskService


class TaskApp:
    def __init__(self, service: TaskService) -> None:
        self.service = service
        self.page: ft.Page | None = None
        self.visible_tasks: list[Task] = []
        self.selected_task: Task | None = None

        self.title_field = ft.TextField()
        self.category_field = ft.TextField()
        self.priority_dropdown = ft.Dropdown()
        self.search_field = ft.TextField()
        self.status_dropdown = ft.Dropdown()
        self.task_list = ft.ListView()
        self.stats_text = ft.Text()

    def run(self) -> None:
        ft.app(target=self._main)

    def _main(self, page: ft.Page) -> None:
        self.page = page
        page.title = "Task Manager"
        page.padding = 20

        self._setup_window(page)
        page.add(self._build_layout())
        self.refresh_tasks()

    def _setup_window(self, page: ft.Page) -> None:
        try:
            page.window.width = 860
            page.window.height = 640
            page.window.resizable = False
        except AttributeError:
            page.window_width = 860
            page.window_height = 640
            page.window_resizable = False

    def _build_layout(self) -> ft.Control:
        self.title_field = ft.TextField(
            label="Название задачи",
            width=260,
            on_submit=lambda _event: self.add_task(),
        )
        self.category_field = ft.TextField(
            label="Категория",
            width=180,
        )
        self.priority_dropdown = ft.Dropdown(
            label="Приоритет",
            value=Priority.MEDIUM.value,
            options=[ft.dropdown.Option(value) for value in Priority.values()],
            width=160,
        )
        self.search_field = ft.TextField(
            label="Поиск",
            width=320,
            on_change=lambda _event: self.refresh_tasks(),
        )
        self.status_dropdown = ft.Dropdown(
            label="Фильтр",
            value="Все",
            options=[
                ft.dropdown.Option("Все"),
                ft.dropdown.Option("Активные"),
                ft.dropdown.Option("Готовые"),
            ],
            width=150,
            on_change=lambda _event: self.refresh_tasks(),
        )
        self.task_list = ft.ListView(height=260, spacing=4)
        self.stats_text = ft.Text()

        return ft.Column(
            controls=[
                ft.Text("Task Manager", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Простое desktop-приложение на Flet"),
                ft.Row(
                    controls=[
                        self.title_field,
                        self.category_field,
                        self.priority_dropdown,
                        ft.ElevatedButton("Добавить", on_click=lambda _event: self.add_task()),
                    ],
                    wrap=True,
                ),
                ft.Row(
                    controls=[
                        self.search_field,
                        self.status_dropdown,
                        ft.ElevatedButton("Сбросить", on_click=lambda _event: self.reset_filters()),
                    ],
                    wrap=True,
                ),
                self.task_list,
                self.stats_text,
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Готово / активно",
                            on_click=lambda _event: self.switch_status(),
                        ),
                        ft.ElevatedButton("Удалить", on_click=lambda _event: self.remove_task()),
                        ft.ElevatedButton(
                            "Очистить готовые",
                            on_click=lambda _event: self.clear_done(),
                        ),
                    ],
                ),
            ],
            spacing=12,
        )

    def add_task(self) -> None:
        try:
            self.service.add_task(
                self.title_field.value or "",
                self.category_field.value or "",
                self.priority_dropdown.value or Priority.MEDIUM.value,
            )
        except ValueError as error:
            self._show_message(str(error))
            return

        self.title_field.value = ""
        self.category_field.value = ""
        self.priority_dropdown.value = Priority.MEDIUM.value
        self.selected_task = None
        self.refresh_tasks()

    def remove_task(self) -> None:
        if self.selected_task is None:
            self._show_message("Выберите задачу из списка")
            return

        self.service.remove_task(self.selected_task)
        self.selected_task = None
        self.refresh_tasks()

    def switch_status(self) -> None:
        if self.selected_task is None:
            self._show_message("Выберите задачу из списка")
            return

        self.service.switch_status(self.selected_task)
        self.refresh_tasks()

    def clear_done(self) -> None:
        removed_count = self.service.clear_done()
        self.selected_task = None
        self.refresh_tasks()
        self._show_message(f"Удалено выполненных задач: {removed_count}")

    def reset_filters(self) -> None:
        self.search_field.value = ""
        self.status_dropdown.value = "Все"
        self.selected_task = None
        self.refresh_tasks()

    def refresh_tasks(self) -> None:
        self.visible_tasks = self.service.get_filtered_tasks(
            self.search_field.value or "",
            self.status_dropdown.value or "Все",
        )
        self.task_list.controls.clear()

        if not self.visible_tasks:
            self.task_list.controls.append(ft.Text("Задач пока нет"))
        else:
            for task in self.visible_tasks:
                self.task_list.controls.append(self._task_row(task))

        self.stats_text.value = self.service.get_statistics().get_text()
        self._update_page()

    def select_task(self, task: Task) -> None:
        self.selected_task = task
        self.refresh_tasks()

    def _task_row(self, task: Task) -> ft.Control:
        selected = self.selected_task is task
        prefix = "-> " if selected else ""

        return ft.TextButton(
            text=f"{prefix}{task.get_text()}",
            on_click=lambda _event, selected_task=task: self.select_task(selected_task),
        )

    def _show_message(self, message: str) -> None:
        if self.page is None:
            return

        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

    def _update_page(self) -> None:
        if self.page is not None:
            self.page.update()
