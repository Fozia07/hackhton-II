"""
Enhanced command-line interface for the console todo application.

This module handles user input and provides an enhanced command-line interface for the todo application.
"""

import re
import sys
import os
from typing import Tuple, Optional

# Add the PhaseI directory to the Python path to resolve imports
phase_i_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, phase_i_dir)

from app.services.task_service import TaskService
from enhanced_cli.display_formatters import (
    format_task_list, format_welcome_message, format_help_message,
    format_error_message, format_confirmation_prompt
)
from enhanced_cli.command_parser import EnhancedCommandParser
from enhanced_cli.interactive_session import InteractiveSession


class CLIInterface:
    """
    Enhanced command-line interface for interacting with the task service.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the CLI interface with a task service.

        Args:
            task_service (TaskService): The task service to interact with
        """
        self.task_service = task_service
        self.running = True
        self.command_parser = EnhancedCommandParser()
        self.interactive_session = InteractiveSession()

        # Command history functionality
        self.command_history = []

    def display_welcome(self):
        """
        Display the enhanced welcome message with usage instructions.
        """
        print(format_welcome_message())

    def display_help(self):
        """
        Display the comprehensive help message with command descriptions.
        """
        print(format_help_message())

    def parse_command(self, user_input: str) -> Tuple[str, list, bool, list]:
        """
        Parse the user input into command and arguments with enhanced error handling.

        Args:
            user_input (str): The raw user input

        Returns:
            Tuple[str, list, bool, list]: The command, arguments, validity, and suggestions
        """
        command, args, is_valid, suggestions = self.command_parser.parse_command(user_input)

        # Validate command arguments
        if is_valid:
            args_valid, error_msg = self.command_parser.validate_command_args(command, args)
            if not args_valid:
                is_valid = False
                suggestions = [error_msg]

        return command, args, is_valid, suggestions

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
            # Add command to history
            self.interactive_session.add_command_to_history(f"add {title}")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_list(self, args: list):
        """
        Handle the list command.

        Args:
            args (list): List of arguments for the list command
        """
        tasks = self.task_service.get_all_tasks()
        formatted_output = format_task_list(tasks)
        print(formatted_output)
        # Add command to history
        self.interactive_session.add_command_to_history("list")

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
                # Add command to history
                self.interactive_session.add_command_to_history(f"update {task_id} {new_title}")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_delete(self, args: list):
        """
        Handle the delete command with confirmation.

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

        # Get the task to show in confirmation
        task = self.task_service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found")
            return

        # Show confirmation prompt
        confirmation = input(format_confirmation_prompt("delete", f"task '{task.title}'")).strip().lower()

        if confirmation in ['y', 'yes']:
            deleted = self.task_service.delete_task(task_id)
            if deleted:
                print(f"Task {task_id} deleted")
                # Add command to history
                self.interactive_session.add_command_to_history(f"delete {task_id}")
            else:
                print(f"Error: Task with ID {task_id} not found")
        else:
            print("Deletion cancelled.")

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
            # Add command to history
            self.interactive_session.add_command_to_history(f"complete {task_id}")
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
            # Add command to history
            self.interactive_session.add_command_to_history(f"incomplete {task_id}")
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
            # Handle invalid command with suggestions
            suggestions = self.command_parser._get_command_suggestions(command)
            error_msg = f"Unknown command '{command}'"
            formatted_error = format_error_message(error_msg, suggestions)
            print(formatted_error)

    def run(self):
        """
        Run the enhanced command-line interface loop.
        """
        self.display_welcome()

        while self.running:
            try:
                user_input = input("> ").strip()
                if not user_input:
                    continue

                # Parse command with enhanced parser
                command, args, is_valid, suggestions = self.parse_command(user_input)

                if not is_valid and command != "":
                    # Handle invalid command with suggestions
                    error_msg = f"Unknown command '{command}'"
                    formatted_error = format_error_message(error_msg, suggestions)
                    print(formatted_error)
                    continue

                # Add command to history if valid
                if command not in ["exit", "quit"]:
                    self.interactive_session.add_command_to_history(user_input)

                self.handle_command(command, args)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break