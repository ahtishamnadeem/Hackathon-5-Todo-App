from typing import List, Optional
from todo_app.domain.todo import Todo
from todo_app.repository.memory import InMemoryTodoRepository

class TodoService:
    """Orchestrator for Todo operations."""

    def __init__(self, repository: InMemoryTodoRepository):
        self._repository = repository

    def create_todo(self, title: str, description: str = None) -> Todo:
        if not title.strip():
            raise ValueError("Todo title cannot be empty")
        return self._repository.add(title, description)

    def list_todos(self) -> List[Todo]:
        return self._repository.get_all()

    def complete_todo(self, todo_id: int) -> bool:
        todo = self._repository.get_by_id(todo_id)
        if todo:
            todo.completed = True
            self._repository.update(todo)
            return True
        return False

    def delete_todo(self, todo_id: int) -> bool:
        return self._repository.delete(todo_id)

    def update_todo(self, todo_id: int, title: str = None, description: str = None) -> bool:
        if title is not None and not title.strip():
            raise ValueError("Todo title cannot be empty")
        todo = self._repository.get_by_id(todo_id)
        if todo:
            if title is not None:
                todo.title = title
            if description is not None:
                todo.description = description
            self._repository.update(todo)
            return True
        return False
