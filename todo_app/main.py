import sys
from todo_app.repository.memory import InMemoryTodoRepository
from todo_app.services.todo_service import TodoService
from todo_app.ui.console import TodoConsole

def main():
    """Application entry point."""
    repository = InMemoryTodoRepository()
    service = TodoService(repository)
    ui = TodoConsole(service)

    try:
        ui.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
