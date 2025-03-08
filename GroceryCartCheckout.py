from collections import defaultdict
from typing import Optional
import uuid

class Product:
    def __init__(self, name: str, desc: str, product_id: str, price: float):
        self.name = name
        self.desc = desc
        self.product_id = product_id
        self.price = price
        self._hash = hash(product_id)  # For defaultdict key
    
    def __hash__(self): return self._hash
    def __eq__(self, other): return isinstance(other, Product) and self.product_id == other.product_id

class User:
    def __init__(self, name: str, email: str, user_id: str):
        self._name = name
        self._email = email
        self.user_id = user_id
    
    def get_name(self) -> str: return self._name
    def get_email(self) -> str: return self._email

class Cart:
    def __init__(self):
        self.products = defaultdict(int)  # Product: quantity
        self.cart_id = str(uuid.uuid4())
    
    def add_product(self, product: Product, quantity: Optional[int] = 1) -> bool:
        quantity = quantity or 1
        self.products[product] += quantity
        print(f"Product {product.name} added")
        return True
    
    def remove_product(self, product: Product, quantity: Optional[int] = 1) -> bool:
        quantity = quantity or 1
        if product not in self.products:
            raise ValueError("Product not in cart")
        self.products[product] -= quantity
        if self.products[product] <= 0:
            del self.products[product]
        return True
    
    def get_total_price(self) -> float:
        return sum(prod.price * qty for prod, qty in self.products.items())

class CartManager:
    def __init__(self):
        self.user_cart_map = {}
    
    def add_products_to_cart(self, user_id: str, product: Product, quantity: Optional[int] = 1) -> bool:
        if user_id not in self.user_cart_map:
            self.user_cart_map[user_id] = Cart()
        return self.user_cart_map[user_id].add_product(product, quantity)
    
    def remove_products_from_cart(self, user_id: str, product: Product, quantity: Optional[int] = 1) -> bool:
        if user_id not in self.user_cart_map:
            raise ValueError("Cart not found")
        return self.user_cart_map[user_id].remove_product(product, quantity)
    
    def get_total_price_of_cart(self, user_id: str) -> float:
        if user_id not in self.user_cart_map:
            raise ValueError("Cart not found")
        price = self.user_cart_map[user_id].get_total_price()
        print(f"Total price: {price}")
        return price
    
    def checkout(self, user_id: str) -> bool:
        if user_id not in self.user_cart_map:
            raise ValueError("Cart not found")
        price = self.get_total_price_of_cart(user_id)
        # Mock third-party call
        resp = 200  # Assume success
        if resp == 200:
            print("Payment processed. Order will be delivered soon")
            del self.user_cart_map[user_id]  # Clear cart
            return True
        print("Payment failed. Please retry")
        return False

class Demo:
    @staticmethod
    def run():
        cart_manager = CartManager()
        product1 = Product("dell laptop", "computer", "p1", 1200)
        product2 = Product("apple laptop", "computer", "p2", 2000)
        user1 = User("kavya", "kay@gmail.com", "u123")
        
        cart_manager.add_products_to_cart(user1.user_id, product1, 2)
        cart_manager.add_products_to_cart(user1.user_id, product2)
        cart_manager.remove_products_from_cart(user1.user_id, product1, 1)
        cart_manager.get_total_price_of_cart(user1.user_id)
        cart_manager.checkout(user1.user_id)

if __name__ == "__main__":
    Demo.run()