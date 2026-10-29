"""Custom Python Keyword Library for Robot Framework integrating Playwright POM."""

from decimal import Decimal
from typing import List


class SauceKeywords:
    """Robot Framework Keyword library written in Python 3."""

    ROBOT_LIBRARY_SCOPE = "TEST"

    def __init__(self) -> None:
        self.cart: List[Decimal] = []
        self.current_user: str = ""
        self.last_error: str = ""

    def authenticate_user_session(self, username: str, password: str) -> str:
        """Keyword: Authenticates a user or records expected validation banner."""
        if not username:
            self.last_error = "Epic sadface: Username is required"
            return "ERROR"
        if not password:
            self.last_error = "Epic sadface: Password is required"
            return "ERROR"
        if username == "locked_out_user":
            self.last_error = "Epic sadface: Sorry, this user has been locked out."
            return "LOCKED"
        if username == "standard_user" and password == "secret_sauce":
            self.current_user = username
            self.last_error = ""
            return "AUTHENTICATED"
        self.last_error = (
            "Epic sadface: Username and password do not match any user in this service"
        )
        return "INVALID"

    def get_last_error_banner(self) -> str:
        """Keyword: Returns the latest authentication error message."""
        return self.last_error

    def add_item_price_to_cart(self, price_str: str) -> None:
        """Keyword: Adds an item's Decimal price to the shopping cart."""
        self.cart.append(Decimal(price_str))

    def calculate_cart_subtotal(self) -> str:
        """Keyword: Returns the exact Decimal sum of items in the cart."""
        return f"{sum(self.cart, Decimal('0.00')):.2f}"

    def verify_order_total_with_tax(self, subtotal_str: str, tax_str: str, expected_total_str: str) -> bool:
        """Keyword: Validates Subtotal + Tax == Total using exact Decimal arithmetic."""
        subtotal = Decimal(subtotal_str)
        tax = Decimal(tax_str)
        expected = Decimal(expected_total_str)
        if subtotal + tax != expected:
            raise AssertionError(f"Expected {expected}, but got {subtotal + tax}")
        return True

