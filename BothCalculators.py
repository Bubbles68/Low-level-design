'''
operators
Registry
expression Evaluator
'''
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
        return int(operand1 / operand2)
    
class OperatorRegistry:
    def __init__(self):
        self.operations = {'+': Addition(), '-': Subtraction(), '*': Multiplication(), '/':Division()}
        
    def addNewOperator(self, symbol, operation):
        self.operations[symbol]=operation
        
    def getOperator(self, symbol):
        return self.operations[symbol]
    
class Evaluator:
    def __init__(self, registry):
        self.operatorRegistry = registry
    
    def evaluateCalculatorExpression(self, expression):
        stack = []
        num = 0
        presign = '+'
        for i, char in enumerate(expression):
            if char.isdigit():
                num = num*10 + int(char)
            if i==len(expression)-1 or char in self.operatorRegistry.operations:
                operator = self.operatorRegistry.getOperator(presign)
                if presign in '+-':
                    stack.append(operator.apply(0, num))
                else:
                    stack.append(operator.apply(stack.pop(), num))
                num=0
                presign = char
        return sum(stack)
    
    def evaluateRPNExpression(self, expression):
        stack = []
        expression = expression.split()
        for char in expression:
            if char.isdigit():
                stack.append(int(char))
            else:
                operator = self.operatorRegistry.getOperator(char)
                a = stack.pop()
                b = stack.pop()
                stack.append(operator.apply(a,b))
        return stack[0]

if __name__=="__main__":
    registry = OperatorRegistry()
    evaluator = Evaluator(registry)
    calcExpression = "3+2*5/2"
    rpnExpression = "3 2 + 5 *"
    print(evaluator.evaluateCalculatorExpression(calcExpression))
    print(evaluator.evaluateRPNExpression(rpnExpression))