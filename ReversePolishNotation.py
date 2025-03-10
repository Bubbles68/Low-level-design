
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
        return operand2 - operand1
    
class Multiplication(Operator):
    def apply(self, operand1, operand2):
        return operand1 * operand2

class Division(Operator):
    def apply(self, operand1, operand2):
        if operand2 == 0:
            raise ValueError("Division by zero")
        return operand1 / operand2 
    
class OperatorRegistry:
    def __init__(self):
        self.operators = {}

    def registerNewOperator(self, symbol:str, operator:Operator):
        self.operators[symbol]=operator

    def getOperator(self, symbol):
        return self.operators[symbol]
    
class Evaluator:
    def __init__(self, operatorRegistry: OperatorRegistry):
        self.operatorRegistry = operatorRegistry
    
    def evaluate(self, expression: str):
        stack = []
        tokens = expression.split()
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            else:
                operator = self.operatorRegistry.getOperator(token)
                if operator:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    result = operator.apply(operand1, operand2)
                    stack.append(result)
                else:
                    raise ValueError(f"Unknown operator: {token}")
        if len(stack) == 1:
            return stack[0]
        else:
            raise ValueError("Invalid RPN expression")
        
if __name__ == "__main__":
    # Create an operator registry and register default operators
    registry = OperatorRegistry()
    registry.registerNewOperator('+', Addition())
    registry.registerNewOperator('-', Subtraction())
    registry.registerNewOperator('*', Multiplication())
    registry.registerNewOperator('/', Division())

    # Create the RPN calculator
    calculator = Evaluator(registry)

    # Example RPN expression: "3 4 + 2 *"
    rpn_expression = "3 4 + 2 *"
    result = calculator.evaluate(rpn_expression)
    print(f"Result: {result}")  # Expected Output: 14.0


    # Example of adding a new operator (e.g., power)
    class Power(Operator):
        def apply(self, operand1: float, operand2: float) -> float:
            return operand1 ** operand2

    # Register the new operator and use it
    registry.registerNewOperator('^', Power())
    rpn_expression_with_new_operator = "2 3 ^"
    result = calculator.evaluate(rpn_expression_with_new_operator)
    print(f"Result: {result}")  # Expected Output: 8.0