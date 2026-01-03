"""
Interactive session management for the enhanced CLI experience.

This module manages the state of the interactive session including command history and session state.
"""

class InteractiveSession:
    """
    Manages the state of an interactive CLI session.
    """

    def __init__(self):
        """
        Initialize the interactive session with default values.
        """
        self.session_id = self._generate_session_id()
        self.command_history = []
        self.current_state = "main_menu"
        self.selected_task_id = None
        self.filter_mode = "all"  # "all", "pending", "completed"
        self.history_limit = 100  # Limit the command history size

    def _generate_session_id(self):
        """
        Generate a unique session ID.

        Returns:
            str: A unique session identifier
        """
        import time
        import random
        return f"session_{int(time.time())}_{random.randint(1000, 9999)}"

    def add_command_to_history(self, command):
        """
        Add a command to the session history.

        Args:
            command (str): The command to add to history
        """
        self.command_history.append(command)

        # Limit history size
        if len(self.command_history) > self.history_limit:
            self.command_history = self.command_history[-self.history_limit:]

    def get_command_history(self):
        """
        Get the command history.

        Returns:
            list: List of previously executed commands
        """
        return self.command_history.copy()

    def set_current_state(self, state):
        """
        Set the current interaction state.

        Args:
            state (str): The new state (e.g., "main_menu", "adding_task", "updating_task")
        """
        valid_states = [
            "main_menu",
            "adding_task",
            "updating_task",
            "viewing_tasks",
            "deleting_task",
            "help_menu"
        ]

        if state in valid_states:
            self.previous_state = self.current_state
            self.current_state = state
        else:
            raise ValueError(f"Invalid state: {state}. Valid states are: {valid_states}")

    def get_current_state(self):
        """
        Get the current interaction state.

        Returns:
            str: The current state
        """
        return self.current_state

    def set_selected_task(self, task_id):
        """
        Set the currently selected task ID.

        Args:
            task_id (int or None): The ID of the selected task, or None if none selected
        """
        if task_id is None or isinstance(task_id, int):
            self.selected_task_id = task_id
        else:
            raise ValueError("Task ID must be an integer or None")

    def get_selected_task(self):
        """
        Get the currently selected task ID.

        Returns:
            int or None: The ID of the selected task, or None if none selected
        """
        return self.selected_task_id

    def set_filter_mode(self, mode):
        """
        Set the current task filtering mode.

        Args:
            mode (str): The filter mode ("all", "pending", "completed")
        """
        valid_modes = ["all", "pending", "completed"]
        if mode in valid_modes:
            self.filter_mode = mode
        else:
            raise ValueError(f"Invalid filter mode: {mode}. Valid modes are: {valid_modes}")

    def get_filter_mode(self):
        """
        Get the current task filtering mode.

        Returns:
            str: The current filter mode
        """
        return self.filter_mode

    def reset_session_state(self):
        """
        Reset the session to its initial state.
        """
        self.current_state = "main_menu"
        self.selected_task_id = None
        self.filter_mode = "all"

    def get_session_info(self):
        """
        Get information about the current session.

        Returns:
            dict: Dictionary containing session information
        """
        return {
            "session_id": self.session_id,
            "current_state": self.current_state,
            "selected_task_id": self.selected_task_id,
            "filter_mode": self.filter_mode,
            "command_history_count": len(self.command_history)
        }

    def clear_command_history(self):
        """
        Clear the command history.
        """
        self.command_history = []

    def get_recent_commands(self, count=5):
        """
        Get the most recent commands from history.

        Args:
            count (int): Number of recent commands to return

        Returns:
            list: List of recent commands
        """
        return self.command_history[-count:] if len(self.command_history) >= count else self.command_history


class CommandHistoryManager:
    """
    Manages command history with additional functionality.
    """

    def __init__(self, session):
        """
        Initialize the command history manager.

        Args:
            session (InteractiveSession): The session to manage history for
        """
        self.session = session

    def search_history(self, pattern):
        """
        Search for commands in history that match a pattern.

        Args:
            pattern (str): The pattern to search for

        Returns:
            list: List of matching commands
        """
        return [cmd for cmd in self.session.get_command_history() if pattern.lower() in cmd.lower()]

    def get_command_suggestions(self):
        """
        Get suggestions based on command history.

        Returns:
            list: List of commonly used commands
        """
        from collections import Counter
        cmd_counter = Counter(self.session.get_command_history())
        # Return the 5 most common commands
        return [cmd for cmd, count in cmd_counter.most_common(5)]