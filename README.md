# GIAIC HACKATHON (5 - PHASES)
# Multi-Phase Todo Application - Phase I

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Phase](https://img.shields.io/badge/Phase-I-yellow.svg)](https://github.com/yourusername/hackathon-5-todoapp)

**🎯 In-Memory Console Todo App | Clean Architecture | Spec-Driven Development**

</div>

## 🌟 Overview

Welcome to the **Multi-Phase Todo Application**! This project represents the successful completion of **Phase I** - an in-memory Python console todo application that establishes the foundational architecture for future phases (web, AI, cloud).

Built with clean architecture principles and spec-driven development, this application demonstrates a robust, extensible foundation for a todo management system.

## ✨ Features

- **📋 Add Todos**: Create new todo items with title and description
- **👀 View Todos**: Display all todos with status, title, and description
- **✏️ Update Todos**: Modify todo titles and descriptions
- **✅ Complete Todos**: Mark todos as completed
- **🗑️ Delete Todos**: Remove todos from memory
- **🛡️ Input Validation**: Defensive validation for all user inputs
- **⚡ In-Memory Storage**: Fast, temporary storage for runtime sessions

## 🏗️ Architecture

This application follows a clean, layered architecture with clear separation of concerns:

```
todo_app/
├── main.py            # Application entry point & app loop
├── domain/
│   └── todo.py        # Todo entity (dataclass)
├── repository/
│   └── memory.py      # In-memory storage (dict-based)
├── services/
│   └── todo_service.py # Business logic orchestrator
└── ui/
    └── console.py     # CLI interface
```

### Layer Responsibilities

- **Domain Layer**: Defines the Todo entity and business rules
- **Repository Layer**: Handles in-memory data storage and retrieval
- **Service Layer**: Orchestrates business logic and operations
- **UI Layer**: Manages console input/output and user interaction

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- UV package manager

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd hackathon-5-todoapp
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   python -m todo_app.main
   ```

### Usage

Once the application is running, you'll see an interactive menu:

```
Multi-Phase Todo App (Phase I)
1. Add Todo
2. View Todos
3. Update Todo Title
4. Delete Todo
5. Mark Complete
6. Exit
```

Simply follow the prompts to manage your todos!

## 📖 Example Workflow

1. **Add a Todo**:
   - Select option `1`
   - Enter a title (e.g., "Buy groceries")
   - Enter an optional description (e.g., "Milk, eggs, bread")

2. **View Todos**:
   - Select option `2`
   - See all todos with their status and details

3. **Update a Todo**:
   - Select option `3`
   - Enter the Todo ID
   - Update the title or description

4. **Mark Complete**:
   - Select option `5`
   - Enter the Todo ID to mark as complete

5. **Delete a Todo**:
   - Select option `4`
   - Enter the Todo ID to remove

## 🏗️ Design Principles

This application follows several key design principles:

- **Simplicity First**: Clean, readable code without unnecessary complexity
- **Separation of Concerns**: Clear boundaries between domain, repository, service, and UI layers
- **Spec-Driven Development**: Built against verified specifications
- **Deterministic Behavior**: Predictable input/output behavior
- **Developer-Friendly**: Easy to run, test, and understand

## 📊 Technical Details

- **Language**: Python 3.13+
- **Architecture**: Layered (Domain → Repository → Service → UI)
- **Storage**: In-memory dictionary (no persistence)
- **Interface**: Console/CLI
- **Dependencies**: Standard library only (no external packages)
- **Testing**: Manual verification via CLI

## 🎯 Phase I Completion

Phase I successfully delivers:

- ✅ Complete CRUD operations (Create, Read, Update, Delete)
- ✅ Mark todos as complete/incomplete
- ✅ In-memory storage with no persistence
- ✅ Clean, maintainable codebase
- ✅ Proper error handling and input validation
- ✅ Extensible architecture for future phases

## 🔄 Future Phases

This foundation enables future phases:

- **Phase II**: Full-stack web application with persistent storage
- **Phase III**: AI-powered chatbot interface
- **Phase IV**: Local Kubernetes deployment
- **Phase V**: Advanced cloud deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Spec-Driven Development](https://spec-driven.com) methodology
- Clean Architecture principles
- Python 3.13+ ecosystem
- UV package manager

---

<div align="center">

**Made with ❤️ during Hackathon-5**

[Back to Top](#multi-phase-todo-application---phase-i)

</div>