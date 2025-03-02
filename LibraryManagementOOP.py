from typing import List
from datetime import datetime, timedelta


class Book:
    def __init__(self, name: str, author: str, book_id: int):
        if not name or not author:
            raise ValueError("Name and author must not be empty")
        self.name = name         # Public, immutable
        self.author = author     # Public, immutable
        self.book_id = book_id   # Public, immutable
        self.borrowed = False    # Public, but controlled by borrow/return logic
        self.due_date = None     # Public, but controlled


class Customer:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self._borrowed_books: List[Book] = []  # Protected to prevent direct manipulation

    def get_borrowed_books(self) -> List[Book]:
        return self._borrowed_books.copy()  # Return a copy for safety

    def borrow_book(self, book: Book, loan_duration: int = 14):
        if len(self._borrowed_books) >= 5:
            raise ValueError(f"{self.name} has reached the borrowing limit of 5 books")
        if book.borrowed:
            raise ValueError(f"Book '{book.name}' is already borrowed")
        self._borrowed_books.append(book)
        book.borrowed = True
        book.due_date = datetime.now() + timedelta(days=loan_duration)
        print(f"{self.name} borrowed '{book.name}', due on {book.due_date}")

    def return_book(self, book: Book):
        if book not in self._borrowed_books:
            raise ValueError(f"{self.name} did not borrow '{book.name}'")
        self._borrowed_books.remove(book)
        book.borrowed = False
        book.due_date = None
        print(f"{self.name} returned '{book.name}'")


class Library:
    def __init__(self, name: str):
        self.name = name
        self._books: List[Book] = []  # Protected to manage additions/removals

    def add_book(self, book: Book):
        if any(b.book_id == book.book_id for b in self._books):
            raise ValueError(f"Book with ID {book.book_id} already exists")
        self._books.append(book)
        print(f"Book '{book.name}' added successfully")

    def remove_book(self, book: Book):
        if book not in self._books:
            raise ValueError(f"Book '{book.name}' not found")
        self._books.remove(book)
        print(f"Book '{book.name}' removed successfully")

    def get_all_books(self):
        if not self._books:
            print(f"No books in {self.name}")
            return
        print(f"Books in {self.name}:")
        for book in self._books:
            status = "Borrowed" if book.borrowed else "Available"
            print(f"- {book.name} by {book.author} (ID: {book.book_id}) - {status}")


class LibraryManager:
    def __init__(self, library: Library):
        self.library = library
        self._customers: List[Customer] = []  # Protected to manage membership

    def add_customer(self, customer: Customer):
        if customer in self._customers:
            raise ValueError(f"Customer '{customer.name}' already registered")
        self._customers.append(customer)
        print(f"Thank you for joining, {customer.name}!")

    def remove_customer(self, customer: Customer):
        if customer not in self._customers:
            raise ValueError(f"Customer '{customer.name}' not found")
        if customer.get_borrowed_books():
            raise ValueError(f"Cannot remove {customer.name} with borrowed books")
        self._customers.remove(customer)
        print(f"Sorry to see you go, {customer.name}")

    def borrow_book(self, customer: Customer, book: Book):
        if book not in self.library._books:
            raise ValueError(f"Book '{book.name}' not in library")
        if customer not in self._customers:
            raise ValueError(f"Customer '{customer.name}' not registered")
        customer.borrow_book(book)

    def return_book(self, customer: Customer, book: Book):
        if customer not in self._customers:
            raise ValueError(f"Customer '{customer.name}' not registered")
        customer.return_book(book)

    def get_borrowed_books_by_customer(self, customer: Customer):
        if customer not in self._customers:
            raise ValueError(f"Customer '{customer.name}' not registered")
        books = customer.get_borrowed_books()
        if not books:
            print(f"{customer.name} has no borrowed books")
        else:
            print(f"Borrowed books by {customer.name}:")
            for book in books:
                print(f"- {book.name} (Due: {book.due_date})")


class LibraryDemo:
    @staticmethod
    def run():
        library = Library("Kitchener Public Library")
        manager = LibraryManager(library)

        # Add books
        book1 = Book("Little Women", "Catherine", 1)
        book2 = Book("Little Tiny House", "No Name", 2)
        book3 = Book("Kite Runner", "Ahmed", 3)
        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)

        # Add customers
        customer1 = Customer("Kavya", "kay@gmail.com")
        customer2 = Customer("Arvind", "arvi@gmail.com")
        manager.add_customer(customer1)
        manager.add_customer(customer2)

        # Borrow and return books
        manager.borrow_book(customer1, book1)
        manager.borrow_book(customer2, book2)
        manager.return_book(customer1, book1)
        manager.borrow_book(customer1, book3)

        # Display info
        library.get_all_books()
        manager.get_borrowed_books_by_customer(customer1)


if __name__ == "__main__":
    LibraryDemo.run()