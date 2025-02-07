import os
import tkinter as tk
from pathlib import Path

import ollama

# Configuration
OLLAMA_MODELS = {
    "analysis": "llama3.2:latest",  # Project structure analysis
    "generation": "olmo2:13b",  # Improvement suggestions
    "vetting": "deepseek-r1",  # Code review
    "finalization": "deepseek-r1:14b",  # Implementation planning
    "enhancement": "phi4:latest",  # Advanced optimization
    "comprehensive": "phi4:latest",  # Final project review
    "presenter": "deepseek-r1:14b",  # Final report generation
}

# Progress messages
PROGRESS_MESSAGES = {
    "start": "Analyzing software project...\n",
    "analyzing": "Phase 1/6: Project Analysis\n",
    "analysis_done": "Analysis complete.\n\n",
    "generating": "Phase 2/6: Improvement Planning\n",
    "generation_done": "Planning complete.\n\n",
    "vetting": "Phase 3/6: Code Review\n",
    "vetting_done": "Review complete.\n\n",
    "finalizing": "Phase 4/6: Implementation Planning\n",
    "finalize_done": "Planning complete.\n\n",
    "enhancing": "Phase 5/6: Optimization\n",
    "enhance_done": "Optimization complete.\n\n",
    "comprehensive": "Phase 6/6: Final Review\n",
    "complete": "Process complete.\n\n",
}


