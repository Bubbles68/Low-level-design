import java.util.*;

public class User {
    String name;
    String id;
    List<Review> reviews;

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<Review> getReviews() {
        return reviews;
    }

    public User(List<Review> reviews, String name, String id) {
        this.reviews = new ArrayList<>();
        this.name = name;
        this.id = id;
    }

    public void postReview(Review review){
        reviews.add(review);
    }
    public void deleteReview(Review review){
        reviews.remove(review);
    }
}
