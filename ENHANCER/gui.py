"""
Graphical User Interface for ENHANCER

Tkinter-based GUI with tabbed interface for code analysis.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import threading
import json

from ENHANCER.core import (
    perform_comprehensive_analysis,
    save_analysis_report,
    export_critical_issues,
)
from ENHANCER.code_analyzer import analyze_directory
from ENHANCER.models import get_available_models

# Configure GUI logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ENHANCER/logs/enhancer_gui.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class EnhancerGUI:
    """Main GUI application for ENHANCER."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ENHANCER - Advanced Code Analysis & Enhancement Tool")
        self.root.geometry("1200x800")

        # Analysis state
        self.current_file: Optional[Path] = None
        self.current_directory: Optional[Path] = None
        self.analysis_results: Optional[Dict[str, Any]] = None
        self.analyzing: bool = False

        # Create main UI
        self._create_widgets()
        self._load_models()

        logger.info("ENHANCER GUI initialized")

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Top control panel
        self._create_control_panel(main_frame)

        # Tabbed interface
        self._create_tabs(main_frame)

        # Status bar
        self._create_status_bar(main_frame)

    def _create_control_panel(self, parent: ttk.Frame) -> None:
        """Create the top control panel."""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # File selection
        ttk.Label(control_frame, text="File/Directory:").grid(row=0, column=0, sticky=tk.W)
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(control_frame, textvariable=self.path_var, width=60)
        path_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))

        ttk.Button(control_frame, text="Browse File", command=self._browse_file).grid(
            row=0, column=2, padx=2
        )
        ttk.Button(control_frame, text="Browse Directory", command=self._browse_directory).grid(
            row=0, column=3, padx=2
        )

        # Model selection
        ttk.Label(control_frame, text="AI Model:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.model_var,
            state="readonly",
            width=40
        )
        self.model_dropdown.grid(row=1, column=1, padx=5, pady=(10, 0), sticky=(tk.W, tk.E))

        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=1, column=2, columnspan=2, pady=(10, 0))

        ttk.Button(button_frame, text="Analyze", command=self._start_analysis).grid(
            row=0, column=0, padx=2
        )
        ttk.Button(button_frame, text="Export Report", command=self._export_report).grid(
            row=0, column=1, padx=2
        )
        ttk.Button(button_frame, text="Export Critical", command=self._export_critical).grid(
            row=0, column=2, padx=2
        )

        control_frame.columnconfigure(1, weight=1)

    def _create_tabs(self, parent: ttk.Frame) -> None:
        """Create the tabbed interface."""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Files tab
        self.files_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.files_tab, text="Files")
        self._create_files_tab()

        # Analysis tab
        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="Analysis")
        self._create_analysis_tab()

        # Issues tab
        self.issues_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.issues_tab, text="Issues")
        self._create_issues_tab()

        # Suggestions tab
        self.suggestions_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.suggestions_tab, text="Suggestions")
        self._create_suggestions_tab()

        # Enhanced Code tab
        self.enhanced_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.enhanced_tab, text="Enhanced Code")
        self._create_enhanced_tab()

    def _create_files_tab(self) -> None:
        """Create the Files tab."""
        self.files_text = scrolledtext.ScrolledText(
            self.files_tab,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Courier", 10)
        )
        self.files_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.files_text.insert("1.0", "Browse and select Python files or directories to analyze.\n\n")
        self.files_text.insert(tk.END, "Supported operations:\n")
        self.files_text.insert(tk.END, "  - Single file analysis\n")
        self.files_text.insert(tk.END, "  - Directory analysis (recursive)\n")
        self.files_text.insert(tk.END, "  - Batch processing\n\n")
        self.files_text.insert(tk.END, "File will be displayed here after selection.")
        self.files_text.config(state=tk.DISABLED)

    def _create_analysis_tab(self) -> None:
        """Create the Analysis tab."""
        self.analysis_text = scrolledtext.ScrolledText(
            self.analysis_tab,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Courier", 10)
        )
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.analysis_text.insert("1.0", "Comprehensive code analysis results will appear here.\n\n")
        self.analysis_text.insert(tk.END, "Analysis includes:\n")
        self.analysis_text.insert(tk.END, "  - Code quality assessment\n")
        self.analysis_text.insert(tk.END, "  - Security vulnerabilities\n")
        self.analysis_text.insert(tk.END, "  - Performance considerations\n")
        self.analysis_text.insert(tk.END, "  - Best practices adherence\n")
        self.analysis_text.config(state=tk.DISABLED)

    def _create_issues_tab(self) -> None:
        """Create the Issues tab."""
        self.issues_text = scrolledtext.ScrolledText(
            self.issues_tab,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Courier", 10)
        )
        self.issues_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.issues_text.insert("1.0", "Detected issues organized by severity:\n\n")
        self.issues_text.insert(tk.END, "  [HIGH]    - Critical security and bug issues\n")
        self.issues_text.insert(tk.END, "  [MEDIUM]  - Quality and maintainability concerns\n")
        self.issues_text.insert(tk.END, "  [LOW]     - Style and minor improvements\n")
        self.issues_text.config(state=tk.DISABLED)

    def _create_suggestions_tab(self) -> None:
        """Create the Suggestions tab."""
        self.suggestions_text = scrolledtext.ScrolledText(
            self.suggestions_tab,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Courier", 10)
        )
        self.suggestions_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.suggestions_text.insert("1.0", "AI-generated improvement suggestions will appear here.\n\n")
        self.suggestions_text.insert(tk.END, "Suggestions include:\n")
        self.suggestions_text.insert(tk.END, "  - Code refactoring opportunities\n")
        self.suggestions_text.insert(tk.END, "  - Modern Python features to adopt\n")
        self.suggestions_text.insert(tk.END, "  - Performance optimizations\n")
        self.suggestions_text.insert(tk.END, "  - Readability improvements\n")
        self.suggestions_text.config(state=tk.DISABLED)

    def _create_enhanced_tab(self) -> None:
        """Create the Enhanced Code tab."""
        self.enhanced_text = scrolledtext.ScrolledText(
            self.enhanced_tab,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Courier", 10)
        )
        self.enhanced_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.enhanced_text.insert("1.0", "Enhanced code with applied improvements will appear here.\n\n")
        self.enhanced_text.insert(tk.END, "You can review and apply suggested enhancements.\n")
        self.enhanced_text.config(state=tk.DISABLED)

    def _create_status_bar(self, parent: ttk.Frame) -> None:
        """Create the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_label.pack(fill=tk.X)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            mode='indeterminate'
        )
        # Progress bar hidden by default

    def _load_models(self) -> None:
        """Load available AI models."""
        try:
            models = get_available_models()
            model_list = []

            for provider, provider_models in models.items():
                for model in provider_models:
                    model_list.append(f"{model} ({provider})")

            if model_list:
                self.model_dropdown['values'] = model_list
                self.model_dropdown.current(0)
                logger.info(f"Loaded {len(model_list)} models")
            else:
                self.model_dropdown['values'] = ["No models available"]
                logger.warning("No AI models available")

        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            self.model_dropdown['values'] = ["Error loading models"]

    def _browse_file(self) -> None:
        """Open file browser for selecting a Python file."""
        file_path = filedialog.askopenfilename(
            title="Select Python File",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if file_path:
            self.current_file = Path(file_path)
            self.current_directory = None
            self.path_var.set(file_path)
            self._display_file_content()
            logger.info(f"Selected file: {file_path}")

    def _browse_directory(self) -> None:
        """Open directory browser."""
        dir_path = filedialog.askdirectory(title="Select Directory")
        if dir_path:
            self.current_directory = Path(dir_path)
            self.current_file = None
            self.path_var.set(dir_path)
            self._display_directory_info()
            logger.info(f"Selected directory: {dir_path}")

    def _display_file_content(self) -> None:
        """Display selected file content in Files tab."""
        if not self.current_file:
            return

        try:
            content = self.current_file.read_text(encoding='utf-8')
            self.files_text.config(state=tk.NORMAL)
            self.files_text.delete("1.0", tk.END)
            self.files_text.insert("1.0", f"File: {self.current_file}\n")
            self.files_text.insert(tk.END, "=" * 80 + "\n\n")
            self.files_text.insert(tk.END, content)
            self.files_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            logger.error(f"Failed to read file: {e}")

    def _display_directory_info(self) -> None:
        """Display directory information in Files tab."""
        if not self.current_directory:
            return

        try:
            python_files = list(self.current_directory.rglob("*.py"))
            self.files_text.config(state=tk.NORMAL)
            self.files_text.delete("1.0", tk.END)
            self.files_text.insert("1.0", f"Directory: {self.current_directory}\n")
            self.files_text.insert(tk.END, "=" * 80 + "\n\n")
            self.files_text.insert(tk.END, f"Found {len(python_files)} Python files:\n\n")
            for py_file in python_files[:100]:  # Limit to first 100
                self.files_text.insert(tk.END, f"  {py_file}\n")
            if len(python_files) > 100:
                self.files_text.insert(tk.END, f"\n... and {len(python_files) - 100} more files")
            self.files_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read directory: {e}")
            logger.error(f"Failed to read directory: {e}")

    def _start_analysis(self) -> None:
        """Start code analysis in a background thread."""
        if self.analyzing:
            messagebox.showwarning("Analysis in Progress", "An analysis is already running.")
            return

        if not self.current_file and not self.current_directory:
            messagebox.showwarning("No Selection", "Please select a file or directory first.")
            return

        # Extract model name from dropdown selection
        selected = self.model_var.get()
        if "(" in selected:
            model = selected.split("(")[0].strip()
        else:
            model = None

        self.analyzing = True
        self.status_var.set("Analyzing...")
        self.progress_bar.pack(fill=tk.X, pady=2)
        self.progress_bar.start()

        # Run analysis in background thread
        thread = threading.Thread(
            target=self._run_analysis,
            args=(model,),
            daemon=True
        )
        thread.start()

    def _run_analysis(self, model: Optional[str]) -> None:
        """Run analysis (called in background thread)."""
        try:
            if self.current_file:
                results = perform_comprehensive_analysis(self.current_file, model=model)
            else:
                results = analyze_directory(self.current_directory, model=model)

            self.analysis_results = results

            # Update UI in main thread
            self.root.after(0, self._display_analysis_results)
            self.root.after(0, lambda: self.status_var.set("Analysis complete"))

        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            self.root.after(0, lambda: messagebox.showerror("Analysis Error", str(e)))
            self.root.after(0, lambda: self.status_var.set("Analysis failed"))

        finally:
            self.analyzing = False
            self.root.after(0, self.progress_bar.stop)
            self.root.after(0, self.progress_bar.pack_forget)

    def _display_analysis_results(self) -> None:
        """Display analysis results in appropriate tabs."""
        if not self.analysis_results:
            return

        # Display in Analysis tab
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete("1.0", tk.END)
        self.analysis_text.insert("1.0", json.dumps(self.analysis_results, indent=2))
        self.analysis_text.config(state=tk.DISABLED)

        # Display in Issues tab
        self._display_issues()

        # Display in Suggestions tab
        self._display_suggestions()

        # Switch to Analysis tab
        self.notebook.select(self.analysis_tab)

    def _display_issues(self) -> None:
        """Display issues in Issues tab."""
        self.issues_text.config(state=tk.NORMAL)
        self.issues_text.delete("1.0", tk.END)

        if 'security_warnings' in self.analysis_results:
            self.issues_text.insert(tk.END, "SECURITY WARNINGS:\n\n")
            for warning in self.analysis_results['security_warnings']:
                severity = warning.get('severity', 'unknown').upper()
                message = warning.get('message', 'No message')
                self.issues_text.insert(tk.END, f"[{severity}] {message}\n")

        self.issues_text.config(state=tk.DISABLED)

    def _display_suggestions(self) -> None:
        """Display suggestions in Suggestions tab."""
        self.suggestions_text.config(state=tk.NORMAL)
        self.suggestions_text.delete("1.0", tk.END)

        if 'ai_analysis' in self.analysis_results:
            ai_analysis = self.analysis_results['ai_analysis']
            if 'suggestions' in ai_analysis:
                result = ai_analysis['suggestions']
                if result.get('success'):
                    self.suggestions_text.insert(tk.END, result.get('analysis', 'No suggestions'))
                else:
                    self.suggestions_text.insert(tk.END, f"Error: {result.get('error')}")

        self.suggestions_text.config(state=tk.DISABLED)

    def _export_report(self) -> None:
        """Export analysis report to file."""
        if not self.analysis_results:
            messagebox.showwarning("No Results", "No analysis results to export.")
            return

        try:
            report_path = save_analysis_report(self.analysis_results, "comprehensive")
            messagebox.showinfo("Export Success", f"Report saved to:\n{report_path}")
            logger.info(f"Report exported to {report_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
            logger.error(f"Failed to export report: {e}")

    def _export_critical(self) -> None:
        """Export critical issues to file."""
        if not self.analysis_results:
            messagebox.showwarning("No Results", "No analysis results to export.")
            return

        try:
            critical_path = export_critical_issues(self.analysis_results)
            messagebox.showinfo("Export Success", f"Critical issues saved to:\n{critical_path}")
            logger.info(f"Critical issues exported to {critical_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
            logger.error(f"Failed to export critical issues: {e}")


def main() -> None:
    """Main entry point for the GUI."""
    root = tk.Tk()
    app = EnhancerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
