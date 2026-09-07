# TodoMVC Playwright POM Test Framework

Automated UI tests for the [TodoMVC demo application](https://demo.playwright.dev/todomvc/#/)
built with **Playwright**, **pytest**, and the **Page Object Model (POM)** pattern.

## Project structure

```
test_ai/
├── conftest.py            # Pytest fixtures (provides a ready TodoPage)
├── pages/
│   ├── base_page.py       # Base page object with shared functionality
│   └── todo_page.py       # Page object for the TodoMVC application
├── tests/
│   └── test_todo.py       # Test suite (add / complete / delete / filters)
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Python dependencies
└── README.md
```

## Covered scenarios

- Add a todo item with English text
- Add a todo item with non-English characters (Cyrillic, Japanese, Chinese, umlauts)
- Add a todo item that includes numbers
- Mark a todo item as completed and verify it in the "Completed" view
- Delete a todo item and verify it disappears from all views
- "Active" filter shows only uncompleted items
- "Completed" filter shows only completed items

## Setup

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the Playwright browsers:

   ```bash
   playwright install chromium
   ```

## Running the tests

Run the whole suite (headless Chromium by default):

```bash
pytest
```

Run with a visible browser window:

```bash
pytest --headed
```

Run a specific test file or test:

```bash
pytest tests/test_todo.py
pytest tests/test_todo.py::TestFilters
```

Run on a different browser:

```bash
pytest --browser firefox
pytest --browser webkit
```

Generate an HTML report of a failing run (traces/screenshots via pytest-playwright):

```bash
pytest --tracing on --screenshot on --video on
```

