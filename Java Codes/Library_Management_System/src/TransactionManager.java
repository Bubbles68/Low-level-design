public class TransactionManager {

    // Borrow a book
    public void borrowBook(User user, Book book) {
        if (book == null || user == null) {
            System.out.println("Invalid book or user.");
            return;
        }
        if (book.getBookStatus() == BookStatus.AVAILABLE) {
            book.setBookStatus(BookStatus.UNAVAILABLE);
            user.borrowBook(book);
            System.out.println(user.getName() + " borrowed " + book.getTitle() + " successfully.");
        } else {
            System.out.println("Book is not available to borrow.");
        }
    }
    // Return a book
    public void returnBook(User user, Book book) {
        if (book == null || user == null) {
            System.out.println("Invalid book or user.");
            return;
        }

        if (user.getBorrowedBooks().contains(book)) {
            book.setBookStatus(BookStatus.AVAILABLE);
            user.returnBook(book);
            System.out.println(user.getName() + " returned " + book.getTitle() + " successfully.");
        } else {
            System.out.println("This book was not borrowed by " + user.getName() + ".");
        }
    }
}