# AI TESTER

## Description

AI Tester is a powerful tool designed to assist developers and QA engineers in analyzing application logs. It leverages Large Language Models (LLMs) to automatically detect bugs, identify anomalies, and generate insightful reports. By pinpointing areas of concern, AI Tester helps streamline the debugging process and improve software quality.

## AI Architecture

AI Tester is built around a modular AI workflow, not a persistent AI agent. The workflow is orchestrated using LangGraph, which allows each step—log parsing, analysis, and report generation—to be defined, tested, and extended independently. This design ensures that the tool is robust, maintainable, and easy to adapt to new log formats or analysis requirements.

Each execution of AI Tester runs the workflow from start to finish on the provided log file(s), producing structured analysis and reports without maintaining long-term state or goals.

## Architecture Highlights

- **Modular Workflow:** Each step (parsing, analysis, reporting) is a separate, testable component orchestrated by LangGraph.
- **Config-Driven Parsing:** Log format and structure are defined in YAML, enabling easy adaptation to new log sources without code changes.
- **Structured Data Flow:** Uses Pydantic models for type-safe, validated data exchange between workflow steps.
- **Separation of Concerns:** Core logic is decoupled from CLI/web, supporting future extensibility (e.g., API or web app integration).
- **Extensible Design:** New parsers, analyzers, or report generators can be added with minimal changes to the workflow.

## Engineering Highlights

- **Type Safety:** Pydantic and type hints ensure robust, predictable data handling throughout the codebase.
- **Testability:** Modular components and config-driven design make unit and integration testing straightforward.
- **Modern Tooling:** Utilizes Typer for CLI, LangGraph for workflow orchestration, and uv for dependency management.
- **Containerization:** Docker support for reproducible, environment-agnostic deployment.
- **Developer Experience:** Clean code structure, clear documentation, and rich CLI output for usability and maintainability.

## Features

- 🚀 **Automated Log Analysis**: Parses and understands various log formats to identify critical information.
- 🐞 **Intelligent Bug Detection**: Uses AI to find potential bugs and errors that might be missed during manual review.
- 📊 **Comprehensive Reporting**: Generates detailed reports summarizing the findings, including stack traces and error frequencies.
- 💡 **Actionable Recommendations**: Provides suggestions on where to focus debugging efforts and potential root causes.
- 🔄 **Flexible LLM Backend**: Easily switch between local models using Ollama and powerful cloud-based models from OpenAI.
- 🧩 **Extensible Parsers**: Add new log parsers to support custom log formats from your applications.

## Architecture Overview

```
ai_tester/
├── app/
│   ├── agent/              # LangGraph workflow for orchestrating log analysis
│   ├── llm/                # LLM backend (Ollama/OpenAI wrapper)
│   ├── analyzer/           # Analyzers
│   ├── parser/             # Log parsers
│   ├── raport_generator/   # Report generator
│   └── cli.py              # CLI entrypoint
├── config/
│   └── settings.yaml       # Configuration for LLM provider, model, etc.
├── main.py                 # Main application entrypoint
├── tests/
│   └── test_data/          # Sample log files for testing
├── Dockerfile
├── docker-compose.yml      # For running the local model
├── pyproject.toml
└── README.md
```

## Technology Stack

- **Python**: Core programming language
- **Typer**: For building the command-line interface with type hints and user-friendly commands.
- **LangChain**: For creating and managing LLM objects and orchestrating AI workflows.
- **Pydantic**: For structured data validation, ensuring stable and predictable AI input/output formats (e.g., analyze state, bug reports).
- **LangGraph**: Orchestrates the agent workflow for modular log parsing, analysis, and report generation.
- **OpenAI / Ollama**: Large Language Model (LLM) providers for log analysis and bug detection.
- **uv**: Dependency management and environment handling.
- **Docker**: Containerization for easy deployment and reproducibility.
- **PyYAML**: For configuration file parsing.
- **Rich**: (Optional) For enhanced CLI output and formatting.

## Getting Started

### Prerequisites

- Python 3.13+
- `uv` for dependency management.
- Access to an OpenAI API key or a running Ollama instance.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ai_tester.git
    cd ai_tester
    ```

2.  **Install dependencies:**
    ```bash
    uv pip install -e .
    ```

## Configuration

Edit `config/settings.yaml` to configure your desired LLM provider and log format.

**Example for OpenAI:**

```yaml
llm:
  provider: "openai"
  model: "gpt-4-turbo"
  # api_key is read from OPENAI_API_KEY environment variable
```

example of env file .env

```
LLM_API_KEY=your-open-ai-api-key
```

**Example for Ollama:**

```yaml
llm:
  provider: "ollama"
  model: "llama3"
  url: "http://localhost:11434"
```

### Log Format and Structure

You can define your log format and structure in the `config/settings.yaml` file. The parser dynamically generates the log entry fields and their order based on the `structure` section. This makes the tool flexible and adaptable to different log formats without code changes.

**Example:**

```yaml
log:
  format: '^\[(?P<timestamp>.*?)\]\s+\[(?P<log_level>\w+)\]\s+\[(?P<component>.*?)\]\s+(?P<message>.*)$'
  structure:
    timestamp: '\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3}' # e.g., 2024-08-01 09:01:12,400
    log_level: "INFO|WARNING|ERROR|CRITICAL|DEBUG"
    component: "[A-Za-z]+"
    message: ".*"
```

- **format:** The regex pattern for parsing each log line. Use named groups matching the keys in `structure`.
- **structure:** Defines the expected fields and their validation regex. The parser will use these keys to generate the log entry structure and extract values in the specified order.
- To support a new log format, simply update the `format` and `structure` in the config file.

## Usage

AI Tester can be run from the command line.

```bash
python main.py analyze /path/to/your/logfile.log
```

For example, to analyze the included sample log file:

```bash
python main.py analyze dummy_log.txt
```

test data in tests/test_data/..

## License

Distributed under the MIT License. See `LICENSE` for more information.
