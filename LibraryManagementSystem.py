from collections import defaultdict


class Library:
    def __init__(self, name:str):
        self.name=name
        self.books=[]

    def addBook(self, book):
        self.books.append(book)
        print(f'book added successfully')
        return

    def removeBook(self, book):
        try:
            self.books.remove(book)
            print(f'book removed successfully')
        except ValueError:
            print(f'Book not found in library')
    
    def getAllBooks(self):
        print(f'Fetching all books .......')
        for book in self.books:
            print(f'{book.name}')
        return

class Book:
    def __init__(self, name:str, author:str, bookId:int):
        self.name=name
        self.author=author
        self.bookId = bookId

class Customer:
    def __init__(self, name:str, email:str):
        self.name=name
        self.email=email
        self.borrowedBooks=[]

    def getBorrowedBooks(self):
        length = len(self.borrowedBooks)
        if length!=0:
            return (length, self.borrowedBooks)
        
    def addBookToBorrowedList(self, book):
        self.borrowedBooks.append(book)

class LibraryManager:
    def __init__(self, library):
        self.customers=[]
        self.borrowedBooks=set()
        self.books=library.books


    def addCustomer(self, customer):
        print(f'Thank you for becoming a member : {customer.name}')
        self.customers.append(customer)
        return 
    
    def removeCustomer(self, customer):
        if customer in self.customers:
            print(f'Sorry to see you go : {customer.name}')
            self.customers.remove(customer)
            return 
        else:
            print(f'Cant remove customer thats not in the system')
    
    def borrowBook(self, book, customer):
        if book not in self.books:
            print("Book not in library")
            return
        if book in self.borrowedBooks:
            print("Book is already borrowed")
            return
        if(customer.getBorrowedBooks()!=None):
            numberOfBooks, borrowedBooks = customer.getBorrowedBooks()
        else:
            numberOfBooks, borrowedBooks = 0, []
        if book not in self.borrowedBooks:
            if numberOfBooks>5:
                print(f'Sorry you have already borrowed 5 books. Please return atleast one to borrow more')
                return
            else:
                customer.addBookToBorrowedList(book)
                self.borrowedBooks.add(book)

    def returnBook(self, book, customer):
        borrowed = customer.getBorrowedBooks()
        if borrowed is None or book not in borrowed[1]:
            print(f"Can't return book that's not borrowed by {customer.name}")
            return
        numberOfBooks, borrowedBooks = borrowed
        self.borrowedBooks.remove(book)
        borrowedBooks.remove(book)
        print(f"Book returned successfully")

    def getAllBooksBorrowedByCustomer(self, customer):
        borrowed = customer.getBorrowedBooks()
        if borrowed and borrowed[0] > 0:
            numberOfBooks, borrowedBooks = borrowed
            print(f'Borrowed Books by customer {customer.name} are :')
            for book in borrowedBooks:
                print(f'{book.name}')
        else:
            print(f'Customer doesn’t have any books borrowed')

class LibraryDemo:
    @staticmethod
    def run():
        library = Library("kitchener public library")
        libraryManager = LibraryManager(library)
        book1 = Book("little women", "catherine", 1)
        book2 = Book("little tiny house", "no name", 2)
        book3 = Book("kite runner", "ahmed", 3)
        book4 = Book("cracking the coding interview", "greta", 4)
        book5 = Book("system design", "alex wu", 5)
        library.addBook(book1)
        library.addBook(book2)
        library.addBook(book3)
        library.addBook(book4)
        library.addBook(book5)
        library.removeBook(book4)
        library.getAllBooks()
        customer1 = Customer("kavya", "kay@gmail.com")
        customer2 = Customer("arvind", "arvi@gmail.com")
        customer3 = Customer("veena", "vina@gmail.com")
        libraryManager.addCustomer(customer1)
        libraryManager.addCustomer(customer2)
        libraryManager.removeCustomer(customer3)
        libraryManager.addCustomer(customer3)
        libraryManager.removeCustomer(customer3)
        libraryManager.borrowBook(book1, customer1)
        libraryManager.borrowBook(book2, customer2)
        libraryManager.borrowBook(book5, customer1)
        libraryManager.returnBook(book1, customer1)
        libraryManager.borrowBook(book3, customer1)
        libraryManager.getAllBooksBorrowedByCustomer(customer1)



if __name__=="__main__":
    LibraryDemo.run()
