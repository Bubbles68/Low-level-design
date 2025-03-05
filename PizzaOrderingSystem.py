'''
Entities:
Pizza - base, sauce, toppings, addToppings, removeToppings, getPrice
order - orderId, userId, List<Pizza>
User - userId, email, paymentType
paymentType - enum - credit, debit, apple pay
Order management system - map<order, user>, addPizzaToOrder, removePizzaFromOrder, placeAnOrder, OrderEsimatedTime
'''

from collections import defaultdict
import uuid


class Pizza:
    def __init__(self, name):
        self.name = name
        self.toppings = 0
        self.price = 0

    def getPrice(self):
        totalPrice = 0
        basePrice = 10
        saucePrice = 2
        toppingPrice = 1
        totalPrice+=(basePrice+saucePrice+(toppingPrice*self.toppings))
        print(f"{self.name} Pizza price is {totalPrice}")
        return totalPrice

class PepporoniPizza(Pizza):
    def getPrice(self):
        self.price * 1.5

class User:
    def __init__(self, name, userId, emailId):
        self.name = name
        self.userId = userId
        self.emailId = emailId

class Order:
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

class OrderManagementSystem:
    def __init__(self):
        self.orderUserMap = {}

    def createOrderForUser(self, user, pizza):
        if user in self.orderUserMap:
            order = self.orderUserMap[user]
        else:
            orderId = self.generateUniqueOrderId()
            order = Order(orderId, user.userId)
            self.orderUserMap[user]=order
        order.addPizzaToOrder(pizza)
        print(f"Order created and {pizza.name} pizza added to the order")

    def getTotalPriceForCheckout(self, user):
        if user not in self.orderUserMap:
            raise ValueError(f"cant get price as user didnt add anything to cart")
        else:
            order = self.orderUserMap[user]
            totalPrice = order.getTotalPriceOfOrder()
            print(f"total price of order is {totalPrice} , placed by User {user.name}")
            return totalPrice

    def generateUniqueOrderId(self):
        return uuid.uuid4()

class PizzaOrderDemo:
    @staticmethod
    def run():
        pizza1 = Pizza("mexican wave")
        pizza2 = Pizza("double cheese")
        pizza3 = Pizza("pepporoni")
        pizza4 = Pizza("jalapeno chicken")
        pizza5 = Pizza("Hawaiian")

        user1 = User("kavya", 123, "kay@gmail.com")
        user2 = User("arvind",345, "arvi@gmail,com")

        orderManager = OrderManagementSystem()
        orderManager.createOrderForUser(user1, pizza1)
        orderManager.createOrderForUser(user2, pizza2)
        orderManager.createOrderForUser(user1, pizza3)
        
        orderManager.getTotalPriceForCheckout(user1)
        orderManager.getTotalPriceForCheckout(user2)

if __name__=="__main__":
    PizzaOrderDemo.run()







       
