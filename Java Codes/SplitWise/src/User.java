import java.util.*;

class User {
    private String name;
    private String emailId;
    private Set<String> groupIds; // User can be in multiple groups

    public User(String emailId, String name) {
        this.emailId = emailId;
        this.name = name;
        this.groupIds = new HashSet<>();
    }

    public String getName() { return name; }
    public String getEmailId() { return emailId; }
    public Set<String> getGroupIds() { return groupIds; }

    public void joinGroup(String groupId) {
        groupIds.add(groupId);
    }

    public void leaveGroup(String groupId) {
        groupIds.remove(groupId);
    }
}

class Expense {
    private int amount;
    private String description;
    private String paidBy; // User ID of the payer
    private List<String> splitAmong; // List of users involved
    private Date timestamp;

    public Expense(int amount, String description, String paidBy, List<String> splitAmong) {
        this.amount = amount;
        this.description = description;
        this.paidBy = paidBy;
        this.splitAmong = splitAmong;
        this.timestamp = new Date();
    }

    public int getAmount() { return amount; }
    public String getDescription() { return description; }
    public String getPaidBy() { return paidBy; }
    public List<String> getSplitAmong() { return splitAmong; }
}

class Group {
    private String groupId;
    private String name;
    private Set<String> users; // Store user IDs
    private List<Expense> expenses;

    public Group(String groupId, String name) {
        this.groupId = groupId;
        this.name = name;
        this.users = new HashSet<>();
        this.expenses = new ArrayList<>();
    }

    public String getGroupId() { return groupId; }
    public String getName() { return name; }
    public Set<String> getUsers() { return users; }
    public List<Expense> getExpenses() { return expenses; }

    public void addUser(String userId) {
        users.add(userId);
    }

    public void removeUser(String userId) {
        users.remove(userId);
    }

    public void addExpense(Expense expense) {
        expenses.add(expense);
    }
}

class UserService {
    private Map<String, User> users = new HashMap<>();

    public void registerUser(String email, String name) {
        if (!users.containsKey(email)) {
            users.put(email, new User(email, name));
        }
    }

    public User getUser(String email) {
        return users.get(email);
    }
}

class GroupService {
    private Map<String, Group> groups = new HashMap<>();

    public void createGroup(String groupId, String name) {
        if (!groups.containsKey(groupId)) {
            groups.put(groupId, new Group(groupId, name));
        }
    }

    public void addUserToGroup(String groupId, String userId) {
        if (groups.containsKey(groupId)) {
            groups.get(groupId).addUser(userId);
        }
    }

    public void removeUserFromGroup(String groupId, String userId) {
        if (groups.containsKey(groupId)) {
            groups.get(groupId).removeUser(userId);
        }
    }

    public Group getGroup(String groupId) {
        return groups.get(groupId);
    }
}

class ExpenseService {
    private Map<String, Map<String, Integer>> balanceSheet = new HashMap<>();

    public void addExpense(String groupId, Expense expense) {
        for (String user : expense.getSplitAmong()) { //all users sharing the expense
            if (!user.equals(expense.getPaidBy())) { //Skip the payer because they don't owe money to themselves.
                balanceSheet.putIfAbsent(user, new HashMap<>());  //Ensure both users exist in balanceSheet.
                balanceSheet.putIfAbsent(expense.getPaidBy(), new HashMap<>()); //Ensure both users exist in balanceSheet.
                balanceSheet.get(user).put(expense.getPaidBy(),
                        balanceSheet.get(user).getOrDefault(expense.getPaidBy(), 0) + (expense.getAmount() / expense.getSplitAmong().size()));
                /*

                Update the debt of the current user (user) towards the payer (paidBy).
                The user owes an equal share of the expense:
                (Total Expense) ÷ (Total Users Splitting).  -- user who payed, gets money -- user who didnt, gets a minus
                 */
                balanceSheet.get(expense.getPaidBy()).put(user,
                        balanceSheet.get(expense.getPaidBy()).getOrDefault(user, 0) - (expense.getAmount() / expense.getSplitAmong().size()));
            }
        }
    }

    public Map<String, Integer> getUserBalance(String userId) {
        return balanceSheet.getOrDefault(userId, new HashMap<>());
    }
}

class ExpenseManagerApp {
    public static void main(String[] args) {
        UserService userService = new UserService();
        GroupService groupService = new GroupService();
        ExpenseService expenseService = new ExpenseService();

        userService.registerUser("alice@example.com", "Alice");
        userService.registerUser("bob@example.com", "Bob");

        groupService.createGroup("g1", "Friends");

        groupService.addUserToGroup("g1", "alice@example.com");
        groupService.addUserToGroup("g1", "bob@example.com");

        Expense expense = new Expense(100, "Dinner", "alice@example.com", Arrays.asList("alice@example.com", "bob@example.com"));
        expenseService.addExpense("g1", expense);

        System.out.println("Balance for Bob: " + expenseService.getUserBalance("bob@example.com"));
    }
}
