"""CartPage module representing the user shopping cart screen."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for the SauceDemo Shopping Cart Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_items: Locator = page.locator('[data-test="inventory-item"]')
        self.item_names: Locator = page.locator('[data-test="inventory-item-name"]')
        self.checkout_button: Locator = page.locator('[data-test="checkout"]')
        self.continue_shopping_button: Locator = page.locator('[data-test="continue-shopping"]')

    def get_items_count(self) -> int:
        return self.cart_items.count()

    def get_item_names(self) -> list[str]:
        return [name.strip() for name in self.item_names.all_inner_texts()]

    def remove_item(self, product_name: str) -> None:
        item = self.cart_items.filter(has_text=product_name)
        item.get_by_role("button", name="Remove").click()

    def proceed_to_checkout(self) -> None:
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()

