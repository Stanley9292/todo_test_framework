"""Base page object with shared functionality for all pages."""

from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to the given URL."""
        self.page.goto(url)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

