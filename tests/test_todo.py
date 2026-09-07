"""Tests for the TodoMVC application covering CRUD and filter behaviour."""

import pytest
from playwright.sync_api import expect

from pages.todo_page import TodoPage


class TestAddTodo:
    """Tests for adding new todo items."""

    def test_add_todo_with_english_text(self, todo_page: TodoPage) -> None:
        """A new todo item can be added using English text."""
        todo_page.add_todo("Buy groceries")

        expect(todo_page.todo_items).to_have_count(1)
        assert todo_page.get_visible_todo_texts() == ["Buy groceries"]
        assert todo_page.get_items_left_count() == 1

    def test_add_todo_with_non_english_characters(self, todo_page: TodoPage) -> None:
        """A new todo item can be added using non-English characters."""
        non_english_texts = [
            "Купить молоко",  # Cyrillic
            "牛乳を買う",  # Japanese
            "买牛奶",  # Chinese
            "Übung macht den Meister",  # German umlauts
        ]

        for text in non_english_texts:
            todo_page.add_todo(text)

        expect(todo_page.todo_items).to_have_count(len(non_english_texts))
        assert todo_page.get_visible_todo_texts() == non_english_texts

    def test_add_todo_with_numbers(self, todo_page: TodoPage) -> None:
        """A new todo item can be added that includes numbers."""
        text_with_numbers = "Call 123-456-7890 at 5pm"

        todo_page.add_todo(text_with_numbers)

        expect(todo_page.todo_items).to_have_count(1)
        assert todo_page.get_visible_todo_texts() == [text_with_numbers]


class TestCompleteTodo:
    """Tests for marking todo items as completed."""

    def test_completed_todo_appears_in_completed_view(
        self, todo_page: TodoPage
    ) -> None:
        """A todo item can be marked as completed and appears in 'Completed'."""
        todo_page.add_todo("Finish report")
        todo_page.complete_todo("Finish report")

        assert todo_page.is_todo_completed("Finish report")
        assert todo_page.get_items_left_count() == 0

        todo_page.show_completed()
        assert todo_page.get_visible_todo_texts() == ["Finish report"]


class TestDeleteTodo:
    """Tests for deleting todo items."""

    def test_deleted_todo_disappears_from_all_views(self, todo_page: TodoPage) -> None:
        """A deleted todo item no longer appears in any view."""
        active_todo = "Active task"
        completed_todo = "Completed task"

        todo_page.add_todo(active_todo)
        todo_page.add_todo(completed_todo)
        todo_page.complete_todo(completed_todo)

        # Delete the active item and verify it is gone from every view.
        todo_page.delete_todo(active_todo)

        todo_page.show_all()
        assert todo_page.get_visible_todo_texts() == [completed_todo]

        todo_page.show_active()
        expect(todo_page.todo_items).to_have_count(0)

        todo_page.show_completed()
        assert todo_page.get_visible_todo_texts() == [completed_todo]

        # Delete the completed item and verify the list is empty everywhere.
        todo_page.delete_todo(completed_todo)
        expect(todo_page.todo_items).to_have_count(0)
        expect(todo_page.todo_list).not_to_be_visible()


class TestFilters:
    """Tests for the 'Active' and 'Completed' filters."""

    @pytest.fixture()
    def prepared_page(self, todo_page: TodoPage) -> TodoPage:
        """Provide a page with one active and one completed todo item."""
        todo_page.add_todo("Active task")
        todo_page.add_todo("Completed task")
        todo_page.complete_todo("Completed task")
        return todo_page

    def test_active_filter_shows_only_uncompleted_items(
        self, prepared_page: TodoPage
    ) -> None:
        """The 'Active' filter shows only items that are not completed."""
        prepared_page.show_active()

        expect(prepared_page.todo_items).to_have_count(1)
        assert prepared_page.get_visible_todo_texts() == ["Active task"]
        assert not prepared_page.is_todo_completed("Active task")

    def test_completed_filter_shows_only_completed_items(
        self, prepared_page: TodoPage
    ) -> None:
        """The 'Completed' filter shows only items marked as completed."""
        prepared_page.show_completed()

        expect(prepared_page.todo_items).to_have_count(1)
        assert prepared_page.get_visible_todo_texts() == ["Completed task"]
        assert prepared_page.is_todo_completed("Completed task")
