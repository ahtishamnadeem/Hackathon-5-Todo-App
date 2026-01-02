import os

class TodoConsole:
    """CLI Interface for the Todo Application."""

    def __init__(self, service):
        self.service = service

    def _clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_header(self, title):
        print(f"\n--- {title} ---")

    def _display_menu(self):
        print("\nMulti-Phase Todo App (Phase I)")
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Update Todo Title")
        print("4. Delete Todo")
        print("5. Mark Complete")
        print("6. Exit")

    def run(self):
        """Runs the main application loop."""
        while True:
            self._display_menu()
            choice = input("\nSelect an option (1-6): ").strip()

            if choice == '1':
                self._add_todo()
            elif choice == '2':
                self._view_todos()
            elif choice == '3':
                self._update_todo()
            elif choice == '4':
                self._delete_todo()
            elif choice == '5':
                self._mark_complete()
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Error: Invalid selection. Please choose 1-6.")

    def _add_todo(self):
        self._print_header("Add New Todo")
        title = input("Enter todo title: ").strip()
        description = input("Enter todo description (optional): ").strip()
        if not description:
            description = None
        try:
            todo = self.service.create_todo(title, description)
            print(f"Success: Added '{todo.title}' (ID: {todo.id})")
        except ValueError as e:
            print(f"Error: {e}")

    def _view_todos(self):
        self._print_header("Your Todo List")
        todos = self.service.list_todos()

        if not todos:
            print("Your todo list is currently empty.")
            return

        print(f"{'ID':<4} {'Status':<12} {'Title':<30} {'Description'}")
        print("-" * 60)
        for todo in todos:
            status = "[Done]" if todo.completed else "[Pending]"
            description = todo.description if todo.description else ""
            print(f"{todo.id:<4} {status:<12} {todo.title:<30} {description}")

    def _get_int_input(self, prompt):
        val = input(prompt).strip()
        if not val.isdigit():
            raise ValueError("ID must be a number.")
        return int(val)

    def _update_todo(self):
        self._print_header("Update Todo")
        try:
            todo_id = self._get_int_input("Enter Todo ID to update: ")
            todo = self.service._repository.get_by_id(todo_id)
            if not todo:
                print(f"Error: Todo ID {todo_id} not found.")
                return

            current_title = input(f"Enter new title (current: '{todo.title}'): ").strip()
            if not current_title:
                current_title = None

            current_description = input(f"Enter new description (current: '{todo.description or ''}'): ").strip()
            if not current_description:
                current_description = None

            if self.service.update_todo(todo_id, current_title, current_description):
                print(f"Success: Updated Todo {todo_id}")
            else:
                print(f"Error: Todo ID {todo_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")

    def _delete_todo(self):
        self._print_header("Delete Todo")
        try:
            todo_id = self._get_int_input("Enter Todo ID to delete: ")
            if self.service.delete_todo(todo_id):
                print(f"Success: Deleted Todo {todo_id}")
            else:
                print(f"Error: Todo ID {todo_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")

    def _mark_complete(self):
        self._print_header("Mark Todo Complete")
        try:
            todo_id = self._get_int_input("Enter Todo ID to complete: ")
            if self.service.complete_todo(todo_id):
                print(f"Success: Marked Todo {todo_id} as complete.")
            else:
                print(f"Error: Todo ID {todo_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
