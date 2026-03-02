# AGENTS.md

## Purpose
This file provides guidance for agentic coding agents (like opencode) working in the qleverflow repository. It includes build, lint, and test commands, code style guidelines, and other best practices to ensure consistent and high-quality contributions. The repository focuses on deploying Qlever (a SPARQL database engine) with UI and mapping components via Docker Compose, along with Python scripts for validation and processing.

## Architecture Overview
- Core Components: Qlever Server, Qlever UI, Qlever Petrimaps.
- Key Directories:
  - validation/shapeValidator/: Python scripts for SHACL validation and concurrent processing.
  - mcp/: Agent and server code for MCP (likely Multi-Context Processing).
  - deployment/: Docker Compose and Kubernetes yaml files.
  - catalogues/: Qlever configuration files.
  - ui/: Gradio-based UI for querying.
  - docs/: Documentation and notes.
- Technologies: Python 3, Docker, Docker Compose, SPARQL, RDF tools like pyoxigraph.
- Dependencies: See requirements.txt (qlever, marimo, polars, kuzu, networkx, igraph, plotly, holoviews, gradio, etc.).

## Build Commands
### Python Dependencies
- Install dependencies: pip install -r requirements.txt
  - This installs all necessary Python packages for scripts in validation/, mcp/, ui/, etc.

### Docker Builds
- Build MCP server image: docker build -t mcp-app . (in mcp/server/)
- General index building: Use IndexBuilderMain as per CLAUDE.md for manual index builds with text support.
- Full deployment build:
  - Step 1: Download data and build index - docker compose -f initialize_compose.yaml up
  - Step 2: Start services - docker compose -f server_compose.yaml up

### Other Builds
- No Makefile or specific build scripts found. For Python scripts, no compilation needed.
- For notebooks (e.g., analyticsPlayground.ipynb): Use jupyter or marimo to run.

## Lint Commands
No explicit linter configuration found (e.g., no .flake8, pyproject.toml with tool configurations). Assume standard Python linting tools based on common practices.

- Format code: black . (Install black if needed: pip install black)
- Lint with Ruff: ruff check . (Install ruff: pip install ruff; preferred for speed)
- Alternative: flake8 . (If preferring PEP8 strict)
- Type checking: mypy . (Install mypy: pip install mypy; though no type hints widely used in current code)

Run lint before commits to maintain code quality. Fix all warnings.

## Test Commands
Limited automated tests found. Scripts like testIOBound.py and testThreadPool.py appear to be standalone processing scripts rather than unit tests. No pytest or unittest imports detected in sampled files.

- Run processing scripts (manual 'tests'):
  - python validation/shapeValidator/testIOBound.py <url> <shapefile>
  - python validation/shapeValidator/testThreadPool.py (assuming similar usage)
- For unit tests: If adding, use pytest framework.
  - Install pytest: pip install pytest
  - Run all tests: pytest
  - Run single test file: pytest validation/shapeValidator/testIOBound.py
  - Run single test function: pytest validation/shapeValidator/testIOBound.py::test_function_name (Note: Current scripts don't have test functions; refactor if needed)
- SPARQL testing: curl -s \"http://workstation.lan:7007\" -H \"Accept: application/qlever-results+json\" -H \"Content-type: application/sparql-query\" --data \"SELECT * WHERE { ?s ?p ?o } LIMIT 10\"
- Verify deployments: After docker compose up, check services on ports 7007 (Qlever), 8176 (UI), 9090 (Petrimaps).

If adding new tests, place them in a tests/ directory and use pytest conventions.

## Code Style Guidelines
Follow PEP 8 for Python code. Mimic existing styles in the repository.

### Imports
- Group imports: Standard library first, then third-party, then local.
- Alphabetical order within groups.
- Avoid wildcard imports (from module import *).
- Example:
  import os
  import sys
  from concurrent.futures import ThreadPoolExecutor
  import pyoxigraph
  from defs.getGraphs import query_sparql_endpoint

### Formatting
- Line length: 88 characters (black default).
- Indentation: 4 spaces, no tabs.
- Strings: Prefer double quotes for consistency.
- Use f-strings for formatting.
- Blank lines: One between functions, two between classes.

### Types
- Use type hints where possible (e.g., def process_uri(uri: str, sf: str) -> str:).
- Install typing extensions if needed for advanced types.
- Run mypy for type checking.

### Naming Conventions
- Variables/functions: snake_case (e.g., query_sparql_endpoint).
- Classes: CamelCase (e.g., ShapeValidator).
- Constants: UPPER_CASE.
- Descriptive names; avoid single-letter variables except in loops.
- Private: _prefix for protected, __prefix for private.

### Error Handling
- Use try-except blocks for expected errors (e.g., network failures in SPARQL queries).
- Log errors meaningfully: Use print for now, consider logging module for production.
- Raise specific exceptions (e.g., ValueError for invalid inputs).
- Example:
  try:
      store.load(shr, RdfFormat.TURTLE)
  except Exception as e:
      print(f\"An error occurred: {e}\")
- Always handle file I/O errors.

### General Best Practices
- Docstrings: Use Google or NumPy style for functions/classes.
- Comments: Sparse but explanatory; no unnecessary comments.
- Security: Never hardcode secrets; use env vars (see deployment/env.example).
- Docker: Run as non-root (user 1000:1000); persist data with volumes (ql_dvol).
- Concurrency: Use ThreadPoolExecutor for I/O-bound tasks, as in existing scripts.
- RDF/SPARQL: Use pyoxigraph for graph operations; ensure N-Quads format for outputs.

## Cursor/Copilot Rules
No .cursor/rules/, .cursorrules, or .github/copilot-instructions.md found in the repository. Follow general AI coding best practices:
- Generate code that matches existing patterns.
- Avoid introducing new dependencies without necessity.
- Ensure code is idempotent and safe for deployments.

## Additional Notes
- Git: Standard workflow; commit messages: \"type: description\" (e.g., \"feat: add new validation script\").
- Proactiveness: Analyze filenames before editing; refuse malicious code.
- When in doubt, use tools like glob, grep, read to explore.
- For Qlever-specific: Follow Qleverfile format in catalogues/ for configurations.
- Length: This file is approximately 150 lines for comprehensive guidance.

(End of AGENTS.md)