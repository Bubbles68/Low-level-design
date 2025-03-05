'''
Entities:
Pizza - base, sauce, toppings, addToppings, removeToppings, getPrice
order - orderId, userId, List<Pizza>
User - userId, email, paymentType
paymentType - enum - credit, debit, apple pay
Order management system - map<order, user>, addPizzaToOrder, removePizzaFromOrder, placeAnOrder, OrderEsimatedTime
'''

from collections import defaultdict
from enum import Enum
import uuid

class PaymentType(Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    APPLE_PAY = "apple_pay"

class Pizza:
    BASE_PRICE = 10
    SAUCE_PRICE = 2
    TOPPING_PRICE = 1

    def __init__(self, name):
        self.name = name
        self._toppings = set()

    def addToppings(self, topping):
        if not isinstance(topping, str):
            raise ValueError("Topping must be a string")
        self._toppings.add(topping)

    def removeToppings(self, topping):
        self._toppings.discard(topping)

    def getPrice(self):
        total = self.BASE_PRICE + self.SAUCE_PRICE + (len(self._toppings) * self.TOPPING_PRICE)
        return total
    
class PepperoniPizza(Pizza):
    PREMIUM_MULTIPLIER = 1.5

    def getPrice(self):
        return super().getPrice() * self.PREMIUM_MULTIPLIER 

class User:
    def __init__(self, name, userId, email, payment_type=PaymentType.CREDIT):
        self._name = name
        self._userId = userId
        self._email = email
        self._payment_type = payment_type if isinstance(payment_type, PaymentType) else PaymentType.CREDIT

    def get_name(self):
        return self._name

    def get_userId(self):
        return self._userId

    def get_email(self):
        return self._email

    def get_payment_type(self):
        return self._payment_type

class Order:
    PREP_TIME_PER_PIZZA = 10

    def __init__(self, orderId, userId):
        self.orderId = orderId
        self.userId = userId
        self.pizzas = defaultdict(int)

    def addPizzaToOrder(self, pizza):
        self.pizzas[pizza]+=1
    
    def removePizzaFromOrder(self, pizza):
        if pizza in self.pizzas:
            self.pizzas[pizza]-=1
            if self.pizzas[pizza]==0:
                del self.pizzas[pizza]
        else:
            raise ValueError(f"cant remove pizza from order, as its not in the cart")
        
    def getTotalPriceOfOrder(self):
        totalPrice = 0 
        if self.pizzas is not None:
            for pizza, count in self.pizzas.items():
                totalPrice += pizza.getPrice()*count
            return totalPrice
        else:
            print("Price is 0, ntng in the cart")
            return 0
    
    def getEstimatedTime(self):
        total_pizzas = sum(self.pizzas.values())
        minutes=self.PREP_TIME_PER_PIZZA *total_pizzas 
        print(f"Preparing your Order...... Order will be ready in {minutes} minutes")
        return minutes

class OrderManagementSystem:
    def __init__(self):
        self.orderUserMap = {}

    def createOrderForUser(self, user, pizza):
        if user not in self.orderUserMap:
            orderId = self.generateUniqueOrderId()
            self.orderUserMap[user] = Order(orderId, user.get_userId())
        self.orderUserMap[user].addPizzaToOrder(pizza)
        return self.orderUserMap[user].orderId
    
    def addPizzaToOrder(self, user, pizza):
        if user not in self.orderUserMap:
            raise ValueError("No existing order for user")
        self.orderUserMap[user].addPizzaToOrder(pizza)

    def removePizzaFromOrder(self, user, pizza):
        if user not in self.orderUserMap:
            raise ValueError("No existing order for user")
        self.orderUserMap[user].removePizzaFromOrder(pizza)

    def placeAnOrder(self, user):
        if user not in self.orderUserMap:
            raise ValueError("No order to place")
        order = self.orderUserMap[user]
        total_price = order.getTotalPriceOfOrder()
        estimated_time = order.getEstimatedTime()
        print(f"Order {order.orderId} placed for {user.get_name()}: ${total_price:.2f}, "
              f"Estimated delivery in : {estimated_time} minutes")
        del self.orderUserMap[user]  # Clear order after placement
        return order.orderId

    def getTotalPriceForCheckout(self, user):
        if user not in self.orderUserMap:
            raise ValueError(f"cant get price as user didnt add anything to cart")
        else:
            order = self.orderUserMap[user]
            totalPrice = order.getTotalPriceOfOrder()
            print(f"total price of order is {totalPrice} , placed by User {user.get_name()}")
            return totalPrice

    def generateUniqueOrderId(self):
        return uuid.uuid4()

class PizzaOrderDemo:
    @staticmethod
    def run():
        pizza1 = Pizza("Mexican Wave")
        pizza1.addToppings("jalapenos")
        pizza2 = Pizza("Double Cheese")
        pizza3 = PepperoniPizza("Pepperoni")

        user1 = User("kavya", 123, "kay@gmail.com")
        user2 = User("arvind",345, "arvi@gmail,com")

        orderManager = OrderManagementSystem()
        orderManager.createOrderForUser(user1, pizza1)
        orderManager.addPizzaToOrder(user1, pizza3)
        print(f"User 1 checkout price: ${orderManager.getTotalPriceForCheckout(user1):.2f}")
        orderManager.placeAnOrder(user1)

        # User 2 orders
        orderManager.createOrderForUser(user2, pizza2)
        print(f"User 2 checkout price: ${orderManager.getTotalPriceForCheckout(user2):.2f}")
        orderManager.placeAnOrder(user2)

if __name__=="__main__":
    PizzaOrderDemo.run()







       
