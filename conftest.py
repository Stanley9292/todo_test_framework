"""Pytest fixtures for the TodoMVC test suite."""

import pytest
from playwright.sync_api import Page

from pages.todo_page import TodoPage


@pytest.fixture()
def todo_page(page: Page) -> TodoPage:
    """Provide a TodoPage opened on a fresh TodoMVC instance."""
    return TodoPage(page).open()

