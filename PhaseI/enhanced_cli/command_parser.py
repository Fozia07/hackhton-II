"""
Enhanced command parser with suggestion capabilities.

This module provides advanced command parsing with suggestions for invalid commands.
"""

import re


class EnhancedCommandParser:
    """
    Enhanced command parser that provides suggestions for invalid commands.
    """

    def __init__(self):
        """
        Initialize the command parser with known commands and their aliases.
        """
        # Define valid commands and their aliases
        self.valid_commands = {
            'add': ['add'],
            'list': ['list', 'ls'],
            'update': ['update'],
            'delete': ['delete'],
            'complete': ['complete', 'done'],
            'incomplete': ['incomplete', 'undo'],
            'help': ['help', '?'],
            'exit': ['exit', 'quit']
        }

        # Flatten all possible commands for suggestion matching
        self.all_commands = []
        for aliases in self.valid_commands.values():
            self.all_commands.extend(aliases)

    def parse_command(self, user_input):
        """
        Parse the user input into command and arguments with enhanced error handling.

        Args:
            user_input (str): The raw user input

        Returns:
            tuple: (command, args, is_valid, suggestions)
        """
        user_input = user_input.strip()
        if not user_input:
            return "", [], False, ["Try typing 'help' for available commands"]

        # Split command and arguments, handling quoted strings
        parts = []
        for match in re.finditer(r'"([^"]*)"|\'([^\']*)\'|(\S+)', user_input):
            # Get the first non-None group (handles both single and double quotes)
            part = next(filter(None, match.groups()))
            parts.append(part)

        if not parts:
            return "", [], False, ["Try typing 'help' for available commands"]

        command = parts[0].lower()
        args = parts[1:]

        # Check if command is valid
        is_valid = any(command in aliases for aliases in self.valid_commands.values())

        # Generate suggestions if command is invalid
        suggestions = []
        if not is_valid:
            suggestions = self._get_command_suggestions(command)

        return command, args, is_valid, suggestions

    def _get_command_suggestions(self, invalid_command):
        """
        Generate suggestions for an invalid command.

        Args:
            invalid_command (str): The invalid command

        Returns:
            list: List of suggested commands
        """
        suggestions = []

        # Find similar commands using simple string matching
        for valid_cmd in self.all_commands:
            # If the invalid command is a prefix of a valid command
            if valid_cmd.startswith(invalid_command) and invalid_command != valid_cmd:
                suggestions.append(f"Did you mean '{valid_cmd}'?")
            # If the commands are similar in length and have small differences
            elif self._similarity(invalid_command, valid_cmd) > 0.6:
                suggestions.append(f"Did you mean '{valid_cmd}'?")

        # If no similar commands found, provide general help
        if not suggestions:
            suggestions.append("Available commands: add, list, update, delete, complete, incomplete, help, exit")
            suggestions.append("Type 'help' for a comprehensive list of commands")

        return suggestions

    def _similarity(self, str1, str2):
        """
        Calculate similarity between two strings using a simple algorithm.

        Args:
            str1 (str): First string
            str2 (str): Second string

        Returns:
            float: Similarity ratio (0.0 to 1.0)
        """
        # Convert to lowercase for comparison
        str1, str2 = str1.lower(), str2.lower()

        # Calculate common characters
        common_chars = sum(min(str1.count(c), str2.count(c)) for c in set(str1 + str2))
        total_chars = len(str1) + len(str2)

        if total_chars == 0:
            return 1.0

        return (2 * common_chars) / total_chars

    def validate_command_args(self, command, args):
        """
        Validate that the command has the correct number of arguments.

        Args:
            command (str): The command to validate
            args (list): The arguments provided

        Returns:
            tuple: (is_valid, error_message)
        """
        # Define expected argument counts for each command
        expected_args = {
            'add': (1, 'Provide a task title in quotes: add "task title"'),
            'update': (2, 'Provide task ID and new title: update <id> "new title"'),
            'delete': (1, 'Provide task ID: delete <id>'),
            'complete': (1, 'Provide task ID: complete <id>'),
            'incomplete': (1, 'Provide task ID: incomplete <id>'),
            'list': (0, 'No additional arguments needed: list'),
            'help': (0, 'No additional arguments needed: help'),
            'exit': (0, 'No additional arguments needed: exit'),
        }

        if command in expected_args:
            expected_count, error_msg = expected_args[command]
            if len(args) != expected_count:
                return False, error_msg

        return True, ""