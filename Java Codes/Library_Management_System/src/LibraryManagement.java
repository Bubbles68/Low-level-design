import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class LibraryManagement {

    private static LibraryManagement instance;
    private Map<String, Book> books;

    public LibraryManagement() {
        this.books = new HashMap<>();
    }

    public static LibraryManagement getInstance() {
        if (instance == null) {
            instance = new LibraryManagement();
        }
        return instance;
    }
    public void addBook(Book book){
        books.put(book.getTitle(), book);
        System.out.println("successfully added book to our library: "+book.getTitle());
    }
    public void removeBook(String bookId) {
        Book book = books.remove(bookId);
        if (book != null) {
            System.out.println("Successfully removed book: " + book.getTitle());
        } else {
            System.out.println("Book not found.");
        }
    }
    public Book searchForBook(String title){
        for (Book book : books.values()) {
            if (book.getTitle().equalsIgnoreCase(title)) {
                return book;
            }
        }
        return null;
    }
    public void displayAllBooksWithStatus(){
        for (Book book : books.values()) {
            System.out.println(book.getTitle() + " - " + book.getBookStatus());
        }
    }
    public Book getBook(String bookId) {
        return books.get(bookId);
    }
}
