import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_theme_toggle_persists(authenticated_page: Page, base_url, reset_db):
    authenticated_page.add_init_script("localStorage.setItem('theme', 'dark')")
    authenticated_page.goto(f"{base_url}/dashboard")

    expect(authenticated_page.locator("html")).to_have_class("dark")

    authenticated_page.get_by_role("button", name="Toggle theme").click()
    expect(authenticated_page.locator("html")).not_to_have_class("dark")

    authenticated_page.get_by_role("link", name="Stats").click()
    expect(authenticated_page.locator("html")).not_to_have_class("dark")
