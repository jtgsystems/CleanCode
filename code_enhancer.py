import tkinter as tk

import ollama

# Configuration
OLLAMA_MODELS = {
    "analysis": "llama3.2:latest",  # Initial code analysis
    "generation": "olmo2:13b",  # Solution generation
    "vetting": "deepseek-r1",  # Code review
    "finalization": "deepseek-r1:14b",  # Code improvement
    "enhancement": "phi4:latest",  # Advanced optimization
    "comprehensive": "phi4:latest",  # Final code review
    "presenter": "deepseek-r1:14b",  # Final code cleanup
}

# Progress messages
PROGRESS_MESSAGES = {
    "start": "Processing code...\n",
    "analyzing": "Phase 1/6: Code Analysis\n",
    "analysis_done": "Analysis complete.\n\n",
    "generating": "Phase 2/6: Solution Generation\n",
    "generation_done": "Generation complete.\n\n",
    "vetting": "Phase 3/6: Code Review\n",
    "vetting_done": "Review complete.\n\n",
    "finalizing": "Phase 4/6: Code Improvement\n",
    "finalize_done": "Improvement complete.\n\n",
    "enhancing": "Phase 5/6: Optimization\n",
    "enhance_done": "Optimization complete.\n\n",
    "comprehensive": "Phase 6/6: Final Review\n",
    "complete": "Process complete.\n\n",
}


def analyze_code(code, model_name):
    """Analyzes the input code."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Analyze this code: '{code}'\n\n"
                    "Focus on:\n"
                    "1. Code structure and organization\n"
                    "2. Potential code smells\n"
                    "3. Performance bottlenecks\n"
                    "4. Security vulnerabilities\n"
                    "5. Best practices compliance\n\n"
                    "Provide a clear, focused analysis that will help in "
                    "improving this exact code. Stay focused on the task "
                    "and avoid going off on tangents."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during analysis: {e}")
            return None
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None


def generate_solutions(analysis, model_name):
    """Generates potential improvements based on analysis."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Based on this analysis: '{analysis}'\n\n"
                    "Generate specific improvements that:\n"
                    "1. Address identified issues\n"
                    "2. Enhance code quality\n"
                    "3. Improve performance\n"
                    "4. Fix security issues\n"
                    "5. Follow best practices\n\n"
                    "Important: Generate practical, focused improvements "
                    "that directly enhance the code. Avoid theoretical "
                    "discussions or tangents."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during solution generation: {e}")
            return None
    except Exception as e:
        print(f"Error during solution generation: {e}")
        return None


def review_code(improvements, model_name):
    """Reviews and validates the suggested improvements."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    "Review these suggested improvements: "
                    f"'{improvements}'\n\n"
                    "Evaluate how well they enhance the original code:\n"
                    "1. Do they improve code quality?\n"
                    "2. Are they maintainable?\n"
                    "3. Do they follow best practices?\n"
                    "4. Are they practical and implementable?\n\n"
                    "Important: Focus on validating improvements that "
                    "directly enhance the original code. Flag any "
                    "suggestions that might introduce new issues or "
                    "complexity."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during code review: {e}")
            return None
    except Exception as e:
        print(f"Error during code review: {e}")
        return None


def improve_code(review_report, original_code, model_name):
    """Creates improved version incorporating validated enhancements."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Original Code: {original_code}\n"
                    f"Validated Improvements: {review_report}\n\n"
                    "Create an improved version that:\n"
                    "1. Maintains original functionality\n"
                    "2. Incorporates validated improvements\n"
                    "3. Uses clean coding practices\n"
                    "4. Improves readability\n"
                    "5. Follows language conventions\n\n"
                    "Important: Stay focused on improving the code. Return "
                    "only the improved version of the input code."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during code improvement: {e}")
            return None
    except Exception as e:
        print(f"Error during code improvement: {e}")
        return None


