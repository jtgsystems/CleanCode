import os
import shutil
import tkinter as tk
from pathlib import Path
from queue import Queue
from threading import Lock

import ollama


# Configuration Component
class Config:
    MODELS = {
        # Project structure analysis
        "analysis": "llama3.2:latest",
        # Improvement suggestions
        "generation": "olmo2:13b",
        # Code review
        "vetting": "deepseek-r1",
        # Implementation planning
        "finalization": "deepseek-r1:14b",
        # Advanced optimization
        "enhancement": "phi4:latest",
        # Final project review
        "comprehensive": "phi4:latest",
        # Final report generation
        "presenter": "deepseek-r1:14b",
    }

    PROGRESS_MESSAGES = {
        "start": "Starting code enhancement pipeline...\n",
        "analyzing": (
            "Phase 1/7: Code Analysis - " "Understanding structure and patterns\n"
        ),
        "analysis_done": "Initial analysis complete.\n\n",
        "generating": (
            "Phase 2/7: Generating Improvements - "
            "Identifying optimization opportunities\n"
        ),
        "generation_done": "Improvement suggestions generated.\n\n",
        "vetting": ("Phase 3/7: Code Review - " "Validating proposed changes\n"),
        "vetting_done": "Code review complete.\n\n",
        "finalizing": (
            "Phase 4/7: Implementation - " "Applying validated improvements\n"
        ),
        "finalize_done": "Implementation complete.\n\n",
        "enhancing": ("Phase 5/7: Advanced Optimization - " "Fine-tuning the code\n"),
        "enhance_done": "Optimization complete.\n\n",
        "comprehensive": ("Phase 6/7: Final Review - " "Ensuring code perfection\n"),
        "comprehensive_done": "Final review complete.\n\n",
        "presenting": ("Phase 7/7: Final Polish - " "Applying finishing touches\n"),
        "complete": ("Enhancement pipeline complete. " "Code is now optimized.\n\n"),
    }


# File Processing Component
class FileProcessor:
    @staticmethod
    def find_text_files(directory):
        """Find all text files in the directory."""
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
        """Create a backup of the file."""
        backup_path = file_path + ".bak"
        shutil.copy2(file_path, backup_path)
        return backup_path

    @staticmethod
    def read_file(file_path):
        """Read the contents of a file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        """Write content to a file."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


# Queue Management Component
class QueueManager:
    def __init__(self):
        self.queue = Queue()
        self.current_file = None
        self.processed_files = []
        self.lock = Lock()

    def add_file(self, file_path):
        """Add a file to the queue."""
        with self.lock:
            if file_path not in self.processed_files:
                self.queue.put(file_path)
                return True
        return False

    def get_next_file(self):
        """Get the next file from the queue."""
        with self.lock:
            if not self.queue.empty():
                self.current_file = self.queue.get()
                return self.current_file
        return None

    def mark_complete(self, file_path):
        """Mark a file as processed."""
        with self.lock:
            self.processed_files.append(file_path)
            self.current_file = None

    def get_status(self):
        """Get the current queue status."""
        with self.lock:
            return {
                "pending": list(self.queue.queue),
                "current": self.current_file,
                "completed": self.processed_files,
            }


