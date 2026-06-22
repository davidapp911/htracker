import pytest
from playwright.sync_api import Page, expect

from tests.e2e.pages.login_page import LoginPage
from tests.e2e.pages.register_page import RegisterPage


@pytest.mark.e2e
def test_register_new_user(page: Page, base_url, reset_db):
    page_obj = RegisterPage(page)
    page_obj.load_register_page(base_url)
    page_obj.fill_register_form(
        {
            "email": "randomemail@domain.com",
            "username": "randomusername",
            "password": "strongpassword123",
        }
    )

    page_obj.submit_form()

    expect(page_obj.redirect_title()).to_be_visible()


@pytest.mark.e2e
def test_register_duplicate_email(page: Page, base_url, create_user, reset_db):
    page_obj = RegisterPage(page)
    page_obj.load_register_page(base_url)
    page_obj.fill_register_form(
        {
            "email": create_user.email,
            "username": "randomusername",
            "password": "strongpassword123",
        }
    )
    page_obj.submit_form()
    expect(page_obj.duplicate_email_message()).to_be_visible()


@pytest.mark.e2e
def test_register_duplicate_username(page: Page, base_url, create_user, reset_db):
    page_obj = RegisterPage(page)
    page_obj.load_register_page(base_url)
    page_obj.fill_register_form(
        {
            "email": "uniqueemail@domain.com",
            "username": create_user.username,
            "password": "strongpassword123",
        }
    )
    page_obj.submit_form()
    expect(page_obj.duplicate_username_message()).to_be_visible()


@pytest.mark.e2e
def test_login_user(page: Page, base_url, create_user, reset_db):
    page_obj = LoginPage(page)
    page_obj.load_login_page(base_url)
    page_obj.fill_login_form(
        {
            "username": create_user.username,
            "password": create_user.password,
        }
    )

    page_obj.submit_form()
    expect(page_obj.dashboard_heading()).to_be_visible()


@pytest.mark.e2e
def test_login_non_registered_user(page: Page, base_url, reset_db):
    page_obj = LoginPage(page)
    page_obj.load_login_page(base_url)
    page_obj.fill_login_form(
        {
            "username": "non_existent_user",
            "password": "SoMePaSsWoRd123",
        }
    )

    page_obj.submit_form()
    expect(page_obj.username_not_found_message()).to_be_visible()


@pytest.mark.e2e
def test_login_wrong_password(page: Page, base_url, create_user, reset_db):
    page_obj = LoginPage(page)
    page_obj.load_login_page(base_url)
    page_obj.fill_login_form(
        {
            "username": create_user.username,
            "password": "ThIsPaSsWoRdIsWrOnG123",
        }
    )

    page_obj.submit_form()
    expect(page_obj.wrong_password_message()).to_be_visible()
