import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class UserManagement {
    private Map<String, User> users; // Store users by ID for efficient lookup

    public UserManagement() {
        this.users = new HashMap<>();
    }

    public void addUser(User user) {
        users.put(user.getId(), user);
        System.out.println("Successfully added user: " + user.getName());
    }

    public void removeUser(String userId) {
        User user = users.remove(userId);
        if (user != null) {
            System.out.println("Successfully removed user: " + user.getName());
        } else {
            System.out.println("User not found.");
        }
    }
    // Get a user by ID
    public User getUser(String userId) {
        return users.get(userId);
    }
}
