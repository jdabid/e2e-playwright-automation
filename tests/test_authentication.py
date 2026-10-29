"""Authentication E2E test suite covering positive, locked, logout, and negative partitions."""

import pytest
from playwright.sync_api import Page, expect

from data.test_data import TestUsers, ExpectedMessages
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestAuthentication:
    """10 automated test cases for authentication and session security."""

    @pytest.mark.smoke
    def test_valid_login_redirects_to_inventory(
        self, page: Page, login_page: LoginPage, inventory_page: InventoryPage
    ) -> None:
        login_page.login(TestUsers.STANDARD_USER.username, TestUsers.STANDARD_USER.password)
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(inventory_page.header_title).to_have_text("Products")

    @pytest.mark.smoke
    def test_locked_out_user_sees_error_banner(
        self, page: Page, login_page: LoginPage
    ) -> None:
        login_page.login(TestUsers.LOCKED_OUT_USER.username, TestUsers.LOCKED_OUT_USER.password)
        expect(login_page.error_banner).to_be_visible()
        assert login_page.get_error_message() == ExpectedMessages.LOCKED_OUT_ERROR

    @pytest.mark.smoke
    def test_logout_clears_session_and_returns_to_login(
        self, page: Page, logged_in_inventory: InventoryPage, login_page: LoginPage
    ) -> None:
        logged_in_inventory.logout()
        expect(login_page.login_button).to_be_visible()

    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            ("", "secret_sauce", ExpectedMessages.USERNAME_REQUIRED_ERROR),
            ("standard_user", "", ExpectedMessages.PASSWORD_REQUIRED_ERROR),
            ("", "", ExpectedMessages.USERNAME_REQUIRED_ERROR),
            ("standard_user", "wrong_pass", ExpectedMessages.INVALID_CREDENTIALS_ERROR),
            ("unknown_user", "secret_sauce", ExpectedMessages.INVALID_CREDENTIALS_ERROR),
            ("STANDARD_USER", "secret_sauce", ExpectedMessages.INVALID_CREDENTIALS_ERROR),
            ("standard_user", "SECRET_SAUCE", ExpectedMessages.INVALID_CREDENTIALS_ERROR),
        ],
        ids=[
            "empty_username",
            "empty_password",
            "both_empty",
            "wrong_password",
            "unknown_username",
            "uppercase_username",
            "uppercase_password",
        ],
    )
    def test_negative_login_partitions(
        self, login_page: LoginPage, username: str, password: str, expected_error: str
    ) -> None:
        login_page.login(username=username, password=password)
        expect(login_page.error_banner).to_be_visible()
        assert login_page.get_error_message() == expected_error

