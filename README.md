# Software Enhancement Pipeline

A Python application that uses multiple AI models to enhance and improve code
through various stages of analysis and optimization.

## Project Structure

```
software_enhancer/
├── __init__.py          # Package initialization
├── config.py            # Configuration settings
├── file_processor.py    # File operations handling
├── queue_manager.py     # Processing queue management
├── enhancement_pipeline.py  # Core enhancement logic
├── gui.py              # Graphical user interface
└── main.py             # Package entry point
```

## Components

1. **Configuration (config.py)**

   - Manages model configurations and progress messages
   - Defines the AI models used for each enhancement phase

2. **File Processing (file_processor.py)**

   - Handles file operations (find, read, write, backup)
   - Manages text file detection and processing

3. **Queue Management (queue_manager.py)**

   - Manages the processing queue with thread-safe operations
   - Tracks file processing status

4. **Enhancement Pipeline (enhancement_pipeline.py)**

   - Implements the core enhancement logic
   - Processes files through 7 distinct phases:
     1. Analysis and Structure
     2. Optimizations
     3. Best Practices
     4. Error Handling
     5. Advanced Optimization
     6. Comprehensive Review
     7. Final Polish

5. **GUI (gui.py)**
   - Provides a user-friendly interface
   - Shows real-time progress and status

## Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -e .
   ```

## Usage

Run the application using:

```bash
python run.py
```

Or after installation:

```bash
enhance
```

## Features

- Multi-phase code enhancement using various AI models
- Real-time progress tracking
- Automatic file backup before modifications
- Thread-safe queue management
- User-friendly GUI interface

## Requirements

- Python 3.8 or higher
- Ollama AI models configured and running
