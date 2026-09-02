# Project Feedback

## Local setup

This project uses Python 3.12, Django, PostgreSQL (introduced in a later task),
and local LLM tooling through LangChain and Ollama.

Create a virtual environment and install the application plus development
dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the automated tests:

```powershell
python -m pytest
```

Start the Django development server:

```powershell
python manage.py runserver
```

The initial health check is available at `http://127.0.0.1:8000/`.
