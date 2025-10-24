"""Graphical User Interface for ENHANCER."""

import tkinter as tk
import traceback
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Optional

from ENHANCER import __version__
from ENHANCER.ai_interface import generate_suggestions_with_ai
from ENHANCER.code_analyzer import analyze_directory, analyze_file
from ENHANCER.config import GUI_LOG_FILE
from ENHANCER.models import get_all_models
from ENHANCER.utils import setup_logging

logger = setup_logging(__name__, log_file=GUI_LOG_FILE)


class EnhancerGUI:
    """Main GUI application class."""

    def __init__(self, root: tk.Tk):
        """Initialize the GUI."""
        self.root = root
        self.root.title(f"ENHANCER - Code Analysis Tool v{__version__}")
        self.root.geometry("1200x800")

        # Data
        self.current_file: Optional[Path] = None
        self.current_code: str = ""
        self.analysis_results: Optional[object] = None  # AnalysisResult type

        # Setup UI
        self.setup_menu()
        self.setup_ui()

        logger.info("GUI initialized")

    def setup_menu(self) -> None:
        """Setup menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Open Directory", command=self.open_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_ui(self) -> None:
        """Setup main UI components."""
        # Top frame - controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        # File path display
        ttk.Label(control_frame, text="File:").pack(side=tk.LEFT, padx=5)
        self.file_label = ttk.Label(control_frame, text="No file selected", foreground="gray")
        self.file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Model selection
        ttk.Label(control_frame, text="Model:").pack(side=tk.LEFT, padx=5)
        self.model_var = tk.StringVar()
        models = get_all_models()
        self.model_combo = ttk.Combobox(
            control_frame,
            textvariable=self.model_var,
            values=models,
            width=30,
            state="readonly"
        )
        if models:
            self.model_combo.current(0)
        self.model_combo.pack(side=tk.LEFT, padx=5)

        # Buttons frame
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)

        ttk.Button(
            button_frame,
            text="Open File",
            command=self.open_file
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Analyze",
            command=self.run_analysis
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Generate Suggestions",
            command=self.generate_suggestions
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_results
        ).pack(side=tk.LEFT, padx=5)

        # Notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Code view
        self.code_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.code_frame, text="Code")
        self.code_text = scrolledtext.ScrolledText(
            self.code_frame,
            wrap=tk.NONE,
            font=("Courier", 10)
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)

        # Tab 2: Analysis Results
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="Analysis")
        self.analysis_text = scrolledtext.ScrolledText(
            self.analysis_frame,
            wrap=tk.WORD,
            font=("Courier", 10)
        )
        self.analysis_text.pack(fill=tk.BOTH, expand=True)

        # Tab 3: Issues
        self.issues_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.issues_frame, text="Issues")
        self.issues_text = scrolledtext.ScrolledText(
            self.issues_frame,
            wrap=tk.WORD,
            font=("Courier", 10)
        )
        self.issues_text.pack(fill=tk.BOTH, expand=True)

        # Tab 4: Suggestions
        self.suggestions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.suggestions_frame, text="Suggestions")
        self.suggestions_text = scrolledtext.ScrolledText(
            self.suggestions_frame,
            wrap=tk.WORD,
            font=("Courier", 10)
        )
        self.suggestions_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def open_file(self) -> None:
        """Open a Python file."""
        filename = filedialog.askopenfilename(
            title="Select Python File",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )

        if filename:
            try:
                self.current_file = Path(filename)
                with open(filename, encoding="utf-8") as f:
                    self.current_code = f.read()

                self.file_label.config(text=filename, foreground="black")
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(1.0, self.current_code)
                self.status_bar.config(text=f"Loaded: {filename}")
                logger.info(f"Opened file: {filename}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")
                logger.error(f"Error opening file: {e}")

    def open_directory(self) -> None:
        """Open a directory for batch analysis."""
        directory = filedialog.askdirectory(title="Select Directory")

        if directory:
            try:
                self.status_bar.config(text="Analyzing directory...")
                self.root.update()

                dir_path = Path(directory)
                results = analyze_directory(dir_path, recursive=True)

                if results:
                    self.display_directory_results(results)
                    self.status_bar.config(
                        text=f"Analyzed {len(results)} files in {directory}"
                    )
                else:
                    messagebox.showinfo("Info", "No Python files found in directory")
                    self.status_bar.config(text="Ready")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to analyze directory:\n{e}")
                logger.error(f"Error analyzing directory: {e}")
                self.status_bar.config(text="Error")

    def run_analysis(self) -> None:
        """Run analysis on current file."""
        if not self.current_file:
            messagebox.showwarning("Warning", "Please open a file first")
            return

        try:
            self.status_bar.config(text="Analyzing...")
            self.root.update()

            # Static analysis
            result = analyze_file(self.current_file, auto_analyze=True)

            if result:
                self.analysis_results = result
                self.display_analysis_results(result)
                self.status_bar.config(text="Analysis complete")
            else:
                messagebox.showerror("Error", "Analysis failed")
                self.status_bar.config(text="Error")

        except Exception as e:
            error_msg = f"Error during analysis:\n{e}\n\n{traceback.format_exc()}"
            messagebox.showerror("Error", error_msg)
            logger.error(error_msg)
            self.status_bar.config(text="Error")

    def generate_suggestions(self) -> None:
        """Generate AI-powered suggestions."""
        if not self.current_file or not self.current_code:
            messagebox.showwarning("Warning", "Please open a file first")
            return

        try:
            self.status_bar.config(text="Generating suggestions...")
            self.root.update()

            model = self.model_var.get()
            if not model:
                messagebox.showwarning("Warning", "Please select a model")
                return

            # Get issues first
            if self.analysis_results:
                issues = self.analysis_results.issues
            else:
                result = analyze_file(self.current_file, auto_analyze=True)
                issues = result.issues if result else []

            # Generate suggestions
            suggestions = generate_suggestions_with_ai(
                self.current_code,
                issues,
                model=model
            )

            if suggestions:
                self.display_suggestions(suggestions)
                self.status_bar.config(text="Suggestions generated")
            else:
                messagebox.showinfo("Info", "No suggestions generated")
                self.status_bar.config(text="Ready")

        except Exception as e:
            error_msg = f"Error generating suggestions:\n{e}"
            messagebox.showerror("Error", error_msg)
            logger.error(error_msg)
            self.status_bar.config(text="Error")

    def display_analysis_results(self, result) -> None:
        """Display analysis results in tabs."""
        # Analysis tab
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "File Metrics:\n")
        self.analysis_text.insert(tk.END, "=" * 60 + "\n")
        for key, value in result.metrics.items():
            self.analysis_text.insert(tk.END, f"{key}: {value}\n")

        # Issues tab
        self.issues_text.delete(1.0, tk.END)
        if result.issues:
            self.issues_text.insert(tk.END, f"Found {len(result.issues)} issues:\n\n")
            for i, issue in enumerate(result.issues, 1):
                self.issues_text.insert(tk.END, f"{i}. {issue['type'].upper()}\n")
                self.issues_text.insert(tk.END, f"   Message: {issue['message']}\n")
                self.issues_text.insert(tk.END, f"   Line: {issue.get('line', 'N/A')}\n")
                self.issues_text.insert(tk.END, f"   Severity: {issue.get('severity', 'N/A')}\n\n")
        else:
            self.issues_text.insert(tk.END, "No issues found.")

        # Basic suggestions tab
        self.suggestions_text.delete(1.0, tk.END)
        if result.suggestions:
            self.suggestions_text.insert(tk.END, "Suggestions:\n\n")
            for i, suggestion in enumerate(result.suggestions, 1):
                self.suggestions_text.insert(tk.END, f"{i}. {suggestion}\n\n")
        else:
            self.suggestions_text.insert(tk.END, "No suggestions. Click 'Generate Suggestions' for AI-powered suggestions.")

        self.notebook.select(1)  # Switch to analysis tab

    def display_suggestions(self, suggestions) -> None:
        """Display suggestions in suggestions tab."""
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(tk.END, "AI-Generated Suggestions:\n")
        self.suggestions_text.insert(tk.END, "=" * 60 + "\n\n")

        for i, suggestion in enumerate(suggestions, 1):
            self.suggestions_text.insert(tk.END, f"{i}. {suggestion}\n\n")

        self.notebook.select(3)  # Switch to suggestions tab

    def display_directory_results(self, results) -> None:
        """Display directory analysis results."""
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "Directory Analysis Results:\n")
        self.analysis_text.insert(tk.END, "=" * 60 + "\n\n")

        total_issues = sum(len(r.issues) for r in results)
        self.analysis_text.insert(tk.END, f"Files analyzed: {len(results)}\n")
        self.analysis_text.insert(tk.END, f"Total issues: {total_issues}\n\n")

        for result in results:
            self.analysis_text.insert(tk.END, f"\nFile: {result.file_path}\n")
            self.analysis_text.insert(tk.END, f"Issues: {len(result.issues)}\n")

            if result.issues:
                for issue in result.issues[:3]:  # Show first 3 issues
                    self.analysis_text.insert(
                        tk.END,
                        f"  - {issue['type']}: {issue['message']}\n"
                    )

        self.notebook.select(1)  # Switch to analysis tab

    def export_report(self) -> None:
        """Export analysis report to file."""
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No analysis results to export")
            return

        filename = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("ENHANCER Analysis Report\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"File: {self.analysis_results.file_path}\n\n")
                    f.write("Metrics:\n")
                    for key, value in self.analysis_results.metrics.items():
                        f.write(f"  {key}: {value}\n")
                    f.write("\nIssues:\n")
                    for issue in self.analysis_results.issues:
                        f.write(f"  - {issue}\n")
                    f.write("\nSuggestions:\n")
                    for suggestion in self.analysis_results.suggestions:
                        f.write(f"  - {suggestion}\n")

                messagebox.showinfo("Success", f"Report saved to {filename}")
                logger.info(f"Report exported to {filename}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report:\n{e}")
                logger.error(f"Error saving report: {e}")

    def clear_results(self) -> None:
        """Clear all results."""
        self.analysis_text.delete(1.0, tk.END)
        self.issues_text.delete(1.0, tk.END)
        self.suggestions_text.delete(1.0, tk.END)
        self.status_bar.config(text="Cleared")

    def show_about(self) -> None:
        """Show about dialog."""
        about_text = f"""ENHANCER - Advanced Code Analysis & Enhancement Tool
Version: {__version__}

A comprehensive Python-based tool that leverages
multiple AI models to analyze code for potential
improvements, issues, and best practices.

Author: Roo
License: MIT
"""
        messagebox.showinfo("About ENHANCER", about_text)


def main() -> None:
    """Main entry point for GUI."""
    try:
        root = tk.Tk()
        EnhancerGUI(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"GUI error: {e}\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
