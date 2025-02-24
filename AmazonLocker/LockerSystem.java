import java.util.*;
import java.util.concurrent.locks.ReentrantLock;

enum Size {
    SMALL(1), MEDIUM(2), LARGE(3);
    private final int value;
    Size(int value) { this.value = value; }
    public int getValue() { return value; }
}

class Package {
    private int id;
    private Size size;
    private int code;

    public Package(int id, Size size) {
        this.id = id;
        this.size = size;
        this.code = new Random().nextInt(9000) + 1000; // Random for scale
    }

    public int getId() { return id; }
    public Size getSize() { return size; }
    public int getCode() { return code; }
}

class Locker {
    private Size size;
    private int id;
    private Package packageInLocker;
    private ReentrantLock lock = new ReentrantLock();

    public Locker(Size size, int id) {
        this.size = size;
        this.id = id;
        this.packageInLocker = null;
    }

    public boolean assignPackage(Package pkg) {
        lock.lock();
        try {
            if (packageInLocker != null || pkg.getSize().getValue() > size.getValue()) {
                return false;
            }
            packageInLocker = pkg;
            return true;
        } finally {
            lock.unlock();
        }
    }

    public Package pickUpPackage(int code) {
        lock.lock();
        try {
            if (packageInLocker != null && packageInLocker.getCode() == code) {
                Package pkg = packageInLocker;
                packageInLocker = null;
                return pkg;
            }
            return null;
        } finally {
            lock.unlock();
        }
    }

    public int getId() { return id; }
}

class LockerSystem {
    private Map<Integer, Locker> lockers;

    public LockerSystem(List<Locker> lockerList) {
        this.lockers = new HashMap<>();
        for (Locker locker : lockerList) {
            lockers.put(locker.getId(), locker);
        }
    }

    public int assignPackage(Package pkg) {
        // Try lockers in order (could optimize with size buckets)
        for (Locker locker : lockers.values()) {
            if (locker.assignPackage(pkg)) {
                return pkg.getCode();
            }
        }
        return -1; // Failure
    }

    public Package pickUpPackage(int code, int id) {
        Locker locker = lockers.get(id);
        if (locker != null) {
            return locker.pickUpPackage(code);
        }
        return null;
    }
}
class LockerSystemDemo {
    public static void main(String[] args) {
        List<Locker> lockers = new ArrayList<>();
        lockers.add(new Locker(Size.SMALL, 1));
        lockers.add(new Locker(Size.MEDIUM, 2));
        LockerSystem system = new LockerSystem(lockers);
        try {
            Package pkg = new Package(1, Size.SMALL);
            int code = system.assignPackage(pkg);
            System.out.println("Assigned P1, Code: " + code);
            Package picked = system.pickUpPackage(code, 1);
            System.out.println("Picked: " + (picked != null ? "P" + picked.getId() : "Failed"));
        } catch (RuntimeException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}