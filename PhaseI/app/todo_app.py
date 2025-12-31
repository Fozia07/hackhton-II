"""
Main entry point for the console todo application.

This module initializes the application components and starts the CLI interface.
"""
from app.services.task_service import TaskService
from app.cli.cli_interface import CLIInterface


def main():
    """
    Main function to run the console todo application.
    """
    # Initialize the task service
    task_service = TaskService()

    # Initialize the CLI interface with the task service
    cli_interface = CLIInterface(task_service)

    # Start the application
    cli_interface.run()


if __name__ == "__main__":
    main()