import pytest
from playwright.sync_api import Page, ViewportSize, expect

MOBILE_VIEWPORT: ViewportSize = {"width": 375, "height": 812}


@pytest.mark.e2e
def test_mobile_viewport(authenticated_page: Page, base_url, reset_db):
    authenticated_page.set_viewport_size(MOBILE_VIEWPORT)

    authenticated_page.goto(f"{base_url}/login")
    expect(authenticated_page.get_by_role("heading", name="Log in")).to_be_visible()
    expect(authenticated_page.get_by_placeholder("username")).to_be_visible()
    expect(authenticated_page.get_by_placeholder("password")).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Log in")).to_be_visible()

    authenticated_page.goto(f"{base_url}/dashboard")
    expect(authenticated_page.get_by_role("heading", name="Today's Habits")).to_be_visible()

    authenticated_page.goto(f"{base_url}/habits")
    authenticated_page.get_by_role("button", name="+ New Habit").click()
    expect(authenticated_page.get_by_role("textbox", name="Habit name")).to_be_visible()
    expect(authenticated_page.get_by_role("combobox")).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Save")).to_be_visible()
