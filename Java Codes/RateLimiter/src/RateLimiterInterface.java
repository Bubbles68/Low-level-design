import java.util.Deque;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.concurrent.locks.ReentrantLock;

interface RequestTracker {
    boolean allow(int limit, long window);
    int getRequestCount();
}

class SlidingWindowTracker implements RequestTracker {
    private Deque<Long> timestamps;
    private ReentrantLock lock;

    public SlidingWindowTracker() {
        this.timestamps = new LinkedList<>();
        this.lock = new ReentrantLock();
    }

    @Override
    public boolean allow(int limit, long window) {
        lock.lock();
        try {
            long now = System.currentTimeMillis();
            // Prune old timestamps (O(1) with Deque)
            while (!timestamps.isEmpty() && now - timestamps.peekFirst() > window) {
                timestamps.pollFirst();
            }
            if (timestamps.size() < limit) {
                timestamps.add(now);
                return true;
            }
            return false;
        } finally {
            lock.unlock();
        }
    }

    // For testing/debugging
    public int getRequestCount() {
        lock.lock();
        try {
            return timestamps.size();
        } finally {
            lock.unlock();
        }
    }
}

class RateLimiter {
    private Map<String, RequestTracker> users;
    private final int limit;
    private final long window;

    public RateLimiter(int limit, long window) {
        this.users = new HashMap<>();
        this.limit = limit;
        this.window = window;
    }

    public boolean allowRequest(String userId) throws IllegalArgumentException {
        if (userId == null || userId.isEmpty()) {
            throw new IllegalArgumentException("Invalid user ID");
        }
        RequestTracker tracker;
        synchronized (users) {
            tracker = users.computeIfAbsent(userId, k -> new SlidingWindowTracker());
        }
        boolean allowed = tracker.allow(limit, window);
        // Simulate logging
        System.out.println("User " + userId + ": " + (allowed ? "Allowed" : "Blocked"));
        return allowed;
    }

    // Cleanup method (e.g., for memory management)
    public void clearExpiredUsers() {
        synchronized (users) {
            users.entrySet().removeIf(entry ->
                    entry.getValue().getRequestCount() == 0);
        }
    }
}

class RateLimiterDemo {
    public static void main(String[] args) {
        RateLimiter limiter = new RateLimiter(2, 1000); // 2 req/1s
        try {
            System.out.println("Req 1: " + limiter.allowRequest("alice")); // true
            System.out.println("Req 2: " + limiter.allowRequest("alice")); // true
            System.out.println("Req 3: " + limiter.allowRequest("alice")); // false
            Thread.sleep(1000);
            System.out.println("Req 4: " + limiter.allowRequest("alice")); // true
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}