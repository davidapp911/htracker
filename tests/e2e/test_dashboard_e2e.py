import pytest
from playwright.sync_api import Page, expect

from tests.constants import HABIT_DATA
from tests.e2e.pages.dashboard_page import DashboardPage


@pytest.mark.e2e
def test_dashboard_logout(authenticated_page: Page, base_url, reset_db):
    page_obj = DashboardPage(authenticated_page)
    page_obj.load_dashboard_page(base_url)
    page_obj.click_logout()

    expect(page_obj.redirect_title()).to_be_visible()


@pytest.mark.e2e
def test_habit_lifecycle(authenticated_page: Page, base_url, reset_db):
    page_obj = DashboardPage(authenticated_page)
    page_obj.load_dashboard_page(base_url)
    page_obj.go_to_manage_habits()
    page_obj.click_new_habit()
    page_obj.fill_habit_form(HABIT_DATA)
    page_obj.submit_habit_form()

    expect(page_obj.habit_name_locator(HABIT_DATA["name"])).to_be_visible()
    expect(page_obj.habit_frequency_locator(HABIT_DATA["frequency"])).to_be_visible()

    page_obj.go_to_dashboard()
    expect(page_obj.habit_checklist_item(HABIT_DATA["name"])).to_be_visible()

    page_obj.check_in_habit(HABIT_DATA["name"])
    page_obj.undo_check_in(HABIT_DATA["name"])

    expect(page_obj.habit_checklist_item(HABIT_DATA["name"])).not_to_have_class(
        "line-through text-blue-100"
    )

    page_obj.go_to_stats()

    expect(page_obj.completions_locator()).to_have_text(HABIT_DATA["completions"])
    expect(page_obj.streak_locator()).to_have_text(HABIT_DATA["streak"])


@pytest.mark.e2e
def test_edit_habit(authenticated_page: Page, base_url, create_habit, reset_db):
    page_obj = DashboardPage(authenticated_page)
    page_obj.load_dashboard_page(base_url)
    page_obj.go_to_manage_habits()
    page_obj.click_edit_habit(create_habit.name)
    page_obj.fill_habit_form(HABIT_DATA)
    page_obj.submit_habit_form()
    page_obj.go_to_dashboard()
    expect(page_obj.habit_name_locator(HABIT_DATA["name"])).to_be_visible()


@pytest.mark.e2e
def test_delete_habit(authenticated_page: Page, base_url, create_habit, reset_db):
    page_obj = DashboardPage(authenticated_page)
    page_obj.load_dashboard_page(base_url)
    page_obj.go_to_manage_habits()
    page_obj.click_delete_habit(create_habit.name)
    page_obj.go_to_dashboard()
    expect(page_obj.habit_name_locator(create_habit.name)).not_to_be_visible()
