"""Queue management module for handling file processing queue."""

from queue import Queue
from threading import Lock


class QueueManager:
    """
    Manages the processing queue with thread-safe operations.

    Handles the queuing, processing, and status tracking of files
    in the enhancement pipeline.
    """

    def __init__(self):
        """Initialize the queue manager with empty queue and status tracking."""
        self.queue = Queue()
        self.current_file = None
        self.processed_files = []
        self.lock = Lock()

    def add_file(self, file_path):
        """
        Add a file to the queue if not already processed.

        Args:
            file_path (str): Path of the file to add to the queue.

        Returns:
            bool: True if file was added, False if already processed.
        """
        with self.lock:
            if file_path not in self.processed_files:
                self.queue.put(file_path)
                return True
        return False

    def get_next_file(self):
        """
        Get the next file from the queue.

        Returns:
            str: Path of the next file to process, or None if queue is empty.
        """
        with self.lock:
            if not self.queue.empty():
                self.current_file = self.queue.get()
                return self.current_file
        return None

    def mark_complete(self, file_path):
        """
        Mark a file as processed.

        Args:
            file_path (str): Path of the file to mark as complete.
        """
        with self.lock:
            self.processed_files.append(file_path)
            self.current_file = None

    def get_status(self):
        """
        Get the current queue status.

        Returns:
            dict: Dictionary containing pending, current, and completed files.
        """
        with self.lock:
            return {
                "pending": list(self.queue.queue),
                "current": self.current_file,
                "completed": self.processed_files,
            }
