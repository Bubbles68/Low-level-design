import java.util.List;

public class LibraryDemo {
    public static void main(String[] args){
        // Get singleton instances
        LibraryManagement library = LibraryManagement.getInstance();
        UserManagement userManagement = new UserManagement();
        TransactionManager transactionManager = new TransactionManager();


        Book book1= new Book("257","how to prepare well for LLD","kavya");
        Book book2= new Book("258","how to cheer up ur gf when she's upset","arvind");

        User user1 = new User("id1","sathya");
        User user2 = new User("id2", "sudha");

        library.addBook(book1);
        library.addBook(book2);
        userManagement.addUser(user1);
        userManagement.addUser(user2);

        library.displayAllBooksWithStatus();

        transactionManager.borrowBook(user1, book1);
        transactionManager.borrowBook(user2, book1);

        library.searchForBook("how to forgive stupid people");

        library.displayAllBooksWithStatus();

        transactionManager.returnBook(user1, book1);
        transactionManager.borrowBook(user2, book1);
        transactionManager.borrowBook(user2, book2);

        userManagement.removeUser(user2.getId());

        List<Book> books = user2.getBorrowedBooks();
        for(Book book:books){
            System.out.println(book.toString());
        }
    }
}
