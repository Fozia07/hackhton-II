"""
AI Agent Service for the Todo AI Chatbot.
Integrates Google Gemini native API with MCP tools for task operations.
"""
import asyncio
import json
from typing import List, Dict, Any, Optional, Tuple
import httpx
from app.core.config import config
from app.services.mcp_client import mcp_client
from app.models import Message
from app.database.session import get_async_session
from sqlmodel import select


class AIAgentService:
    """
    Service class to handle AI agent operations with MCP tools integration.
    Uses Google Gemini native REST API.
    """

    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.api_key = config.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = config.openai_model  # Read from .env file
        self.temperature = config.ai_temperature
        self.max_tokens = config.ai_max_tokens

    def _define_tools(self) -> List[Dict]:
        """
        Define available tools in Gemini function_declarations format.

        Returns:
            List of function declarations for Gemini API
        """
        return [
            {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the task"
                        }
                    },
                    "required": ["user_id", "title"]
                }
            },
            {
                "name": "list_tasks",
                "description": "Retrieve tasks for the user with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter tasks by status (all, pending, completed)"
                        }
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to complete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "Remove a task from the user's list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to delete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            {
                "name": "update_task",
                "description": "Modify properties of an existing task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "New description for the task"
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "New completion status for the task"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        ]

    def _convert_to_gemini_format(self, messages: List[Dict[str, str]]) -> Dict:
        """
        Convert conversation messages to Gemini contents format.

        Args:
            messages: List of messages in OpenAI format

        Returns:
            Dictionary with 'contents' and 'tools' fields for Gemini API
        """
        contents = []

        # Skip system message and convert the rest
        for msg in messages:
            if msg["role"] == "system":
                # Gemini doesn't have system role, we'll prepend it to first user message
                continue
            elif msg["role"] == "user":
                contents.append({
                    "role": "user",
                    "parts": [{"text": msg["content"]}]
                })
            elif msg["role"] == "assistant":
                contents.append({
                    "role": "model",
                    "parts": [{"text": msg["content"]}]
                })

        # Prepend system instructions to first user message if exists
        system_msg = next((m for m in messages if m["role"] == "system"), None)
        if system_msg and contents and contents[0]["role"] == "user":
            original_text = contents[0]["parts"][0]["text"]
            contents[0]["parts"][0]["text"] = f"{system_msg['content']}\n\nUser: {original_text}"

        return {
            "contents": contents,
            "tools": [{"function_declarations": self._define_tools()}]
        }

    def _parse_gemini_response(self, response_data: Dict) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Parse Gemini API response.

        Args:
            response_data: Raw API response JSON

        Returns:
            Tuple of (response_text, function_call_data)
        """
        try:
            candidate = response_data.get("candidates", [{}])[0]
            content = candidate.get("content", {})
            parts = content.get("parts", [{}])

            if not parts:
                return None, None

            first_part = parts[0]

            # Check for function call
            if "functionCall" in first_part:
                function_call = first_part["functionCall"]
                return None, {
                    "name": function_call.get("name"),
                    "args": function_call.get("args", {})
                }

            # Check for text response
            if "text" in first_part:
                return first_part["text"], None

            return None, None

        except (KeyError, IndexError) as e:
            return f"Error parsing response: {str(e)}", None

    async def _execute_tool(self, function_name: str, arguments: Dict, user_id: str) -> str:
        """
        Execute tool/function call.

        Args:
            function_name: Name of function to execute
            arguments: Function arguments
            user_id: User ID for task operations

        Returns:
            Tool execution result as JSON string
        """
        try:
            if function_name == "add_task":
                result = await mcp_client.add_task(**arguments)
            elif function_name == "list_tasks":
                result = await mcp_client.list_tasks(**arguments)
            elif function_name == "complete_task":
                result = await mcp_client.complete_task(**arguments)
            elif function_name == "delete_task":
                result = await mcp_client.delete_task(**arguments)
            elif function_name == "update_task":
                result = await mcp_client.update_task(**arguments)
            else:
                result = {"error": f"Unknown tool: {function_name}"}

            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})

    async def process_conversation(self, user_id: str, conversation_id: str, user_message: str) -> tuple[str, List[Dict[str, Any]]]:
        """
        Process a conversation with the AI agent, allowing it to use MCP tools.

        Args:
            user_id: ID of the user
            conversation_id: ID of the conversation
            user_message: User's message to process

        Returns:
            Tuple of (AI-generated response, list of tool calls made)
        """
        # Get conversation history from the database
        conversation_history = await self._get_conversation_history(conversation_id, user_id)

        # Build the messages array for the AI agent
        messages = self._build_messages_for_agent(conversation_history, user_message)

        # Track tool calls made during the conversation
        executed_tool_calls = []

        try:
            # Build Gemini API URL
            url = f"{self.base_url}/models/{self.model}:generateContent"
            params = {"key": self.api_key}

            # Log the request details for debugging
            print(f"[DEBUG] Making request to: {url}")
            print(f"[DEBUG] Model: {self.model}")
            print(f"[DEBUG] Base URL: {self.base_url}")

            # Convert messages to Gemini format
            request_body = self._convert_to_gemini_format(messages)

            # Make first API call to Gemini
            response = await self.http_client.post(url, params=params, json=request_body)

            print(f"[DEBUG] Response status: {response.status_code}")

            response.raise_for_status()
            response_data = response.json()

            # Parse the response
            text, function_call = self._parse_gemini_response(response_data)

            # If the model wants to call a function, execute it
            if function_call:
                function_name = function_call["name"]
                function_args = function_call["args"]

                print(f"[DEBUG] Function call detected: {function_name}")

                # Record the tool call
                executed_tool_calls.append({
                    "function": {
                        "name": function_name,
                        "arguments": json.dumps(function_args)
                    },
                    "type": "function"
                })

                # Execute the tool
                tool_result = await self._execute_tool(function_name, function_args, user_id)

                # Build second request with function result
                # Add the function call to contents
                request_body["contents"].append({
                    "role": "model",
                    "parts": [{"functionCall": function_call}]
                })

                # Add the function response
                request_body["contents"].append({
                    "role": "function",
                    "parts": [{
                        "functionResponse": {
                            "name": function_name,
                            "response": {"result": tool_result}
                        }
                    }]
                })

                # Make second API call to get final response
                final_response = await self.http_client.post(url, params=params, json=request_body)
                final_response.raise_for_status()
                final_response_data = final_response.json()

                # Parse final response
                final_text, _ = self._parse_gemini_response(final_response_data)

                return final_text or "Task completed successfully.", executed_tool_calls

            else:
                # If no function was called, return the text response directly
                return text or "I'm here to help with your tasks!", []

        except httpx.HTTPStatusError as e:
            # Handle HTTP errors with detailed logging
            error_detail = f"Status: {e.response.status_code}, Response: {e.response.text[:500]}"
            print(f"[ERROR] HTTP Status Error: {error_detail}")

            # Handle rate limit errors with friendly message
            if e.response.status_code == 429:
                error_msg = "I'm currently experiencing high demand. Please wait a moment and try again."
            else:
                error_msg = f"Sorry, I encountered an API error: {e.response.status_code}. Please try again."

            return error_msg, [{"error": e.response.text}]
        except Exception as e:
            # Handle any other errors
            print(f"[ERROR] Exception: {str(e)}")
            error_msg = f"Sorry, I encountered an error processing your request: {str(e)}. Please try again."
            return error_msg, [{"error": str(e)}]

    async def _get_conversation_history(self, conversation_id: str, user_id: str) -> List[Message]:
        """
        Get conversation history from the database.

        Args:
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user who owns the conversation

        Returns:
            List of messages in the conversation
        """
        async for session in get_async_session():
            try:
                statement = select(Message).where(
                    Message.conversation_id == conversation_id,
                    Message.user_id == user_id
                ).order_by(Message.sequence_number)

                result = await session.exec(statement)
                return result.all()
            except Exception:
                # Return empty list if there's an error
                return []

    def _build_messages_for_agent(self, conversation_history: List[Message], new_user_message: str) -> List[Dict[str, str]]:
        """
        Build the messages array for the AI agent, converting from our database format.

        Args:
            conversation_history: List of messages from the database
            new_user_message: The new user message to add to the conversation

        Returns:
            List of messages formatted for the OpenAI API
        """
        import json
        from datetime import datetime

        # System message with instructions for the AI agent
        messages = [{
            "role": "system",
            "content": """You are a helpful AI assistant that helps users manage their tasks.

IMPORTANT: You have access to 5 tools that you MUST use when appropriate:
- add_task: When user wants to add/create a new task, you MUST call this tool
- list_tasks: When user wants to see/view/list their tasks, you MUST call this tool
- complete_task: When user says a task is done/completed, you MUST call this tool
- delete_task: When user wants to remove/delete a task, you MUST call this tool
- update_task: When user wants to change/modify a task, you MUST call this tool

CRITICAL: Always use the appropriate tool for task operations. Do not just describe what you would do - actually call the tool.

After calling a tool, respond in a friendly, helpful manner:
- For successful actions: "Added task 'Buy groceries' ✅", "Completed task 'Clean room' ✅", etc.
- For errors: "Couldn't find that task, sorry!", "Task not found - please check the task name", etc.

If a user tries to operate on a task that doesn't exist, respond with a friendly error message."""
        }]

        # Convert conversation history to OpenAI format
        for message in conversation_history:
            messages.append({
                "role": message.role,
                "content": message.content
            })

        # Add the new user message
        messages.append({
            "role": "user",
            "content": new_user_message
        })

        return messages


# Global AI agent instance
ai_agent = AIAgentService()