from abc import ABC, abstractmethod


class Operator(ABC):
    @abstractmethod
    def apply(self, operand1, operand2):
        pass

class Addition(Operator):
    def apply(self, operand1, operand2):
        return operand1 + operand2
    
class Subtraction(Operator):
    def apply(self, operand1, operand2):
        return operand1 - operand2  

class Multiplication(Operator):
    def apply(self, operand1, operand2):
        return operand1 * operand2

class Division(Operator):
    def apply(self, operand1, operand2):
        if operand2 == 0:
            raise ValueError("Division by zero")
        return operand1 // operand2  # Integer division to match normal calculator behavior

class OperatorRegistry:
    def __init__(self):
        self.operators = {'+': Addition(),
                          '-': Subtraction(),
                          '*': Multiplication(),
                          '/': Division()}

    def registerNewOperator(self, symbol: str, operator: Operator):
        self.operators[symbol] = operator

    def getOperator(self, symbol):
        return self.operators.get(symbol, None)

class Evaluator:
    def __init__(self, operatorRegistry: OperatorRegistry):
        self.operatorRegistry = operatorRegistry
    
    def calculate(self, expression: str) -> int:
        num, stack, presign = 0, [], "+"
        for i, char in enumerate(expression):
            if char.isdigit():
                num = num * 10 + int(char)
            if i == len(expression) - 1 or char in self.operatorRegistry.operators:
                operation = self.operatorRegistry.getOperator(presign)  
                if operation:
                    if presign in "+-":
                        stack.append(operation.apply(0, num))  # Using 0 to simulate unary addition/subtraction
                    else:
                        stack.append(operation.apply(stack.pop(), num))
                presign = char
                num = 0
        return sum(stack)
    
if __name__ == "__main__":
    registry = OperatorRegistry()
    calculator = Evaluator(registry)
    print(calculator.calculate("3+5*2-8/4"))
