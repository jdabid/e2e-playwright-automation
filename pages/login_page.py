"""LoginPage module encapsulating authentication elements and actions."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the SauceDemo Login Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input: Locator = page.locator('[data-test="username"]')
        self.password_input: Locator = page.locator('[data-test="password"]')
        self.login_button: Locator = page.locator('[data-test="login-button"]')
        self.error_banner: Locator = page.locator('[data-test="error"]')

    def navigate(self, path: str = "/") -> None:
        super().navigate(path)

    def fill_username(self, username: str) -> None:
        self.username_input.fill(username)

    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    def click_login(self) -> None:
        self.login_button.click()

    def login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        return self.error_banner.inner_text().strip()

