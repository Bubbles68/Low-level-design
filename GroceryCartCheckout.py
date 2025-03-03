from collections import defaultdict
from typing import Dict
import uuid

class Grocery:
    def __init__(self, product_id: int, name: str, description: str, price: float, category: str):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category

class User:
    def __init__(self, name: str, email: str, user_id: str):
        if not email or not name:
            raise ValueError("Email and name must not be empty")
        self.name = name
        self.email = email
        self.user_id = user_id

class Cart:
    def __init__(self, cart_id: str):
        self.cart_id = cart_id
        self._items: Dict[Grocery, int] = defaultdict(int)  # Protected
        self._total_price = 0.0

    def add_item(self, item: Grocery):
        self._items[item] += 1
        self._update_total()

    def remove_item(self, item: Grocery, quantity: int):
        if item not in self._items:
            raise ValueError(f"Item '{item.name}' not in cart")
        if quantity > self._items[item]:
            raise ValueError(f"Cannot remove {quantity} of '{item.name}' (only {self._items[item]} in cart)")
        self._items[item] -= quantity
        if self._items[item] == 0:
            del self._items[item]
        self._update_total()

    def _update_total(self):
        self._total_price = sum(item.price * qty for item, qty in self._items.items())

    def get_items(self) -> Dict[Grocery, int]:
        return dict(self._items)  # Return a copy

    def get_total_price(self) -> float:
        return self._total_price

class CartManager:
    def __init__(self):
        self._cart_user_map: Dict[str, Cart] = {}
        self._grocery_items: Dict[int, Grocery] = {}

    def add_grocery_item(self, item: Grocery):
        self._grocery_items[item.product_id] = item

    def add_item_to_cart(self, user_id: str, item_id: int):
        if item_id not in self._grocery_items:
            raise ValueError(f"Item ID {item_id} not found")
        if user_id not in self._cart_user_map:
            self._cart_user_map[user_id] = Cart(str(uuid.uuid4()))  # Unique cart ID
        cart = self._cart_user_map[user_id]
        cart.add_item(self._grocery_items[item_id])

    def remove_item_from_cart(self, user_id: str, item_id: int, quantity: int):
        if user_id not in self._cart_user_map:
            raise ValueError(f"No cart found for user {user_id}")
        if item_id not in self._grocery_items:
            raise ValueError(f"Item ID {item_id} not found")
        cart = self._cart_user_map[user_id]
        cart.remove_item(self._grocery_items[item_id], quantity)

    def checkout_items(self, user_id: str) -> float:
        if user_id not in self._cart_user_map:
            raise ValueError(f"No cart found for user {user_id}")
        cart = self._cart_user_map[user_id]
        total = cart.get_total_price()
        print(f"Checking out cart {cart.cart_id} for {total:.2f}")
        del self._cart_user_map[user_id]  # Clear cart after checkout
        return total

    def generate_invoice(self, user_id: str):
        if user_id not in self._cart_user_map:
            raise ValueError(f"No cart found for user {user_id}")
        cart = self._cart_user_map[user_id]
        print(f"Invoice for cart {cart.cart_id}:")
        for item, qty in cart.get_items().items():
            print(f"- {item.name} (x{qty}): ${item.price * qty:.2f}")
        print(f"Total: ${cart.get_total_price():.2f}")

class GroceryCartDemo:
    @staticmethod
    def run():
        cart_manager = CartManager()

        # Add grocery items
        item1 = Grocery(1, "Salt", "Table salt", 2.5, "Spices")
        item2 = Grocery(2, "Sugar", "Granulated sugar", 3.5, "Baking Supplies")
        item3 = Grocery(3, "Cake", "Vanilla flavor", 6.0, "Ready to Eat")
        cart_manager.add_grocery_item(item1)
        cart_manager.add_grocery_item(item2)
        cart_manager.add_grocery_item(item3)

        # Add users
        user1 = User("Kavya", "kay@gmail.com", "1000")
        user2 = User("Arvind", "arvi@gmail.com", "2000")

        # Add items to carts
        cart_manager.add_item_to_cart(user1.user_id, item2.product_id)
        cart_manager.add_item_to_cart(user1.user_id, item3.product_id)
        cart_manager.add_item_to_cart(user1.user_id, item2.product_id)
        cart_manager.add_item_to_cart(user2.user_id, item1.product_id)
        cart_manager.add_item_to_cart(user2.user_id, item3.product_id)

        # Generate invoices and checkout
        cart_manager.generate_invoice(user1.user_id)
        cart_manager.checkout_items(user1.user_id)
        cart_manager.generate_invoice(user2.user_id)

if __name__ == "__main__":
    GroceryCartDemo.run()