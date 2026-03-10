# tools/editor_tools.py
from mcp.server.fastmcp import FastMCP, Context, Image
from typing import Optional
import base64
from godot_connection import get_godot_connection

def register_editor_tools(mcp: FastMCP):
    """Register all editor control tools with the MCP server."""
    
    @mcp.tool()
    def editor_action(ctx: Context, command: str) -> str:
        """Execute an editor command like play, stop, or save.
        
        Args:
            ctx: The MCP context
            command: The command to execute (PLAY, STOP, SAVE)
            
        Returns:
            str: Success message or error details
        """
        try:
            # Validate command
            valid_commands = ["PLAY", "STOP", "SAVE"]
            if command.upper() not in valid_commands:
                return f"Error: Invalid command '{command}'. Valid commands are {', '.join(valid_commands)}"
            
            response = get_godot_connection().send_command("EDITOR_CONTROL", {
                "command": command.upper()
            })
            
            return response.get("message", f"Editor command '{command}' executed")
        except Exception as e:
            return f"Error executing editor command: {str(e)}"
            
    @mcp.tool()
    def show_message(
        ctx: Context,
        title: str,
        message: str,
        type: str = "INFO"
    ) -> str:
        """Show a message in the Godot editor.
        
        Args:
            ctx: The MCP context
            title: Title of the message
            message: Content of the message
            type: Message type (INFO, WARNING, ERROR)
            
        Returns:
            str: Success message or error details
        """
        try:
            # Validate message type
            valid_types = ["INFO", "WARNING", "ERROR"]
            if type.upper() not in valid_types:
                return f"Error: Invalid message type '{type}'. Valid types are {', '.join(valid_types)}"
            
            response = get_godot_connection().send_command("EDITOR_CONTROL", {
                "command": "SHOW_MESSAGE",
                "params": {
                    "title": title,
                    "message": message,
                    "type": type.upper()
                }
            })
            
            return response.get("message", "Message shown in editor")
        except Exception as e:
            return f"Error showing message: {str(e)}"

    @mcp.tool()
    def play_scene(ctx: Context) -> str:
        """Start playing the current scene in the editor.
        
        Args:
            ctx: The MCP context
            
        Returns:
            str: Success message or error details
        """
        return editor_action(ctx, "PLAY")
        
    @mcp.tool()
    def stop_scene(ctx: Context) -> str:
        """Stop playing the current scene in the editor.
        
        Args:
            ctx: The MCP context
            
        Returns:
            str: Success message or error details
        """
        return editor_action(ctx, "STOP")
        
    @mcp.tool()
    def save_all(ctx: Context) -> str:
        """Save all open resources in the editor.
        
        Args:
            ctx: The MCP context
            
        Returns:
            str: Success message or error details
        """
        return editor_action(ctx, "SAVE")

    @mcp.tool()
    def capture_screenshot(ctx: Context) -> str:
        """Capture a screenshot of the Godot editor viewport and return the file path.

        Args:
            ctx: The MCP context

        Returns:
            str: Path to the saved screenshot PNG file
        """
        response = get_godot_connection().send_command("CAPTURE_SCREENSHOT", {})
        if "error" in response:
            return f"Error: {response['error']}"
        return response.get("path", "Screenshot captured but path unknown")

    @mcp.tool()
    def send_game_input(ctx: Context, command: str) -> str:
        """Send input commands to the running Godot game.

        Commands:
            move <direction> <steps> - Move player (left/right/up/down, default 1 step)
            interact - Press the interact button

        Examples:
            "move left 5" - move left 5 tiles
            "move up 3" - move up 3 tiles
            "interact" - interact with facing entity

        Args:
            ctx: The MCP context
            command: The input command string

        Returns:
            str: Success message or error details
        """
        response = get_godot_connection().send_command("SEND_INPUT", {"command": command})
        if "error" in response:
            return f"Error: {response['error']}"
        return response.get("message", "Input sent")