"""End-to-End Checkout and Form Validation tests (10 cases)."""

import pytest
from playwright.sync_api import expect

from data.test_data import CustomerData, ExpectedMessages, Products
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage


class TestCheckoutE2E:
    """10 automated test cases for E2E purchase flow and checkout form BVA."""

    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_complete_purchase_journey_with_decimal_totals_validation(
        self,
        logged_in_inventory: InventoryPage,
        cart_page: CartPage,
        checkout_info_page: CheckoutInfoPage,
        checkout_overview_page: CheckoutOverviewPage,
        checkout_complete_page: CheckoutCompletePage,
    ) -> None:
        for product in Products.E2E_SELECTED_PRODUCTS:
            logged_in_inventory.add_product_to_cart(product)
        logged_in_inventory.open_cart()
        cart_page.proceed_to_checkout()

        customer = CustomerData.DEFAULT_CUSTOMER
        checkout_info_page.fill_shipping_info(
            customer.first_name, customer.last_name, customer.postal_code
        )
        checkout_info_page.continue_to_overview()

        item_prices = checkout_overview_page.get_item_prices()
        subtotal = checkout_overview_page.get_subtotal()
        tax = checkout_overview_page.get_tax()
        total = checkout_overview_page.get_total()

        assert sum(item_prices) == subtotal
        assert subtotal + tax == total

        checkout_overview_page.finish_checkout()
        assert checkout_complete_page.get_complete_header_text() == ExpectedMessages.ORDER_COMPLETE_HEADER

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "first_name,last_name,postal_code,expected_error",
        [
            ("", "Castro", "110111", ExpectedMessages.FIRST_NAME_REQUIRED_ERROR),
            ("Cristian", "", "110111", ExpectedMessages.LAST_NAME_REQUIRED_ERROR),
            ("Cristian", "Castro", "", ExpectedMessages.POSTAL_CODE_REQUIRED_ERROR),
            ("", "", "", ExpectedMessages.FIRST_NAME_REQUIRED_ERROR),
            ("", "", "110111", ExpectedMessages.FIRST_NAME_REQUIRED_ERROR),
            ("Cristian", "", "", ExpectedMessages.LAST_NAME_REQUIRED_ERROR),
        ],
    )
    def test_checkout_step_one_missing_field_validations(
        self,
        logged_in_inventory: InventoryPage,
        cart_page: CartPage,
        checkout_info_page: CheckoutInfoPage,
        first_name: str,
        last_name: str,
        postal_code: str,
        expected_error: str,
    ) -> None:
        logged_in_inventory.add_product_to_cart(Products.BACKPACK)
        logged_in_inventory.open_cart()
        cart_page.proceed_to_checkout()
        checkout_info_page.fill_shipping_info(first_name, last_name, postal_code)
        checkout_info_page.continue_to_overview()
        expect(checkout_info_page.error_banner).to_be_visible()
        assert checkout_info_page.get_error_message() == expected_error

    @pytest.mark.regression
    def test_cancel_on_checkout_step_one_returns_to_cart(
        self,
        logged_in_inventory: InventoryPage,
        cart_page: CartPage,
        checkout_info_page: CheckoutInfoPage,
    ) -> None:
        logged_in_inventory.add_product_to_cart(Products.BOLT_TSHIRT)
        logged_in_inventory.open_cart()
        cart_page.proceed_to_checkout()
        checkout_info_page.cancel()
        expect(cart_page.header_title).to_have_text("Your Cart")

    @pytest.mark.regression
    def test_cancel_on_checkout_overview_returns_to_inventory(
        self,
        logged_in_inventory: InventoryPage,
        cart_page: CartPage,
        checkout_info_page: CheckoutInfoPage,
        checkout_overview_page: CheckoutOverviewPage,
    ) -> None:
        logged_in_inventory.add_product_to_cart(Products.FLEECE_JACKET)
        logged_in_inventory.open_cart()
        cart_page.proceed_to_checkout()
        c = CustomerData.DEFAULT_CUSTOMER
        checkout_info_page.fill_shipping_info(c.first_name, c.last_name, c.postal_code)
        checkout_info_page.continue_to_overview()
        checkout_overview_page.cancel()
        expect(logged_in_inventory.header_title).to_have_text("Products")

    @pytest.mark.regression
    def test_back_home_after_complete_order_resets_cart_badge(
        self,
        logged_in_inventory: InventoryPage,
        cart_page: CartPage,
        checkout_info_page: CheckoutInfoPage,
        checkout_overview_page: CheckoutOverviewPage,
        checkout_complete_page: CheckoutCompletePage,
    ) -> None:
        logged_in_inventory.add_product_to_cart(Products.ONESIE)
        logged_in_inventory.open_cart()
        cart_page.proceed_to_checkout()
        c = CustomerData.DEFAULT_CUSTOMER
        checkout_info_page.fill_shipping_info(c.first_name, c.last_name, c.postal_code)
        checkout_info_page.continue_to_overview()
        checkout_overview_page.finish_checkout()
        checkout_complete_page.back_to_home()
        assert logged_in_inventory.get_cart_count() == 0

