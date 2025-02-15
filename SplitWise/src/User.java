import java.util.*;

public class User {
    private String name;
    private String emailId;
    private Set<String> groupIds; // Stores groups the user is part of
    private Map<String, Double> balances; // Key: userEmail, Value: Amount owed (+) or to pay (-)

    public User(String emailId, String name) {
        this.emailId = emailId;
        this.name = name;
        this.groupIds = new HashSet<>();
        this.balances = new HashMap<>();
    }

    public String getName() {
        return name;
    }

    public String getEmailId() {
        return emailId;
    }

    public Set<String> getGroupIds() {
        return groupIds;
    }

    public Map<String, Double> getBalances() {
        return balances;
    }

    public void addGroup(String groupId) {
        groupIds.add(groupId);
    }

    public void removeGroup(String groupId) {
        groupIds.remove(groupId);
    }

    public void updateBalance(String userEmail, double amount) {
        balances.put(userEmail, balances.getOrDefault(userEmail, 0.0) + amount);
    }
}

class Group {
    private String groupId;
    private String name;
    private Set<User> users;
    private List<Expense> expenses;

    public Group(String groupId, String name) {
        this.groupId = groupId;
        this.name = name;
        this.users = new HashSet<>();
        this.expenses = new ArrayList<>();
    }

    public String getGroupId() {
        return groupId;
    }

    public String getName() {
        return name;
    }

    public Set<User> getUsers() {
        return users;
    }

    public List<Expense> getExpenses() {
        return expenses;
    }

    public void addUser(User user) {
        users.add(user);
        user.addGroup(groupId);
    }

    public void removeUser(User user) {
        users.remove(user);
        user.removeGroup(groupId);
    }

    public void addExpense(Expense expense) {
        expenses.add(expense);
    }
}

class Expense {
    private String expenseId;
    private double amount;
    private User paidBy;
    private Map<User, Double> splitAmong;

    public Expense(String expenseId, double amount, User paidBy, Map<User, Double> splitAmong) {
        this.expenseId = expenseId;
        this.amount = amount;
        this.paidBy = paidBy;
        this.splitAmong = splitAmong;
    }

    public String getExpenseId() {
        return expenseId;
    }

    public double getAmount() {
        return amount;
    }

    public User getPaidBy() {
        return paidBy;
    }

    public Map<User, Double> getSplitAmong() {
        return splitAmong;
    }
}

// Handles login/logout operations
class AuthService {
    private Map<String, User> usersDB = new HashMap<>();

    public User login(String emailId, String name) {
        return usersDB.computeIfAbsent(emailId, id -> new User(emailId, name));
    }
}

// Manages groups
class GroupService {
    private Map<String, Group> groupDB = new HashMap<>();

    public Group createGroup(String groupId, String name) {
        Group group = new Group(groupId, name);
        groupDB.put(groupId, group);
        return group;
    }

    public void addUserToGroup(String groupId, User user) {
        Group group = groupDB.get(groupId);
        if (group != null) {
            group.addUser(user);
        }
    }

    public void removeUserFromGroup(String groupId, User user) {
        Group group = groupDB.get(groupId);
        if (group != null) {
            group.removeUser(user);
        }
    }
}

// Manages expenses
class ExpenseService {
    public void addExpense(Group group, User paidBy, double amount, Map<User, Double> splitAmong) {
        Expense expense = new Expense(UUID.randomUUID().toString(), amount, paidBy, splitAmong);
        group.addExpense(expense);

        for (Map.Entry<User, Double> entry : splitAmong.entrySet()) {
            User user = entry.getKey();
            double share = entry.getValue();
            user.updateBalance(paidBy.getEmailId(), -share);
            paidBy.updateBalance(user.getEmailId(), share);
        }
    }
}

// Handles balance calculations
class BalanceService {
    public double getTotalAmountOwedToUser(User user) {
        return user.getBalances().values().stream().filter(amount -> amount > 0).mapToDouble(Double::doubleValue).sum();
    }

    public double getTotalAmountUserNeedsToPay(User user) {
        return user.getBalances().values().stream().filter(amount -> amount < 0).mapToDouble(Double::doubleValue).sum();
    }
}

// Demo Usage
class SplitwiseApp {
    public static void main(String[] args) {
        AuthService authService = new AuthService();
        GroupService groupService = new GroupService();
        ExpenseService expenseService = new ExpenseService();
        BalanceService balanceService = new BalanceService();

        // Users
        User alice = authService.login("alice@example.com", "Alice");
        User bob = authService.login("bob@example.com", "Bob");
        User charlie = authService.login("charlie@example.com", "Charlie");

        // Group Creation
        Group tripGroup = groupService.createGroup("grp-123", "Goa Trip");
        groupService.addUserToGroup("grp-123", alice);
        groupService.addUserToGroup("grp-123", bob);
        groupService.addUserToGroup("grp-123", charlie);

        // Adding an Expense (Alice paid $150, split equally among 3 users)
        Map<User, Double> split = new HashMap<>();
        split.put(alice, 50.0);
        split.put(bob, 50.0);
        split.put(charlie, 50.0);

        expenseService.addExpense(tripGroup, alice, 150.0, split);

        // Check balances
        System.out.println("Alice needs to be paid: " + balanceService.getTotalAmountOwedToUser(alice));
        System.out.println("Bob needs to pay: " + balanceService.getTotalAmountUserNeedsToPay(bob));
        System.out.println("Charlie needs to pay: " + balanceService.getTotalAmountUserNeedsToPay(charlie));
    }
}
