#!/usr/bin/env python3
"""
Test script to demonstrate Phase I functionality.
This script shows how the Phase I console todo application works.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PhaseI'))

from app.services.task_service import TaskService
from app.cli.cli_interface import CLIInterface
from enhanced_cli.display_formatters import format_task_list, format_welcome_message, format_help_message

def demo_phase1_features():
    """Demonstrate the Phase I console todo application features."""
    print("=== Phase I: Enhanced Console Todo Application Demo ===\n")

    # Initialize the task service
    task_service = TaskService()

    # Show welcome message
    print(format_welcome_message())

    print("\n--- Available Commands ---")
    print(format_help_message())

    print("\n--- Testing Basic Functionality ---")

    # Add some test tasks
    print("\n1. Adding tasks:")
    task1 = task_service.add_task("Buy groceries")
    print(f"   Added: Task {task1.id} - {task1.title} [PENDING]")

    task2 = task_service.add_task("Complete Phase I")
    print(f"   Added: Task {task2.id} - {task2.title} [PENDING]")

    # List all tasks
    print("\n2. Listing tasks:")
    tasks = task_service.get_all_tasks()
    formatted_output = format_task_list(tasks)
    print(formatted_output)

    # Complete a task
    print("\n3. Completing a task:")
    success = task_service.complete_task(1)
    if success:
        print(f"   Task 1 marked as complete")

    # List tasks again to show the change
    print("\n4. Updated task list:")
    tasks = task_service.get_all_tasks()
    formatted_output = format_task_list(tasks)
    print(formatted_output)

    print("\n=== Phase I Demo Complete ===")
    print("The Phase I application provides:")
    print("- Enhanced CLI with clear commands")
    print("- Task management (add, list, update, delete, complete, incomplete)")
    print("- In-memory storage")
    print("- Confirmation prompts for destructive operations")
    print("- Sequential task IDs starting from 1")
    print("- Visual indicators for task status")

if __name__ == "__main__":
    demo_phase1_features()