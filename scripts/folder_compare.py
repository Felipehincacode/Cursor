#!/usr/bin/env python3
"""
Folder Comparison Tool

Compare two folders and identify missing or unmatched files between them.
Useful for checking if all files were properly copied or processed.
"""

import os
from pathlib import Path
from typing import Set, Dict, Tuple
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from loguru import logger
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# Configure logger
logger.add("folder_compare.log", rotation="1 MB")

# Initialize Rich console
console = Console()

def calculate_file_hash(file_path: Path, chunk_size: int = 8192) -> str:
    """Calculate a quick hash of the first and last chunks of a file."""
    import hashlib
    
    if not file_path.is_file():
        return ""
    
    md5 = hashlib.md5()
    file_size = file_path.stat().st_size
    
    with open(file_path, 'rb') as f:
        # Read first chunk
        data = f.read(chunk_size)
        md5.update(data)
        
        # If file is larger than chunk_size, read last chunk
        if file_size > chunk_size:
            f.seek(-chunk_size, 2)
            data = f.read(chunk_size)
            md5.update(data)
    
    return md5.hexdigest()

def get_files_info(directory: Path) -> Dict[str, Tuple[int, str]]:
    """Get information about files in a directory."""
    files_info = {}
    
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(directory))
            size = file_path.stat().st_size
            quick_hash = calculate_file_hash(file_path)
            files_info[rel_path] = (size, quick_hash)
    
    return files_info

def compare_folders(
    source_dir: str = typer.Argument(..., help="Source directory path"),
    target_dir: str = typer.Argument(..., help="Target directory path"),
    check_content: bool = typer.Option(False, "--check-content", "-c", help="Compare file contents, not just names"),
) -> None:
    """
    Compare two folders and show differences in files.
    
    Args:
        source_dir: Path to the source directory
        target_dir: Path to the target directory
        check_content: If True, compare file contents (size and hash) not just names
    """
    try:
        source_path = Path(source_dir).resolve()
        target_path = Path(target_dir).resolve()

        if not source_path.exists() or not target_path.exists():
            console.print("[red]Error: One or both directories do not exist[/red]")
            return

        logger.info(f"Comparing folders:\nSource: {source_path}\nTarget: {target_path}")
        console.print(f"[blue]Scanning directories...[/blue]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
        ) as progress:
            
            task1 = progress.add_task("Scanning source directory...", total=None)
            source_files = get_files_info(source_path)
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("Scanning target directory...", total=None)
            target_files = get_files_info(target_path)
            progress.update(task2, completed=True)

        # Create sets of filenames
        source_filenames = set(source_files.keys())
        target_filenames = set(target_files.keys())

        # Find missing and extra files
        missing_files = source_filenames - target_filenames
        extra_files = target_filenames - source_filenames
        common_files = source_filenames & target_filenames

        # Check for content mismatches if requested
        content_mismatches = set()
        if check_content:
            for filename in common_files:
                if source_files[filename] != target_files[filename]:
                    content_mismatches.add(filename)

        # Create and display results table
        table = Table(title="Folder Comparison Results")
        table.add_column("Category", style="cyan")
        table.add_column("Files", style="white")
        table.add_column("Count", justify="right", style="green")

        if missing_files:
            table.add_row(
                "Missing in Target",
                "\n".join(sorted(missing_files)),
                str(len(missing_files))
            )

        if extra_files:
            table.add_row(
                "Extra in Target",
                "\n".join(sorted(extra_files)),
                str(len(extra_files))
            )

        if check_content and content_mismatches:
            table.add_row(
                "Content Mismatches",
                "\n".join(sorted(content_mismatches)),
                str(len(content_mismatches))
            )

        if not (missing_files or extra_files or (check_content and content_mismatches)):
            table.add_row("Status", "Folders are identical!", "0")

        console.print(table)

        # Log results
        logger.info(f"Comparison completed. Missing: {len(missing_files)}, "
                   f"Extra: {len(extra_files)}, "
                   f"Content mismatches: {len(content_mismatches) if check_content else 'not checked'}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    typer.run(compare_folders) 