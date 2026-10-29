"""Inventory sorting and catalog verification tests (10 cases)."""

import pytest
from playwright.sync_api import expect

from data.test_data import SortOptions, Products
from pages.inventory_page import InventoryPage


class TestInventorySortingAndCatalog:
    """10 automated test cases for catalog sorting and item presence."""

    @pytest.mark.regression
    def test_sort_by_price_low_to_high(self, logged_in_inventory: InventoryPage) -> None:
        logged_in_inventory.select_sort_option(SortOptions.PRICE_LOW_TO_HIGH)
        prices = logged_in_inventory.get_all_prices()
        assert prices == sorted(prices)

    @pytest.mark.regression
    def test_sort_by_price_high_to_low(self, logged_in_inventory: InventoryPage) -> None:
        logged_in_inventory.select_sort_option(SortOptions.PRICE_HIGH_TO_LOW)
        prices = logged_in_inventory.get_all_prices()
        assert prices == sorted(prices, reverse=True)

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "sort_option,reverse_order",
        [
            (SortOptions.NAME_A_TO_Z, False),
            (SortOptions.NAME_Z_TO_A, True),
        ],
        ids=["name_a_to_z", "name_z_to_a"],
    )
    def test_sort_by_product_name(
        self, logged_in_inventory: InventoryPage, sort_option: str, reverse_order: bool
    ) -> None:
        logged_in_inventory.select_sort_option(sort_option)
        names = logged_in_inventory.get_all_product_names()
        assert names == sorted(names, reverse=reverse_order)

    @pytest.mark.regression
    @pytest.mark.parametrize("product_name", Products.ALL_PRODUCTS)
    def test_each_catalog_product_is_rendered_and_visible(
        self, logged_in_inventory: InventoryPage, product_name: str
    ) -> None:
        card = logged_in_inventory.inventory_items.filter(has_text=product_name)
        expect(card).to_be_visible()

