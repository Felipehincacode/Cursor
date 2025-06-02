#!/usr/bin/env python3
"""
Media Workflow Toolbox

A collection of tools for photographers and videographers to streamline their workflow.
"""

import os
import sys
from typing import List, Callable
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Static
from textual.screen import Screen
import importlib.util
from pathlib import Path

# Initialize Rich console
console = Console()

class ToolDescription:
    def __init__(self, name: str, module: str, description: str, function: str = "main"):
        self.name = name
        self.module = module
        self.description = description
        self.function = function

# Available tools
TOOLS = [
    ToolDescription(
        "File Sorter",
        "scripts.file_sorter",
        "Sort media files into categorized folders based on their extensions",
    ),
    ToolDescription(
        "Folder Compare",
        "scripts.folder_compare",
        "Compare two folders and show missing or unmatched files",
    ),
    ToolDescription(
        "Project Generator",
        "scripts.project_generator",
        "Create standardized folder structures for photo and video projects",
    ),
]

class ToolButton(Button):
    def __init__(self, tool: ToolDescription):
        super().__init__(tool.name, id=f"tool_{tool.module}")
        self.tool = tool

class ToolboxScreen(Screen):
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Static("Select a tool to run:", classes="title"),
            *[ToolButton(tool) for tool in TOOLS],
            id="tool-list"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.button
        if isinstance(button, ToolButton):
            self.run_tool(button.tool)

    def run_tool(self, tool: ToolDescription) -> None:
        try:
            # Import the module
            module_spec = importlib.util.find_spec(tool.module)
            if module_spec is None:
                console.print(f"[red]Error: Module {tool.module} not found[/red]")
                return

            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)

            # Get the main function
            main_func = getattr(module, tool.function, None)
            if main_func is None:
                console.print(f"[red]Error: Function {tool.function} not found in {tool.module}[/red]")
                return

            # Exit the TUI temporarily
            self.app.exit()

            # Run the tool
            console.print(f"\n[blue]Running {tool.name}...[/blue]\n")
            main_func()

            # Prompt to return to menu
            input("\nPress Enter to return to the menu...")

            # Restart the TUI
            self.app.run()

        except Exception as e:
            console.print(f"[red]Error running {tool.name}: {str(e)}[/red]")
            input("\nPress Enter to return to the menu...")
            self.app.run()

class ToolboxApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #tool-list {
        width: 60;
        height: auto;
        border: solid green;
        padding: 1 2;
    }

    Button {
        width: 100%;
        margin: 1 0;
    }

    .title {
        text-align: center;
        padding: 1;
    }
    """

    def on_mount(self) -> None:
        self.push_screen(ToolboxScreen())

def main():
    """Run the Media Workflow Toolbox."""
    try:
        # Ensure scripts directory is in Python path
        scripts_dir = Path(__file__).parent
        sys.path.append(str(scripts_dir))

        # Show welcome message
        console.print(Panel.fit(
            "[bold blue]Media Workflow Toolbox[/bold blue]\n"
            "A collection of tools for photographers and videographers",
            border_style="green"
        ))

        # Start the TUI
        app = ToolboxApp()
        app.run()

    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    main() 