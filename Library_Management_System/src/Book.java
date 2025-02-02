public class Book {
    private String id;
    private String title;
    private String author;
    private BookStatus bookStatus;

    public String getTitle() {
        return title;
    }

    public BookStatus getBookStatus() {
        return bookStatus;
    }

    public void setBookStatus(BookStatus bookStatus) {
        this.bookStatus = bookStatus;
    }

    @Override
    public String toString() {
        return "Book{" +
                "id='" + id + '\'' +
                ", title='" + title + '\'' +
                ", author='" + author + '\'' +
                ", bookStatus=" + bookStatus +
                '}';
    }

    public Book(String id, String title, String author) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.bookStatus = BookStatus.AVAILABLE;
    }
}


