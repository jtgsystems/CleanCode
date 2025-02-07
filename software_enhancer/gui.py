"""GUI module for the Software Enhancement Pipeline."""

import tkinter as tk
from pathlib import Path

from .config import Config
from .enhancement_pipeline import EnhancementPipeline
from .file_processor import FileProcessor
from .queue_manager import QueueManager


class EnhancerGUI:
    """
    Graphical user interface for the Software Enhancement Pipeline.

    Provides a user-friendly interface for selecting files, monitoring
    the enhancement process, and viewing results.
    """

    def __init__(self):
        """Initialize the GUI components."""
        self.root = tk.Tk()
        self.root.title("Code Enhancement Pipeline")
        self.root.configure(bg="#f0f0f0")
        self.root.minsize(1000, 800)

        self.main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.queue_manager = QueueManager()
        self.pipeline = EnhancementPipeline()

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface components."""
        # Create model status indicators
        self.model_indicators = self.create_model_indicators()

        # Left panel for input and progress
        self.left_panel = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Input section
        self.setup_input_section()

        # Output section
        self.setup_output_section()

        # Right panel for queue status
        self.setup_queue_panel()

        # Process button
        self.setup_process_button()

    def create_model_indicators(self):
        """
        Create status indicators for each model.

        Returns:
            dict: Dictionary of model indicator labels.
        """
        frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        frame.pack(fill=tk.X, pady=(0, 10))

        indicators = {}
        for model_type in Config.MODELS:
            label = tk.Label(
                frame,
                text=f"● {model_type}",
                font=("Arial", 9),
                fg="#666666",
                bg="#f0f0f0",
                padx=5,
            )
            label.pack(side=tk.LEFT)
            indicators[model_type] = label

        return indicators

    def create_scrolled_text(self, parent, height=10, width=50, readonly=False):
        """
        Create a scrolled text widget.

        Args:
            parent: Parent widget
            height (int): Widget height in lines
            width (int): Widget width in characters
            readonly (bool): Whether the widget should be read-only

        Returns:
            tuple: Frame and text widget
        """
        frame = tk.Frame(parent)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            frame,
            height=height,
            width=width,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            font=("Arial", 10),
        )

        if readonly:
            text_widget.config(state=tk.DISABLED)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        return frame, text_widget

    def setup_input_section(self):
        """Set up the input section of the GUI."""
        input_label = tk.Label(
            self.left_panel,
            text="Enter project path:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
        )
        input_label.pack(anchor=tk.W)

        self.input_frame, self.input_text = self.create_scrolled_text(
            self.left_panel,
            height=2,
            width=60,
        )
        self.input_frame.pack(fill=tk.X, pady=(5, 15))

    def setup_output_section(self):
        """Set up the output section of the GUI."""
        output_label = tk.Label(
            self.left_panel,
            text="Enhancement Progress:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
        )
        output_label.pack(anchor=tk.W)

        self.output_frame, self.output_text = self.create_scrolled_text(
            self.left_panel,
            height=30,
            width=60,
            readonly=True,
        )
        self.output_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 15))

    def setup_queue_panel(self):
        """Set up the queue status panel."""
        right_panel = tk.Frame(self.main_frame, bg="#f0f0f0", padx=20)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)

        queue_label = tk.Label(
            right_panel,
            text="Processing Queue:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
        )
        queue_label.pack(anchor=tk.W)

        self.queue_frame, self.queue_text = self.create_scrolled_text(
            right_panel,
            height=30,
            width=40,
            readonly=True,
        )
        self.queue_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 15))

    def setup_process_button(self):
        """Set up the process button."""
        self.process_button = tk.Button(
            self.left_panel,
            text="Start Enhancement Pipeline",
            command=self.start_processing,
            font=("Arial", 11),
            bg="#4a90e2",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2",
        )
        self.process_button.pack(pady=10)

    def update_output(self, text):
        """
        Update the output text area.

        Args:
            text (str): Text to display in the output area.
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

    def update_queue_display(self):
        """Update the queue status display."""
        status = self.queue_manager.get_status()
        self.queue_text.config(state=tk.NORMAL)
        self.queue_text.delete(1.0, tk.END)

        self.queue_text.insert(tk.END, "=== Queue Status ===\n\n")

        if status["current"]:
            self.queue_text.insert(tk.END, "Currently Processing:\n")
            self.queue_text.insert(tk.END, f"- {status['current']}\n\n")

        if status["pending"]:
            self.queue_text.insert(tk.END, "Pending Files:\n")
            for file in status["pending"]:
                self.queue_text.insert(tk.END, f"- {file}\n")
            self.queue_text.insert(tk.END, "\n")

        if status["completed"]:
            self.queue_text.insert(tk.END, "Completed Files:\n")
            for file in status["completed"]:
                self.queue_text.insert(tk.END, f"- {file}\n")

        self.queue_text.config(state=tk.DISABLED)

    def set_active_model(self, model_type):
        """
        Set the active model indicator.

        Args:
            model_type (str): Type of model to set as active.
        """
        for label in self.model_indicators.values():
            label.config(fg="#666666")
        if model_type in self.model_indicators:
            self.model_indicators[model_type].config(fg="#4a90e2")

    def start_processing(self):
        """Start the enhancement pipeline processing."""
        project_path = self.input_text.get("1.0", tk.END).strip()
        if not project_path:
            self.update_output("Error: No project path entered.")
            return

        if not Path(project_path).exists():
            self.update_output("Error: Project path does not exist.")
            return

        # Find all text files
        text_files = FileProcessor.find_text_files(project_path)
        if not text_files:
            self.update_output("Error: No text files found in the directory.")
            return

        # Initialize queue
        for file_path in text_files:
            self.queue_manager.add_file(file_path)

        # Update initial queue display
        self.update_queue_display()

        while True:
            # Get next file to process
            current_file = self.queue_manager.get_next_file()
            if not current_file:
                break

            output = f"\nProcessing: {current_file}\n"
            output += Config.PROGRESS_MESSAGES["start"]
            self.update_output(output)
            self.update_queue_display()

            try:
                # Create backup
                FileProcessor.create_backup(current_file)
                output += f"Backup created: {current_file}.bak\n\n"

                # Process through enhancement pipeline
                for phase, msg in Config.PROGRESS_MESSAGES.items():
                    if phase.endswith("_done") or phase in ["start", "complete"]:
                        continue

                    model_type = phase.replace("ing", "")
                    self.set_active_model(model_type)
                    output += msg
                    self.update_output(output)

                # Enhance the file
                improved_code = self.pipeline.enhance_file(current_file)

                if improved_code:
                    FileProcessor.write_file(current_file, improved_code)
                    output += f"File successfully enhanced: {current_file}\n"
                    self.queue_manager.mark_complete(current_file)
                else:
                    output += "Error: Enhancement pipeline failed.\n"
                    self.update_output(output)
                    continue

                output += Config.PROGRESS_MESSAGES["complete"]
                self.update_output(output)
                self.update_queue_display()

            except Exception as e:
                output += f"Error processing file: {e}\n"
                self.update_output(output)
                continue

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()
