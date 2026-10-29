"""Shared pytest fixtures for the E2E Playwright test suite."""

import pytest
from playwright.sync_api import Page, expect

from data.test_data import TestUsers
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.navigate("/")
    return login


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_info_page(page: Page) -> CheckoutInfoPage:
    return CheckoutInfoPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)


@pytest.fixture
def logged_in_inventory(
    page: Page,
    login_page: LoginPage,
    inventory_page: InventoryPage,
) -> InventoryPage:
    login_page.login(
        username=TestUsers.STANDARD_USER.username,
        password=TestUsers.STANDARD_USER.password,
    )
    expect(inventory_page.header_title).to_be_visible()
    expect(inventory_page.header_title).to_have_text("Products")
    return inventory_page

