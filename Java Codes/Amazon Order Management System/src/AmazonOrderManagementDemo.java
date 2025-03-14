/*
for amazon order management
FUNCTIONAL REQUIREMENTS:
    -Create an Order
    -Cancel an Order
    -Track Order Status
    -Update Order Details
    -Process Payment
    -Manage Inventory
    -Generate Invoice
ENTITIES and METHODS:
    - User:
        -Attributes: user id, name, email
        -Methods: addProductToCart, removeProductFromCart
    - Product:
        -Attributes: productId, productName, productDescription, price, quantityInStock
        -Methods: getPrice, isAvailable
    - ProductCatalog:
        -Methods: searchProducts, getProductDetails
    - Cart:
        -Attributes: cartId, productsList, userId
        -Methods: getTotalPrice, addProduct, removeProduct, checkout
    - Order:
        -Attributes: orderId, userId, listOfProducts, orderDate, status, totalPrice
        -Methods: generateInvoice, getShipmentDate, cancelOrder()
    - Inventory Manager:
        -Attributes: ProductList List<Product>
        -Methods: getProducts, sendRestockRequest, addProducts, removeProducts, checkStock
    - Order manager:
        -Attributes: OrderLists List<Order>
        -Methods: createOrder, cancelOrder, trackOrder, processPayment
    - Payment Service:
        -Methods: processPayments, refundPayment

 */

import java.util.ArrayList;
import java.util.List;

class User{
    private String name;
    private String email;
    private String userId;
    private Cart cart;

    public User(String name, String email, String userId) {
        this.name = name;
        this.email = email;
        this.userId = userId;
        this.cart = new Cart();
    }

    public void addProductToCart(Product product) {
        cart.addProduct(product);
        System.out.println(product.getProductName() + " added to cart.");
    }

    public void removeProductFromCart(Product product) {
        cart.removeProduct(product);
        System.out.println(product.getProductName() + " removed from cart.");
    }

    public Cart getCart() {
        return cart;
    }
}

class Cart{
    private int cartId;
    private List<Product> productsList = new ArrayList<>();

    public void addProduct(Product product) {
        productsList.add(product);
    }

    public void removeProduct(Product product) {
        productsList.remove(product);
    }

    public double getTotalPrice() {
        return productsList.stream().mapToDouble(Product::getPrice).sum();
    }

    public void checkout() {
        System.out.println("Proceeding to checkout...");
    }

    public List<Product> getProducts() {
        return productsList;
    }
}

class Product{
    int productId;
    private String productName;
    private double price;
    private int quantityInStock;

    public Product(int productId, String productName, double price, int quantityInStock) {
        this.productId = productId;
        this.productName = productName;
        this.price = price;
        this.quantityInStock = quantityInStock;
    }

    public double getPrice() {
        return price;
    }

    public String getProductName() {
        return productName;
    }

    public boolean isAvailable() {
        return quantityInStock > 0;
    }
}

class Order{
    int orderId;
    private List<Product> productsList;
    double totalPrice;
    private String status;

    public Order(int orderId, List<Product> productsList, double totalPrice) {
        this.orderId = orderId;
        this.productsList = productsList;
        this.totalPrice = totalPrice;
        this.status = "Created";
    }

    public void generateInvoice() {
        System.out.println("Invoice generated for Order ID: " + orderId);
        productsList.forEach(p -> System.out.println(p.getProductName() + ": $" + p.getPrice()));
        System.out.println("Total Price: $" + totalPrice);
    }

    public void cancelOrder() {
        status = "Cancelled";
        System.out.println("Order ID: " + orderId + " has been cancelled.");
    }

    public String getStatus() {
        return status;
    }
}

class InventoryManager{
    private List<Product> productList;

    public InventoryManager(List<Product> productList) {
        this.productList = productList;
    }

    public Product getProduct(int productId) {
        return productList.stream().filter(p -> p.productId == productId).findFirst().orElse(null);
    }

    public boolean checkStock(int productId) {
        Product p = getProduct(productId);
        return p != null && p.isAvailable();
    }

    public void restockProduct(int productId, int quantity) {
        Product p = getProduct(productId);
        if (p != null) {
            System.out.println("Restocking " + quantity + " units of " + p.getProductName());
            // Assuming this adds to the stock
        }
    }
}

class OrderManager {
    private List<Order> orderList;

    public OrderManager() {
        this.orderList = new ArrayList<>();
    }

    public Order createOrder(Cart cart) {
        int orderId = orderList.size() + 1; // Simple way to generate order IDs
        Order order = new Order(orderId, cart.getProducts(), cart.getTotalPrice());
        orderList.add(order);
        System.out.println("Order ID: " + orderId + " created.");
        return order;
    }

    public void cancelOrder(Order order) {
        order.cancelOrder();
    }

    public void trackOrder(int orderId) {
        Order order = orderList.stream().filter(o -> o.orderId == orderId).findFirst().orElse(null);
        if (order != null) {
            System.out.println("Order ID: " + orderId + " Status: " + order.getStatus());
        } else {
            System.out.println("Order not found.");
        }
    }
}

class PaymentService {
    public void processPayments(Order order) {
        System.out.println("Payment processed for Order ID: " + order.orderId + " with total: $" + order.totalPrice);
    }

    public void refundPayment(Order order) {
        System.out.println("Refund processed for Order ID: " + order.orderId);
    }
}

public class AmazonOrderManagementDemo {
    public static void main(String[] args) {
        // Sample product catalog
        List<Product> products = new ArrayList<>();
        products.add(new Product(1, "Laptop", 1000.00, 10));
        products.add(new Product(2, "Smartphone", 500.00, 5));
        products.add(new Product(3, "Headphones", 100.00, 3));

        // Inventory manager to check stock
        InventoryManager inventoryManager = new InventoryManager(products);

        // Creating users
        User user1 = new User("John Doe", "john@example.com", "U123");
        User user2 = new User("Jane Smith", "jane@example.com", "U124");

        // Adding products to user1's cart
        user1.addProductToCart(products.get(0)); // Adding Laptop
        user1.addProductToCart(products.get(1)); // Adding Smartphone

        // Checkout process
        Cart user1Cart = user1.getCart();
        user1Cart.checkout();

        // Create an order
        OrderManager orderManager = new OrderManager();
        Order order = orderManager.createOrder(user1Cart);

        // Generate invoice
        order.generateInvoice();

        // Process payment
        PaymentService paymentService = new PaymentService();
        paymentService.processPayments(order);

        // Track order
        orderManager.trackOrder(order.orderId);

        // Cancel order
        orderManager.cancelOrder(order);
        orderManager.trackOrder(order.orderId); // Check status after cancellation

        // Simulating restocking
        inventoryManager.restockProduct(2, 5); // Restocking 5 units of Smartphone
    }
}
