#!/usr/bin/env python3
"""
Project Template Generator

Create standardized folder structures for photo and video projects.
Supports custom templates and project initialization.
"""

import os
import json
from pathlib import Path
from typing import Dict, List
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from loguru import logger
import typer
from datetime import datetime

# Configure logger
logger.add("project_generator.log", rotation="1 MB")

# Initialize Rich console
console = Console()

# Default templates
DEFAULT_TEMPLATES = {
    "photo_basic": {
        "structure": {
            "RAW": {},
            "JPEG": {},
            "Edited": {
                "Finals": {},
                "Web": {},
                "Social": {}
            },
            "Lightroom": {},
            "References": {}
        },
        "description": "Basic photography project structure"
    },
    "video_basic": {
        "structure": {
            "01_Footage": {
                "RAW": {},
                "B-Roll": {},
                "Audio": {}
            },
            "02_Assets": {
                "Music": {},
                "SFX": {},
                "Graphics": {},
                "LUTs": {}
            },
            "03_Project_Files": {
                "Premiere": {},
                "After_Effects": {}
            },
            "04_Exports": {
                "Drafts": {},
                "Finals": {},
                "Web": {}
            }
        },
        "description": "Basic video project structure"
    }
}

def load_templates(templates_file: Path) -> Dict:
    """Load custom templates from a JSON file or return defaults."""
    if templates_file.exists():
        try:
            with open(templates_file) as f:
                custom_templates = json.load(f)
                return {**DEFAULT_TEMPLATES, **custom_templates}
        except json.JSONDecodeError:
            logger.warning(f"Error reading {templates_file}. Using default templates.")
    return DEFAULT_TEMPLATES

def save_template(templates_file: Path, template_name: str, structure: Dict) -> None:
    """Save a new template to the templates file."""
    templates = load_templates(templates_file)
    templates[template_name] = {
        "structure": structure,
        "description": f"Custom template: {template_name}"
    }
    
    with open(templates_file, 'w') as f:
        json.dump(templates, f, indent=4)
    logger.info(f"Saved new template: {template_name}")

def create_structure(base_path: Path, structure: Dict, prefix: str = "") -> None:
    """Recursively create folder structure."""
    for name, substructure in structure.items():
        folder_path = base_path / f"{prefix}{name}"
        folder_path.mkdir(exist_ok=True)
        if substructure:  # If there are subfolders
            create_structure(folder_path, substructure)

def generate_project(
    project_name: str = typer.Argument(..., help="Name of the project"),
    template: str = typer.Option("photo_basic", "--template", "-t", help="Template to use"),
    base_dir: str = typer.Option(".", "--dir", "-d", help="Base directory for the project"),
    date_prefix: bool = typer.Option(True, "--date-prefix/--no-date-prefix", help="Add date prefix to project folder"),
) -> None:
    """
    Generate a new project structure from a template.
    
    Args:
        project_name: Name of the project
        template: Template to use (default: photo_basic)
        base_dir: Base directory for the project
        date_prefix: Whether to add date prefix to project folder
    """
    try:
        base_path = Path(base_dir).resolve()
        templates_file = base_path / "project_templates.json"
        
        # Load templates
        templates = load_templates(templates_file)
        
        if template not in templates:
            console.print(f"[red]Template '{template}' not found. Available templates:[/red]")
            for name, info in templates.items():
                console.print(f"[green]{name}[/green]: {info['description']}")
            return

        # Create project folder name
        if date_prefix:
            date_str = datetime.now().strftime("%Y%m%d")
            project_folder = f"{date_str}_{project_name}"
        else:
            project_folder = project_name

        project_path = base_path / project_folder

        # Confirm if folder exists
        if project_path.exists():
            if not Confirm.ask(f"Project folder '{project_folder}' already exists. Overwrite?"):
                return

        # Create project structure
        console.print(f"[blue]Creating project structure for: {project_folder}[/blue]")
        project_path.mkdir(exist_ok=True)
        create_structure(project_path, templates[template]["structure"])

        # Create a project info file
        info = {
            "project_name": project_name,
            "created_date": datetime.now().isoformat(),
            "template_used": template
        }
        
        with open(project_path / "project_info.json", 'w') as f:
            json.dump(info, f, indent=4)

        console.print(f"[green]Project structure created successfully at: {project_path}[/green]")
        logger.info(f"Created project structure: {project_path}")

        # Show tree structure
        console.print("\n[yellow]Project Structure:[/yellow]")
        for item in project_path.rglob("*"):
            if item.is_dir():
                depth = len(item.relative_to(project_path).parts)
                console.print("  " * depth + f"📁 {item.name}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        console.print(f"[red]An error occurred: {str(e)}[/red]")

def add_template(
    name: str = typer.Argument(..., help="Name for the new template"),
    template_file: str = typer.Argument(..., help="JSON file containing the template structure"),
) -> None:
    """Add a new project template from a JSON file."""
    try:
        template_path = Path(template_file)
        if not template_path.exists():
            console.print(f"[red]Template file not found: {template_file}[/red]")
            return

        with open(template_path) as f:
            structure = json.load(f)

        templates_file = Path("project_templates.json")
        save_template(templates_file, name, structure)
        console.print(f"[green]Template '{name}' added successfully[/green]")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        console.print(f"[red]An error occurred: {str(e)}[/red]")

app = typer.Typer()
app.command()(generate_project)
app.command()(add_template)

if __name__ == "__main__":
    app() 