# Enhancement Pipeline Component
class EnhancementPipeline:
    def __init__(self):
        self.models = Config.MODELS

    def enhance_phase(self, code, model_name, phase_prompt):
        """Enhances code using a specific model and phase-specific prompt."""
        try:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{phase_prompt}\n\n"
                        "Current code:\n```\n"
                        f"{code}\n"
                        "```\n\n"
                        "Return ONLY the improved code without any explanations "
                        "or markdown."
                    ),
                }
            ]
            response = ollama.chat(model=model_name, messages=messages)
            improved_code = response["message"]["content"]

            # Clean up the response
            improved_code = improved_code.strip()
            if improved_code.startswith("```"):
                improved_code = improved_code.split("```")[1]
            if improved_code.startswith("python"):
                improved_code = improved_code[6:]
            improved_code = improved_code.strip()

            return improved_code
        except Exception as e:
            print(f"Error during code enhancement phase: {e}")
            return None

    def enhance_file(self, file_path):
        """Enhances a file through multiple phases of improvement."""
        try:
            current_code = FileProcessor.read_file(file_path)

            # Phase 1: Analysis and Structure
            analysis_prompt = """
            Analyze and improve this code focusing on:
            1. Code structure and organization
            2. Function decomposition
            3. Variable naming
            4. Code flow
            5. Documentation
            Make structural improvements while preserving functionality.
            """
            current_code = self.enhance_phase(
                current_code, self.models["analysis"], analysis_prompt
            )
            if not current_code:
                return None

            # Phase 2: Optimizations
            optimization_prompt = """
            Optimize this code focusing on:
            1. Algorithm efficiency
            2. Memory usage
            3. Time complexity
            4. Resource utilization
            5. Performance bottlenecks
            Implement optimizations while maintaining readability.
            """
            current_code = self.enhance_phase(
                current_code, self.models["generation"], optimization_prompt
            )
            if not current_code:
                return None

            # Phase 3: Best Practices
            review_prompt = """
            Review and improve this code focusing on:
            1. Best practices
            2. Design patterns
            3. SOLID principles
            4. DRY principle
            5. Code maintainability
            Apply industry standard practices while ensuring code quality.
            """
            current_code = self.enhance_phase(
                current_code, self.models["vetting"], review_prompt
            )
            if not current_code:
                return None

            # Phase 4: Error Handling
            implementation_prompt = """
            Enhance implementation focusing on:
            1. Error handling
            2. Edge cases
            3. Input validation
            4. Exception handling
            5. Defensive programming
            Implement robust error handling while maintaining code clarity.
            """
            current_code = self.enhance_phase(
                current_code, self.models["finalization"], implementation_prompt
            )
            if not current_code:
                return None

            # Phase 5: Advanced Optimization
            advanced_prompt = """
            Perform advanced optimization focusing on:
            1. Code elegance
            2. Functional programming concepts
            3. Modern language features
            4. Clean code principles
            5. Advanced patterns
            Apply sophisticated improvements while ensuring maintainability.
            """
            current_code = self.enhance_phase(
                current_code, self.models["enhancement"], advanced_prompt
            )
            if not current_code:
                return None

            # Phase 6: Comprehensive Review
            final_prompt = """
            Perform final review focusing on:
            1. Overall code quality
            2. Consistency
            3. Documentation completeness
            4. API design
            5. Future maintainability
            Ensure the code is perfect and production-ready.
            """
            current_code = self.enhance_phase(
                current_code, self.models["comprehensive"], final_prompt
            )
            if not current_code:
                return None

            # Phase 7: Final Polish
            polish_prompt = """
            Apply final polish focusing on:
            1. Code formatting
            2. Documentation style
            3. Comment clarity
            4. Naming consistency
            5. Overall aesthetics
            Ensure the code is pristine and professional and error free.
            """
            current_code = self.enhance_phase(
                current_code, self.models["presenter"], polish_prompt
            )
            if not current_code:
                return None

            return current_code
        except Exception as e:
            print(f"Error during code enhancement: {e}")
            return None


# GUI Component
class EnhancerGUI:
    def __init__(self):
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
        """Set up the user interface."""
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
        """Creates model status indicators."""
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
        """Create a scrolled text widget."""
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
        """Set up the input section."""
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
        """Set up the output section."""
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
        """Update the output text area."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

    def update_queue_display(self):
        """Update the queue display."""
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
        """Set the active model indicator."""
        for label in self.model_indicators.values():
            label.config(fg="#666666")
        if model_type in self.model_indicators:
            self.model_indicators[model_type].config(fg="#4a90e2")

    def start_processing(self):
        """Start the enhancement pipeline."""
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

                    self.set_active_model(phase.replace("ing", ""))
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
        """Start the GUI."""
        self.root.mainloop()


def main():
    """Main function."""
    app = EnhancerGUI()
    app.run()


if __name__ == "__main__":
    main()
