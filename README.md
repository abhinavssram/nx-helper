# nx-helper

**nx-helper** is a tool for analyzing and querying dependency graphs (such as those generated by [Nx](https://nx.dev/)) using natural language and LLM-powered tools. It helps answer questions about entities (apps, libs, etc.), their types, and their dependencies in a monorepo.

---

## Features
- Query the number and types of entities in your Nx graph
- Find dependencies and dependents for any entity
- Group dependencies by type (e.g., app, lib)
- Check if one entity depends on another
- Find common dependencies between entities
- Natural language interface powered by LLMs

---

## Installation

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the root directory with your Anthropic API key:
     ```env
     ANTHROPIC_API_KEY=your-anthropic-api-key
     ```

---

## Input Data

- The tool expects a file named `nx-output.json` in the project root. This file should contain your Nx project graph in JSON format.
- Example structure:
  ```json
  {
    "graph": {
      "nodes": {
        "my-app": { "name": "my-app", "type": "app", ... },
        "my-lib": { "name": "my-lib", "type": "lib", ... }
      },
      "dependencies": {
        "my-app": [ { "source": "my-app", "target": "my-lib", "type": "static" } ]
      }
    }
  }
  ```
- You can generate this file using Nx's built-in graph export tools or scripts.

---

## Usage

Run the main script:
```bash
python main.py
```
You will be prompted to enter your questions about the Nx graph. Type `exit` to quit.

---

## Requirements
- Python 3.8+
- [langchain-anthropic](https://pypi.org/project/langchain-anthropic/)
- Anthropic API key (for Claude LLM)

---

## Outputs
- Some queries will write results to the `/outputs` directory for later review.

---