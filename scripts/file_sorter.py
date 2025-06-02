#!/usr/bin/env python3
"""
Media File Sorter

This script organizes media files into categorized subfolders based on their extensions.
It provides a rich console interface with progress bars and logging capabilities.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Set
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich import print as rprint
from loguru import logger
import typer

# Configure logger
logger.add("file_sorter.log", rotation="1 MB")

# Initialize Rich console
console = Console()

# File extension categories
EXTENSION_CATEGORIES: Dict[str, Set[str]] = {
    "RAW": {".arw", ".cr2", ".cr3", ".nef", ".dng", ".raw"},
    "JPEG": {".jpg", ".jpeg", ".jpe"},
    "PNG": {".png"},
    "VIDEO": {".mp4", ".mov", ".avi", ".mkv"},
    "AUDIO": {".wav", ".mp3", ".aac"},
    "EDITED": {".psd", ".xmp", ".ai"},
}

def create_category_folders(base_path: Path) -> Dict[str, Path]:
    """Create category folders if they don't exist."""
    category_paths = {}
    for category in EXTENSION_CATEGORIES.keys():
        category_path = base_path / category
        category_path.mkdir(exist_ok=True)
        category_paths[category] = category_path
    return category_paths

def get_file_category(file_path: Path) -> str:
    """Determine the category of a file based on its extension."""
    ext = file_path.suffix.lower()
    for category, extensions in EXTENSION_CATEGORIES.items():
        if ext in extensions:
            return category
    return "MISC"

def sort_files(
    source_dir: str = typer.Argument(..., help="Source directory containing media files"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Preview changes without moving files"),
) -> None:
    """
    Sort media files into categorized subfolders.
    
    Args:
        source_dir: Directory containing files to sort
        dry_run: If True, only preview changes without moving files
    """
    try:
        source_path = Path(source_dir).resolve()
        if not source_path.exists():
            console.print(f"[red]Error: Source directory '{source_dir}' does not exist[/red]")
            return

        logger.info(f"Starting file sort in: {source_path}")
        console.print(f"[blue]Scanning directory: {source_path}[/blue]")

        # Create category folders
        category_paths = create_category_folders(source_path)
        
        # Get list of files to process
        files_to_process = [f for f in source_path.iterdir() if f.is_file()]
        
        if not files_to_process:
            console.print("[yellow]No files found to process[/yellow]")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            
            task = progress.add_task("Sorting files...", total=len(files_to_process))
            
            for file_path in files_to_process:
                category = get_file_category(file_path)
                dest_dir = category_paths.get(category, source_path / "MISC")
                dest_path = dest_dir / file_path.name

                if dry_run:
                    console.print(f"Would move: {file_path.name} -> {dest_path}")
                else:
                    try:
                        if not dest_dir.exists():
                            dest_dir.mkdir(parents=True)
                        if file_path != dest_path:
                            shutil.move(str(file_path), str(dest_path))
                            logger.info(f"Moved: {file_path.name} -> {dest_path}")
                    except Exception as e:
                        logger.error(f"Error moving {file_path}: {str(e)}")
                        console.print(f"[red]Error moving {file_path.name}: {str(e)}[/red]")

                progress.update(task, advance=1)

        console.print("[green]File sorting complete![/green]")
        logger.info("File sorting operation completed")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    typer.run(sort_files) 