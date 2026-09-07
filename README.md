# TodoMVC Playwright POM Test Framework

Automated UI tests for the [TodoMVC demo application](https://demo.playwright.dev/todomvc/#/)
built with **Playwright**, **pytest**, and the **Page Object Model POM)** pattern.
Dependencies are managed with **[Poetry](https://python-poetry.org/)**.

## Project structure

```
test_ai/
✔—— conftest.py            # Pytest fixtures (provides a ready TodoPage)
├—— pages/
✔—— │—— base_page.py       # Base page object with shared functionality
✔—— └—— todo_page.py       # Page object for the TodoMVC application
✔—— tests/
├—— └—— test_todo.py       # Test suite (add / complete / delete / filters)
✔—— pyproject.toml         # Poetry dependencies + pytest configuration
✔—— poetry.lock            # Locked dependency versions
├—— README.md
```

## Covered scenarios

- Add a todo item with English text
- Add a todo item with non-English characters (Cyrillic, Japanese, Chinese, umlauts)
- Add a todo item that includes numbers
- Mark a todo item as completed and verify it in the "Completed" view
- Delete a todo item and verify it disappears from all views
- "Active" filter shows only uncompleted items
- "Completed" filter shows only completed items

## Prerequisites

- **Python 3.10+**
- **Poetry** — install it if you don't have it:

  Installation for any platform:
  ```bash
  pip install poetry
  ```

## Setup

From the project root, install dependencies (Poetry creates a virtual environment
automatically):

```bash
poetry install
```

Install the Playwright browser binaries:

```bash
poetry run playwright install chromium
```

> On Linux, if you hit missing system library errors, run
> `sudo poetry run playwright install --with-deps chromium` (or install the
> dependencies manually with `playwright install-deps`).

## Running the tests

Run the whole suite (headless Chromium by default):

```bash
poetry run pytest
```

Run with a visible browser window (headed mode):

```bash
poetry run pytest --headed
```

Slow down actions to follow them visually:

```bash
poetry run pytest --headed --slowmo 500
```

Run a specific test file or test:

```bash
poetry run pytest tests/test_todo.py
poetry run pytest tests/test_todo.py::TestFilters
```

Run on a different browser (install it first with `poetry run playwright install <browser>`):

```bash
poetry run pytest --browser firefox
poetry run pytest --browser webkit
```

Collect traces, screenshots, and videos (useful for debugging failures):

```bash
poetry run pytest --tracing on --screenshot on --video on
```

> **Tip:** instead of prefixing every command with `poetry run`, you can activate
> the Poetry-managed virtual environment first:
> - Linux / macOS: `eval $(poetry env activate)` or `source $(poetry env info --path)/bin/activate`
> - Windows (PowerShell): `Invoke-Expression (poetry env activate)`
>
> Then just run `pytest`, `playwright`, etc. directly.
