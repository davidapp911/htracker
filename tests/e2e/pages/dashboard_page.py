from tests.e2e.pages.base_page import BasePage


class DashboardPage(BasePage):
    def load_dashboard_page(self, base_url: str):
        self.navigate(f"{base_url}/dashboard")

    def click_logout(self):
        self.page.get_by_role("button", name="Logout").click()

    def redirect_title(self):
        return self.page.get_by_role("heading", name="Log in")

    def go_to_manage_habits(self):
        self.page.get_by_role("link", name="Manage Habits").click()

    def click_new_habit(self):
        self.page.get_by_role("button", name="+ New Habit").click()

    def click_edit_habit(self, habit_name: str):
        self.page.locator("li").filter(
            has=self.page.get_by_text(habit_name, exact=True)
        ).get_by_role("button", name="Edit").click()

    def click_delete_habit(self, habit_name: str):
        self.page.locator("li").filter(
            has=self.page.get_by_text(habit_name, exact=True)
        ).get_by_role("button", name="Delete").click()

    def fill_habit_form(self, habit_data: dict[str, str]):
        self.page.get_by_role("textbox", name="Habit name").fill(habit_data["name"])
        self.page.get_by_role("combobox").select_option(label=habit_data["frequency"])

    def submit_habit_form(self):
        self.page.get_by_role("button", name="Save").click()

    def habit_name_locator(self, habit_name: str):
        return self.page.get_by_text(habit_name)

    def habit_frequency_locator(self, habit_frequency: str):
        return self.page.get_by_text(habit_frequency)

    def go_to_dashboard(self):
        self.page.get_by_role("button", name="Dashboard").click()

    def habit_checklist_item(self, habit_name: str):
        return self.page.get_by_text(habit_name)

    def check_in_habit(self, habit_name: str):
        with self.page.expect_response(lambda r: "/logs" in r.url and r.request.method == "POST"):
            self.page.get_by_text(habit_name).click()

    def undo_check_in(self, habit_name: str):
        with self.page.expect_response(
            lambda r: "/logs/" in r.url and r.request.method == "DELETE"
        ):
            self.page.get_by_text(habit_name).click()

    def go_to_stats(self):
        self.page.get_by_role("link", name="Stats").click()

    def completions_locator(self):
        return (
            self.page.locator("div.rounded-xl")
            .filter(has=self.page.get_by_text("Completions", exact=True))
            .locator("p")
            .last
        )

    def streak_locator(self):
        return (
            self.page.locator("div.rounded-xl")
            .filter(has=self.page.get_by_text("Longest streak", exact=True))
            .locator("p")
            .last
        )


# Navbar
# get_by_role("link", name="Stats")
#
# get_by_role("button", name="Toggle theme")

# Create new habits
# get_by_role("link", name="Manage Habits")
# get_by_role("button", name="+ New Habit")
# get_by_role("heading", name="My Habits")


# New / Edit habit Form
# get_by_role("textbox", name="Habit name")
# get_by_role("combobox")
# get_by_role("button", name="Save")
# get_by_role("button", name="Cancel")


# get_by_role("button", name="Edit").first
