import java.time.LocalDateTime;

public class Review {
    public Long id;
    public String content;
    public Product product;
    public Rating rating;
    LocalDateTime createdAt;
}
