"""Page object for the TodoMVC application."""

from typing import List

from playwright.sync_api import Page, Locator, expect

from pages.base_page import BasePage


class TodoPage(BasePage):
    """Page object encapsulating interactions with the TodoMVC app."""

    URL = "https://demo.playwright.dev/todomvc/#/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Locators
        self.new_todo_input: Locator = page.locator(".new-todo")
        self.todo_list: Locator = page.locator(".todo-list")
        self.todo_items: Locator = self.todo_list.locator("li")
        self.todo_count: Locator = page.locator(".todo-count")
        self.filter_all: Locator = page.locator(".filters a", has_text="All")
        self.filter_active: Locator = page.locator(".filters a", has_text="Active")
        self.filter_completed: Locator = page.locator(
            ".filters a", has_text="Completed"
        )

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def open(self) -> "TodoPage":
        """Open the TodoMVC application and wait until it is ready."""
        self.navigate(self.URL)
        expect(self.new_todo_input).to_be_visible()
        return self

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def add_todo(self, text: str) -> None:
        """Add a new todo item with the given text."""
        self.new_todo_input.fill(text)
        self.new_todo_input.press("Enter")

    def complete_todo(self, text: str) -> None:
        """Mark the todo item with the given text as completed."""
        self._todo_item(text).locator(".toggle").check()

    def delete_todo(self, text: str) -> None:
        """Delete the todo item with the given text."""
        item = self._todo_item(text)
        expect(item).to_be_visible()
        item.hover()
        destroy_button = item.locator(".destroy")
        expect(destroy_button).to_be_visible()
        destroy_button.click()
        expect(item).to_have_count(0)

    def show_all(self) -> None:
        """Activate the 'All' filter."""
        self.filter_all.click()
        expect(self.filter_all).to_have_class("selected")

    def show_active(self) -> None:
        """Activate the 'Active' filter."""
        self.filter_active.click()
        expect(self.filter_active).to_have_class("selected")

    def show_completed(self) -> None:
        """Activate the 'Completed' filter."""
        self.filter_completed.click()
        expect(self.filter_completed).to_have_class("selected")

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------
    def get_visible_todo_texts(self) -> List[str]:
        """Return the texts of all currently visible todo items."""
        return self.todo_items.locator("label").all_inner_texts()

    def get_items_left_count(self) -> int:
        """Return the number of items left shown in the counter."""
        return int(self.todo_count.locator("strong").inner_text())

    def is_todo_completed(self, text: str) -> bool:
        """Return True if the todo item with the given text is completed."""
        return "completed" in (self._todo_item(text).get_attribute("class") or "")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _todo_item(self, text: str) -> Locator:
        """Return the locator of the todo item containing the given text."""
        return self.todo_items.filter(has_text=text)

