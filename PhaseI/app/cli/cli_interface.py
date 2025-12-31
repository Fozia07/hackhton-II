"""
Command-line interface for the console todo application.

This module handles user input and provides a command-line interface for the todo application.
"""
import re
from typing import Tuple, Optional
from app.services.task_service import TaskService


class CLIInterface:
    """
    Command-line interface for interacting with the task service.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the CLI interface with a task service.

        Args:
            task_service (TaskService): The task service to interact with
        """
        self.task_service = task_service
        self.running = True

    def display_help(self):
        """
        Display help information for available commands.
        """
        print("\nAvailable commands:")
        print("  add \"task title\"     - Add a new task")
        print("  list (or ls)         - List all tasks")
        print("  update id \"new title\" - Update a task title")
        print("  delete id            - Delete a task")
        print("  complete id (or done) - Mark task as complete")
        print("  incomplete id (or undo) - Mark task as incomplete")
        print("  help (or ?)          - Show this help message")
        print("  exit (or quit)       - Exit the application")
        print()

    def parse_command(self, user_input: str) -> Tuple[str, list]:
        """
        Parse the user input into command and arguments.

        Args:
            user_input (str): The raw user input

        Returns:
            Tuple[str, list]: The command and list of arguments
        """
        user_input = user_input.strip()
        if not user_input:
            return "", []

        # Split command and arguments, handling quoted strings
        parts = []
        # This regex matches either quoted strings or unquoted words
        for match in re.finditer(r'"([^"]*)"|\'([^\']*)\'|(\S+)', user_input):
            # Get the first non-None group (handles both single and double quotes)
            part = next(filter(None, match.groups()))
            parts.append(part)

        if not parts:
            return "", []

        command = parts[0].lower()
        args = parts[1:]

        return command, args

    def handle_add(self, args: list):
        """
        Handle the add command.

        Args:
            args (list): List of arguments for the add command
        """
        if len(args) < 1:
            print("Error: Please provide a task title in quotes")
            print('Example: add "Buy groceries"')
            return

        title = " ".join(args)
        try:
            task = self.task_service.add_task(title)
            print(f"Task {task.id} added: {task.title} [PENDING]")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_list(self, args: list):
        """
        Handle the list command.

        Args:
            args (list): List of arguments for the list command
        """
        tasks = self.task_service.get_all_tasks()
        if not tasks:
            print("No tasks found.")
            return

        print("\nTask List:")
        for task in tasks:
            status = "x" if task.completed else " "
            print(f"{task.id}. [{status}] {task.title}")
        print()

    def handle_update(self, args: list):
        """
        Handle the update command.

        Args:
            args (list): List of arguments for the update command
        """
        if len(args) < 2:
            print("Error: Please provide task ID and new title")
            print('Example: update 1 "New task title"')
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        new_title = " ".join(args[1:])

        try:
            updated_task = self.task_service.update_task(task_id, new_title)
            if updated_task:
                print(f"Task {task_id} updated to: {updated_task.title}")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_delete(self, args: list):
        """
        Handle the delete command.

        Args:
            args (list): List of arguments for the delete command
        """
        if len(args) < 1:
            print("Error: Please provide a task ID")
            print("Example: delete 1")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        deleted = self.task_service.delete_task(task_id)
        if deleted:
            print(f"Task {task_id} deleted")
        else:
            print(f"Error: Task with ID {task_id} not found")

    def handle_complete(self, args: list):
        """
        Handle the complete command.

        Args:
            args (list): List of arguments for the complete command
        """
        if len(args) < 1:
            print("Error: Please provide a task ID")
            print("Example: complete 1")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        completed = self.task_service.complete_task(task_id)
        if completed:
            print(f"Task {task_id} marked as complete")
        else:
            print(f"Error: Task with ID {task_id} not found")

    def handle_incomplete(self, args: list):
        """
        Handle the incomplete command.

        Args:
            args (list): List of arguments for the incomplete command
        """
        if len(args) < 1:
            print("Error: Please provide a task ID")
            print("Example: incomplete 1")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        incompleted = self.task_service.incomplete_task(task_id)
        if incompleted:
            print(f"Task {task_id} marked as incomplete")
        else:
            print(f"Error: Task with ID {task_id} not found")

    def handle_command(self, command: str, args: list):
        """
        Handle a parsed command.

        Args:
            command (str): The command to handle
            args (list): List of arguments for the command
        """
        # Map command aliases to their primary function
        if command in ["add"]:
            self.handle_add(args)
        elif command in ["list", "ls"]:
            self.handle_list(args)
        elif command in ["update"]:
            self.handle_update(args)
        elif command in ["delete"]:
            self.handle_delete(args)
        elif command in ["complete", "done"]:
            self.handle_complete(args)
        elif command in ["incomplete", "undo"]:
            self.handle_incomplete(args)
        elif command in ["help", "?"]:
            self.display_help()
        elif command in ["exit", "quit"]:
            self.running = False
            print("Goodbye!")
        else:
            print(f"Error: Unknown command '{command}'. Type 'help' for available commands.")

    def run(self):
        """
        Run the command-line interface loop.
        """
        print("Welcome to the Console Todo Application!")
        print("Type 'help' for available commands or 'exit' to quit.")

        while self.running:
            try:
                user_input = input("> ").strip()
                if not user_input:
                    continue

                command, args = self.parse_command(user_input)
                self.handle_command(command, args)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break