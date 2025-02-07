# Software Project Enhancer

This tool analyzes a software project, suggests improvements, reviews the
suggestions, plans the implementation, optimizes the plan, and generates a final
report. It leverages Ollama language models for each stage of the process.

## Requirements

- **Python:** This script requires Python 3.x.
- **Ollama:** You need to have Ollama installed and running. Download it from
  [https://ollama.com/](https://ollama.com/).
- **Ollama Models:** The script uses specific Ollama models. Make sure you have
  pulled them:

  ```bash
  ollama pull llama3.2:latest
  ollama pull olmo2:13b
  ollama pull deepseek-r1
  ollama pull deepseek-r1:14b
  ollama pull phi4:latest
  ```

- **Tkinter:** This should come preinstalled with most Python installations. If
  not:
  - **Debian/Ubuntu:** `sudo apt-get install python3-tk`
  - **Fedora/CentOS/RHEL:** `sudo yum install python3-tkinter`
  - **macOS:** Usually included with Python from python.org.
- **Python Libraries:**

  ```bash
  pip install ollama tkinter pathlib
  ```

## Installation

1. **Clone the repository** (if applicable - since this is a single file, this
   step might not be necessary, but I'll include it for completeness).

   ```bash
    git clone <repository_url>
    cd <repository_directory>
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   (You would need to create a `requirements.txt` file with `ollama`, `tkinter`,
   and `pathlib` listed, but since you can't create new files in the root, I'll
   just leave the command as is and the user can create it if they want)

## Usage

1. **Run the script:**

   ```bash
   python software_enhancer.py
   ```

2. **Enter the project path:** In the application window, enter the absolute
   path to the root directory of the software project you want to analyze.
3. **Click "Analyze & Enhance Project":** The tool will start the analysis and
   enhancement process. Progress and results will be displayed in the output
   area.

## Configuration

The `OLLAMA_MODELS` dictionary in `software_enhancer.py` configures which Ollama
models are used for each phase:

```python
OLLAMA_MODELS = {
    "analysis": "llama3.2:latest",
    "generation": "olmo2:13b",
    "vetting": "deepseek-r1",
    "finalization": "deepseek-r1:14b",
    "enhancement": "phi4:latest",
    "comprehensive": "phi4:latest",
    "presenter": "deepseek-r1:14b",
}
```

You can change these models if you have other models installed with Ollama and
want to experiment. Make sure the models you choose are appropriate for the
task.

## Troubleshooting

- **"Error: No project path entered."**: Make sure you enter the project path in
  the input field before clicking the button.
- **"Error: Project path does not exist."**: Double-check the path you entered.
  It must be the absolute path to a valid directory.
- **"Error during ...":** If you encounter errors during any of the analysis or
  generation phases, it might be due to issues with the Ollama models or network
  connectivity. Make sure Ollama is running and the models are downloaded.
- **GUI Issues:** If the GUI doesn't display correctly, ensure you have Tkinter
  installed properly.
