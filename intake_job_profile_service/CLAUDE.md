# Bash commands
- uv run main.py: run the project
- uv add {package name}: command to add dependencies to the project
- uv remove {package name}: remove a dependencies from the project
- uv add --dev {package name}: command to add development dependencies to the project
- mypy {file name}: command to run type checker against py file

# Workflow
- Ensure that ruff and mypy are added to the project as a dev dependency
- For linting run `ruff check`
- For formatting run `ruff format` 
- Ensure that python files are type checked
