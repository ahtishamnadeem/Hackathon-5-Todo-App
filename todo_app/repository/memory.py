from typing import List, Optional
from todo_app.domain.todo import Todo

class InMemoryTodoRepository:
    """In-memory storage for todos using a dictionary."""

    def __init__(self):
        self._todos = {}
        self._next_id = 1

    def add(self, title: str, description: str = None) -> Todo:
        todo = Todo(id=self._next_id, title=title, description=description)
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo

    def get_all(self) -> List[Todo]:
        return list(self._todos.values())

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        return self._todos.get(todo_id)

    def update(self, todo: Todo) -> Optional[Todo]:
        if todo.id in self._todos:
            self._todos[todo.id] = todo
            return todo
        return None

    def delete(self, todo_id: int) -> bool:
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False
