from tests.e2e.pages.base_page import BasePage


class LoginPage(BasePage):
    def load_login_page(self, base_url: str):
        self.navigate(f"{base_url}/login")

    def fill_login_form(self, user_data: dict[str, str]):
        self.page.get_by_role("textbox", name="username").fill(user_data["username"])
        self.page.get_by_role("textbox", name="password").fill(user_data["password"])

    def submit_form(self):
        self.page.get_by_role("button", name="Log in").click()

    def dashboard_heading(self):
        return self.page.get_by_role("heading", name="Today's Habits")

    def username_not_found_message(self):
        return self.page.get_by_text("Username not found.")

    def wrong_password_message(self):
        return self.page.get_by_text("Password does not match.")