def analyze_project(project_path, model_name):
    """Analyzes the entire software project structure."""
    try:
        # Get project structure
        structure = []
        for root, dirs, files in os.walk(project_path):
            level = root.replace(project_path, "").count(os.sep)
            indent = " " * 4 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 4 * (level + 1)
            for f in files:
                structure.append(f"{subindent}{f}")

        project_structure = "\n".join(structure)

        messages = [
            {
                "role": "user",
                "content": (
                    "Analyze this software project structure:\n\n"
                    f"{project_structure}\n\n"
                    "Focus on:\n"
                    "1. Overall architecture and organization\n"
                    "2. Project structure and patterns\n"
                    "3. Potential architectural issues\n"
                    "4. Dependencies and relationships\n"
                    "5. Best practices compliance\n\n"
                    "Provide a clear, focused analysis that will help in "
                    "improving this project. Stay focused on architectural "
                    "and structural aspects."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during project analysis: {e}")
            return None
    except Exception as e:
        print(f"Error during project analysis: {e}")
        return None


def generate_improvements(analysis, model_name):
    """Generates potential project-wide improvements."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Based on this project analysis: '{analysis}'\n\n"
                    "Generate specific improvements that:\n"
                    "1. Address architectural issues\n"
                    "2. Enhance project structure\n"
                    "3. Improve modularity\n"
                    "4. Optimize dependencies\n"
                    "5. Follow industry best practices\n\n"
                    "Important: Generate practical, focused improvements "
                    "that can be realistically implemented. Focus on "
                    "project-wide enhancements."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during improvement generation: {e}")
            return None
    except Exception as e:
        print(f"Error during improvement generation: {e}")
        return None


def review_project(improvements, model_name):
    """Reviews and validates the suggested project improvements."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    "Review these project improvements: "
                    f"'{improvements}'\n\n"
                    "Evaluate how well they enhance the project:\n"
                    "1. Are they architecturally sound?\n"
                    "2. Do they improve maintainability?\n"
                    "3. Are they scalable?\n"
                    "4. Do they follow best practices?\n"
                    "5. Are they practical to implement?\n\n"
                    "Important: Focus on validating improvements that "
                    "will benefit the entire project. Flag any suggestions "
                    "that might introduce complexity or technical debt."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during project review: {e}")
            return None
    except Exception as e:
        print(f"Error during project review: {e}")
        return None


def plan_implementation(review_report, model_name):
    """Creates implementation plan for validated improvements."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Based on this review: {review_report}\n\n"
                    "Create an implementation plan that:\n"
                    "1. Prioritizes improvements\n"
                    "2. Breaks down into manageable tasks\n"
                    "3. Identifies dependencies\n"
                    "4. Minimizes disruption\n"
                    "5. Includes rollback strategies\n\n"
                    "Important: Create a practical plan that can be "
                    "executed incrementally while maintaining project "
                    "stability."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during implementation planning: {e}")
            return None
    except Exception as e:
        print(f"Error during implementation planning: {e}")
        return None


def optimize_project(implementation_plan, model_name):
    """Optimizes the implementation plan."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    "Optimize this implementation plan:\n\n"
                    f"{implementation_plan}\n\n"
                    "Focus on:\n"
                    "1. Resource efficiency\n"
                    "2. Risk mitigation\n"
                    "3. Timeline optimization\n"
                    "4. Quality assurance\n"
                    "5. Success metrics\n\n"
                    "Important: Optimize the plan while maintaining "
                    "feasibility and risk management. Return ONLY the "
                    "optimized version."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during plan optimization: {e}")
            return None
    except Exception as e:
        print(f"Error during plan optimization: {e}")
        return None


def comprehensive_review(
    project_path,
    analysis_report,
    improvements,
    review_report,
    implementation_plan,
    optimized_plan,
    model_name,
):
    """Creates final report with complete enhancement strategy."""
    try:
        # First, use phi4 for comprehensive review
        messages = [
            {
                "role": "user",
                "content": (
                    "Review all project enhancement documents and create "
                    "a comprehensive strategy:\n\n"
                    f"Project: {project_path}\n"
                    f"Analysis: {analysis_report}\n"
                    f"Improvements: {improvements}\n"
                    f"Review: {review_report}\n"
                    f"Implementation: {implementation_plan}\n"
                    f"Optimization: {optimized_plan}\n\n"
                    "Create a refined strategy that ensures successful "
                    "project enhancement while minimizing risks."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            improved = response["message"]["content"]
        except Exception as e:
            print(f"Error during comprehensive review: {e}")
            improved = None

        # Then use deepseek-r1:14b for final report
        messages = [
            {
                "role": "user",
                "content": (
                    "You are the final report generator. Review this "
                    "enhancement strategy and create a clear, actionable "
                    f"report:\n\n{improved}\n\n"
                    "Requirements:\n"
                    "1. Clear executive summary\n"
                    "2. Prioritized recommendations\n"
                    "3. Implementation roadmap\n"
                    "4. Risk assessment\n"
                    "5. Success metrics\n\n"
                    "Create a professional report that stakeholders can "
                    "use to guide the enhancement process.\n\n"
                    "Start your response with 'ENHANCEMENT REPORT:' "
                    "followed by the complete report."
                ),
            }
        ]
        try:
            response = ollama.chat(model=OLLAMA_MODELS["presenter"], messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during report generation: {e}")
            return None
    except Exception as e:
        print(f"Error during comprehensive review: {e}")
        return None


def create_model_indicators(parent):
    """Creates a frame with model status indicators."""
    frame = tk.Frame(parent, bg="#f0f0f0")
    frame.pack(fill=tk.X, pady=(0, 10))

    indicators = {}
    for model_type in OLLAMA_MODELS:
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


def create_scrolled_text(parent, height=10, width=50, readonly=False):
    """Helper function to create a Text widget with a scrollbar."""
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


def main():
    """Main function."""
    progress_msgs = PROGRESS_MESSAGES

    root = tk.Tk()
    root.title("Software Project Enhancer")
    root.configure(bg="#f0f0f0")
    root.minsize(800, 600)

    main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create model status indicators
    model_indicators = create_model_indicators(main_frame)

    # Reset all indicators to inactive
    def reset_indicators():
        for label in model_indicators.values():
            label.config(fg="#666666")

    # Set an indicator as active
    def set_active_model(model_type):
        reset_indicators()
        model_indicators[model_type].config(fg="#4a90e2")

    input_label = tk.Label(
        main_frame,
        text="Enter project path:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
    )
    input_label.pack(anchor=tk.W)

    input_frame, input_text = create_scrolled_text(
        main_frame,
        height=2,
        width=80,
    )
    input_frame.pack(fill=tk.X, pady=(5, 15))

    output_label = tk.Label(
        main_frame,
        text="Analysis Results:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
    )
    output_label.pack(anchor=tk.W)

    output_frame, output_text = create_scrolled_text(
        main_frame,
        height=25,
        width=80,
        readonly=True,
    )
    output_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 15))

    def update_output(text):
        """Updates the output text area."""
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, text)
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)

    def process_project():
        project_path = input_text.get("1.0", tk.END).strip()
        if not project_path:
            update_output("Error: No project path entered.")
            return

        if not Path(project_path).exists():
            update_output("Error: Project path does not exist.")
            return

        output = progress_msgs["start"]
        update_output(output)

        # Phase 1: Project Analysis
        set_active_model("analysis")
        output += progress_msgs["analyzing"]
        update_output(output)

        analysis_report = analyze_project(
            project_path,
            OLLAMA_MODELS["analysis"],
        )
        if not analysis_report:
            update_output(output + "Error: Analysis failed.")
            return

        output += progress_msgs["analysis_done"]
        output += analysis_report + "\n\n"
        update_output(output)

        # Phase 2: Improvement Planning
        set_active_model("generation")
        output += progress_msgs["generating"]
        update_output(output)

        improvements = generate_improvements(
            analysis_report,
            OLLAMA_MODELS["generation"],
        )
        if not improvements:
            update_output(output + "Error: Planning failed.")
            return

        output += progress_msgs["generation_done"]
        output += improvements + "\n\n"
        update_output(output)

        # Phase 3: Project Review
        set_active_model("vetting")
        output += progress_msgs["vetting"]
        update_output(output)

        review_report = review_project(
            improvements,
            OLLAMA_MODELS["vetting"],
        )
        if not review_report:
            update_output(output + "Error: Review failed.")
            return

        output += progress_msgs["vetting_done"]
        output += review_report + "\n\n"
        update_output(output)

        # Phase 4: Implementation Planning
        set_active_model("finalization")
        output += progress_msgs["finalizing"]
        update_output(output)

        implementation_plan = plan_implementation(
            review_report,
            OLLAMA_MODELS["finalization"],
        )
        if not implementation_plan:
            update_output(output + "Error: Planning failed.")
            return

        output += progress_msgs["finalize_done"]
        output += implementation_plan + "\n\n"
        update_output(output)

        # Phase 5: Plan Optimization
        set_active_model("enhancement")
        output += progress_msgs["enhancing"]
        update_output(output)

        optimized_plan = optimize_project(
            implementation_plan,
            OLLAMA_MODELS["enhancement"],
        )
        if not optimized_plan:
            update_output(output + "Error: Optimization failed.")
            return

        output += progress_msgs["enhance_done"]
        output += optimized_plan + "\n\n"
        update_output(output)

        # Phase 6: Comprehensive Review
        set_active_model("comprehensive")
        output += progress_msgs["comprehensive"]
        update_output(output)

        comprehensive_result = comprehensive_review(
            project_path,
            analysis_report,
            improvements,
            review_report,
            implementation_plan,
            optimized_plan,
            OLLAMA_MODELS["comprehensive"],
        )
        if not comprehensive_result:
            update_output(output + "Error: Review failed.")
            return

        # Final report generation
        set_active_model("presenter")
        output += "Generating final report...\n"
        update_output(output)

        # Present final result
        output += progress_msgs["complete"]
        if "ENHANCEMENT REPORT:" in comprehensive_result:
            final_text = comprehensive_result.split(
                "ENHANCEMENT REPORT:",
                1,
            )[1].strip()
            output += final_text + "\n"
        else:
            output += comprehensive_result + "\n"
        update_output(output)

    process_button = tk.Button(
        main_frame,
        text="Analyze & Enhance Project",
        command=process_project,
        font=("Arial", 11),
        bg="#4a90e2",
        fg="white",
        padx=20,
        pady=10,
        relief=tk.RAISED,
        cursor="hand2",
    )
    process_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
