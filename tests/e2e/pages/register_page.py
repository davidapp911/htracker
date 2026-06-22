from tests.e2e.pages.base_page import BasePage


class RegisterPage(BasePage):
    def load_register_page(self, base_url: str):
        self.navigate(f"{base_url}/register")

    def fill_register_form(self, user_data: dict[str, str]):
        self.page.get_by_role("textbox", name="email").fill(user_data["email"])
        self.page.get_by_role("textbox", name="username").fill(user_data["username"])
        self.page.get_by_role("textbox", name="password").fill(user_data["password"])

    def submit_form(self):
        self.page.get_by_role("button", name="Register").click()

    def redirect_title(self):
        return self.page.get_by_role("heading", name="Log in")

    def duplicate_email_message(self):
        return self.page.get_by_text("Email already in use.")

    def duplicate_username_message(self):
        return self.page.get_by_text("Username already taken.")
