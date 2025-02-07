"""File processing module for handling file operations."""

import os
import shutil


class FileProcessor:
    """Handles file operations like finding, reading, writing, and backup."""

    @staticmethod
    def find_text_files(directory):
        """
        Find all text files in the directory.

        Args:
            directory (str): Directory path to search for text files.

        Returns:
            list: List of text file paths found in the directory.
        """
        text_files = []

        for root, _, files in os.walk(directory):
            for file in files:
                # Skip backup files and hidden files
                if not file.endswith(".bak") and not file.startswith("."):
                    file_path = os.path.join(root, file)
                    try:
                        # Try to read the file to ensure it's a text file
                        with open(file_path, "r", encoding="utf-8") as f:
                            f.read(1024)  # Read first 1KB to check if readable
                        text_files.append(file_path)
                    except (UnicodeDecodeError, IOError):
                        # Skip binary files or files that can't be read as text
                        continue

        return text_files

    @staticmethod
    def create_backup(file_path):
        """
        Create a backup of the file.

        Args:
            file_path (str): Path of the file to backup.

        Returns:
            str: Path of the created backup file.
        """
        backup_path = file_path + ".bak"
        shutil.copy2(file_path, backup_path)
        return backup_path

    @staticmethod
    def read_file(file_path):
        """
        Read the contents of a file.

        Args:
            file_path (str): Path of the file to read.

        Returns:
            str: Contents of the file.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        """
        Write content to a file.

        Args:
            file_path (str): Path of the file to write to.
            content (str): Content to write to the file.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
