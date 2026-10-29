"""Shopping cart state and dynamic navigation tests (12 cases)."""

import pytest
from playwright.sync_api import expect

from data.test_data import Products
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCartAndNavigation:
    """12 automated test cases for cart state transitions and navigation."""

    @pytest.mark.regression
    @pytest.mark.parametrize("product_name", Products.ALL_PRODUCTS)
    def test_add_and_remove_single_product_updates_cart_badge(
        self, logged_in_inventory: InventoryPage, product_name: str
    ) -> None:
        logged_in_inventory.add_product_to_cart(product_name)
        assert logged_in_inventory.get_cart_count() == 1
        logged_in_inventory.remove_product_from_cart(product_name)
        assert logged_in_inventory.get_cart_count() == 0

    @pytest.mark.regression
    @pytest.mark.parametrize("count", [1, 2, 3, 4])
    def test_adding_multiple_products_increments_badge_accurately(
        self, logged_in_inventory: InventoryPage, count: int
    ) -> None:
        for product in Products.ALL_PRODUCTS[:count]:
            logged_in_inventory.add_product_to_cart(product)
        assert logged_in_inventory.get_cart_count() == count

    @pytest.mark.regression
    def test_remove_item_directly_from_cart_screen(
        self, logged_in_inventory: InventoryPage, cart_page: CartPage
    ) -> None:
        logged_in_inventory.add_product_to_cart(Products.BACKPACK)
        logged_in_inventory.open_cart()
        assert cart_page.get_items_count() == 1
        cart_page.remove_item(Products.BACKPACK)
        assert cart_page.get_items_count() == 0

    @pytest.mark.regression
    def test_continue_shopping_returns_to_inventory_preserving_cart(
        self, logged_in_inventory: InventoryPage, cart_page: CartPage
    ) -> None:
        logged_in_inventory.add_product_to_cart(Products.BIKE_LIGHT)
        logged_in_inventory.open_cart()
        cart_page.continue_shopping()
        expect(logged_in_inventory.header_title).to_have_text("Products")
        assert logged_in_inventory.get_cart_count() == 1