def optimize_code(improved_code, model_name):
    """Optimizes and enhances the improved code."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    "Optimize and enhance this code:\n\n"
                    f"{improved_code}\n\n"
                    "Focus on:\n"
                    "1. Performance optimization\n"
                    "2. Memory efficiency\n"
                    "3. Code organization\n"
                    "4. Error handling\n"
                    "5. Documentation\n\n"
                    "Important: Stay focused on optimizing THIS code. "
                    "Do NOT create examples or add unrelated content. "
                    "Return ONLY the optimized version."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during optimization: {e}")
            return None
    except Exception as e:
        print(f"Error during optimization: {e}")
        return None


def comprehensive_review(
    original_code,
    analysis_report,
    solutions,
    review_report,
    improved_code,
    optimized_code,
    model_name,
):
    """Creates final version and ensures clean presentation."""
    try:
        # First, use phi4 for comprehensive review
        messages = [
            {
                "role": "user",
                "content": (
                    "Review all versions of this code and create an "
                    "improved version that combines the best elements:\n\n"
                    f"Original: {original_code}\n"
                    f"Analysis: {analysis_report}\n"
                    f"Solutions: {solutions}\n"
                    f"Review: {review_report}\n"
                    f"Improved: {improved_code}\n"
                    f"Optimized: {optimized_code}\n\n"
                    "Create a refined version that maintains functionality "
                    "while maximizing code quality and performance."
                ),
            }
        ]
        try:
            response = ollama.chat(model=model_name, messages=messages)
            improved = response["message"]["content"]
        except Exception as e:
            print(f"Error during comprehensive review: {e}")
            improved = None

        # Then use deepseek-r1:14b as final presenter
        messages = [
            {
                "role": "user",
                "content": (
                    "You are the final presenter. Review this code and "
                    "ensure it's presented in the cleanest possible "
                    f"format:\n\n{improved}\n\n"
                    "Requirements:\n"
                    "1. Follow language style guide\n"
                    "2. Use consistent formatting\n"
                    "3. Add necessary documentation\n"
                    "4. Organize imports properly\n"
                    "5. Maintain clean structure\n\n"
                    "First, identify 25 potential formatting or "
                    "style issues, then fix them all. Finally, "
                    "present the result in the cleanest possible format.\n\n"
                    "Start your response with 'FINAL CODE:' followed "
                    "by the clean, formatted code."
                ),
            }
        ]
        try:
            response = ollama.chat(model=OLLAMA_MODELS["presenter"], messages=messages)
            return response["message"]["content"]
        except Exception as e:
            print(f"Error during final presentation: {e}")
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
    root.title("Code Enhancer")
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
        text="Enter your code:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
    )
    input_label.pack(anchor=tk.W)

    input_frame, input_text = create_scrolled_text(
        main_frame,
        height=15,
        width=80,
    )
    input_frame.pack(fill=tk.X, pady=(5, 15))

    output_label = tk.Label(
        main_frame,
        text="Results:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
    )
    output_label.pack(anchor=tk.W)

    output_frame, output_text = create_scrolled_text(
        main_frame,
        height=20,
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

    def process_code():
        input_code = input_text.get("1.0", tk.END).strip()
        if not input_code:
            update_output("Error: No code entered.")
            return

        output = progress_msgs["start"]
        update_output(output)

        # Phase 1: Analysis
        set_active_model("analysis")
        output += progress_msgs["analyzing"]
        update_output(output)

        analysis_report = analyze_code(
            input_code,
            OLLAMA_MODELS["analysis"],
        )
        if not analysis_report:
            update_output(output + "Error: Analysis failed.")
            return

        output += progress_msgs["analysis_done"]
        output += analysis_report + "\n\n"
        update_output(output)

        # Phase 2: Solution Generation
        set_active_model("generation")
        output += progress_msgs["generating"]
        update_output(output)

        solutions = generate_solutions(
            analysis_report,
            OLLAMA_MODELS["generation"],
        )
        if not solutions:
            update_output(output + "Error: Generation failed.")
            return

        output += progress_msgs["generation_done"]
        output += solutions + "\n\n"
        update_output(output)

        # Phase 3: Code Review
        set_active_model("vetting")
        output += progress_msgs["vetting"]
        update_output(output)

        review_report = review_code(
            solutions,
            OLLAMA_MODELS["vetting"],
        )
        if not review_report:
            update_output(output + "Error: Review failed.")
            return

        output += progress_msgs["vetting_done"]
        output += review_report + "\n\n"
        update_output(output)

        # Phase 4: Code Improvement
        set_active_model("finalization")
        output += progress_msgs["finalizing"]
        update_output(output)

        improved_code = improve_code(
            review_report,
            input_code,
            OLLAMA_MODELS["finalization"],
        )
        if not improved_code:
            update_output(output + "Error: Improvement failed.")
            return

        output += progress_msgs["finalize_done"]
        output += improved_code + "\n\n"
        update_output(output)

        # Phase 5: Optimization
        set_active_model("enhancement")
        output += progress_msgs["enhancing"]
        update_output(output)

        optimized_code = optimize_code(
            improved_code,
            OLLAMA_MODELS["enhancement"],
        )
        if not optimized_code:
            update_output(output + "Error: Optimization failed.")
            return

        output += progress_msgs["enhance_done"]
        output += optimized_code + "\n\n"
        update_output(output)

        # Phase 6: Comprehensive Review
        set_active_model("comprehensive")
        output += progress_msgs["comprehensive"]
        update_output(output)

        comprehensive_result = comprehensive_review(
            input_code,
            analysis_report,
            solutions,
            review_report,
            improved_code,
            optimized_code,
            OLLAMA_MODELS["comprehensive"],
        )
        if not comprehensive_result:
            update_output(output + "Error: Review failed.")
            return

        # Final presentation cleanup
        set_active_model("presenter")
        output += "Cleaning up final presentation...\n"
        update_output(output)

        # Present final result
        output += progress_msgs["complete"]
        if "FINAL CODE:" in comprehensive_result:
            final_text = comprehensive_result.split(
                "FINAL CODE:",
                1,
            )[1].strip()
            output += final_text + "\n"
        else:
            output += comprehensive_result + "\n"
        update_output(output)

    process_button = tk.Button(
        main_frame,
        text="Analyze & Enhance Code",
        command=process_code,
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
