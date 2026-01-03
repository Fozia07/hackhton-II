"""
Display formatters for the enhanced CLI experience.

This module provides formatting functions for enhanced visual display of tasks and application elements.
"""

def format_task_list(tasks):
    """
    Format a list of tasks for display with enhanced visual indicators.

    Args:
        tasks (list): List of Task objects to format

    Returns:
        str: Formatted string representation of the task list
    """
    if not tasks:
        return "No tasks found."

    formatted_tasks = []
    for task in tasks:
        status = "x" if task.completed else " "
        formatted_task = f"{task.id}. [{status}] {task.title}"
        if task.completed:
            formatted_task += "  (COMPLETED)"
        formatted_tasks.append(formatted_task)

    result = "TASK LIST:\n"
    result += "\n".join(formatted_tasks)
    return result


def format_task(task):
    """
    Format a single task for display with enhanced visual indicators.

    Args:
        task: Task object to format

    Returns:
        str: Formatted string representation of the task
    """
    status = "x" if task.completed else " "
    formatted = f"[{status}] {task.title}"
    if task.completed:
        formatted += " (COMPLETED)"
    return formatted


def format_welcome_message():
    """
    Format the enhanced welcome message with usage instructions.

    Returns:
        str: Formatted welcome message
    """
    welcome = (
        "\n" + "="*50 + "\n"
        "Welcome to the Enhanced Console Todo Application!\n"
        + "="*50 + "\n"
        "Available commands:\n"
        "  add \"task title\"     - Add a new task\n"
        "  list (or ls)         - List all tasks\n"
        "  update id \"new title\" - Update a task title\n"
        "  delete id            - Delete a task (with confirmation)\n"
        "  complete id (or done) - Mark task as complete\n"
        "  incomplete id (or undo) - Mark task as incomplete\n"
        "  help (or ?)          - Show this help message\n"
        "  exit (or quit)       - Exit the application\n"
        "\nType 'help' for detailed command information.\n"
    )
    return welcome


def format_help_message():
    """
    Format the comprehensive help message with command descriptions.

    Returns:
        str: Formatted help message
    """
    help_text = (
        "\n" + "="*60 + "\n"
        "COMPREHENSIVE HELP - ENHANCED TODO APPLICATION\n"
        + "="*60 + "\n\n"
        "COMMANDS:\n"
        "  add \"task title\"           - Add a new task with the given title\n"
        "                              Example: add \"Buy groceries\"\n\n"
        "  list or ls                 - Display all tasks with visual indicators\n"
        "                              Shows [ ] for pending and [x] for completed\n\n"
        "  update <id> \"new title\"    - Update the title of task with specified ID\n"
        "                              Example: update 1 \"Updated task title\"\n\n"
        "  delete <id>                - Delete the task with specified ID\n"
        "                              Requires confirmation before deletion\n\n"
        "  complete <id> or done <id> - Mark task as completed\n"
        "                              Visual indicator changes to [x]\n\n"
        "  incomplete <id> or undo <id> - Mark task as incomplete\n"
        "                              Visual indicator changes to [ ]\n\n"
        "  help or ?                  - Show this comprehensive help message\n\n"
        "  exit or quit               - Exit the application\n\n"
        "VISUAL INDICATORS:\n"
        "  [ ] - Pending task\n"
        "  [x] - Completed task\n\n"
        "KEYBOARD SHORTCUTS:\n"
        "  Some commands have shortcuts for faster access\n"
        "  Use any of the alternative forms shown above\n"
        + "="*60 + "\n"
    )
    return help_text


def format_error_message(error, suggestions=None):
    """
    Format an error message with helpful suggestions.

    Args:
        error (str): The error message
        suggestions (list): Optional list of suggestions to fix the error

    Returns:
        str: Formatted error message with suggestions
    """
    formatted = f"\nERROR: {error}\n"

    if suggestions:
        formatted += "\nSuggestions:\n"
        for i, suggestion in enumerate(suggestions, 1):
            formatted += f"  {i}. {suggestion}\n"

    formatted += "\nTip: Type 'help' for a list of all available commands.\n"
    return formatted


def format_confirmation_prompt(action, item):
    """
    Format a confirmation prompt for potentially destructive operations.

    Args:
        action (str): The action to confirm (e.g., "delete")
        item (str): The item being acted upon

    Returns:
        str: Formatted confirmation prompt
    """
    return f"\nAre you sure you want to {action} {item}? (y/N): "