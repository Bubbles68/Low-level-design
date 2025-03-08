'''
Command: has an (action) to do on a (target)
Rule: input is a {list of words}, determines if the rule can be matched
Processor : which has the {list of devices} and the allowed [commands]
'''

from abc import ABC, abstractmethod


class Command:
    def __init__(self, action, target):
        self.action = action
        self.target = target
    
    def __str__(self):
        return f"Action {self.action} performed on {self.target}"
        
class Rule(ABC):
    @abstractmethod
    def match(self):
        pass

class TurnOnOffRule(Rule):
    listOfActions = {"on", "off"}
    def match(self, words, validDevices):
        if len(words)<3:
            return None
        else:
            if words[0].lower() == "turn" and words[1].lower() in self.listOfActions and words[-1].lower() in validDevices:
                return Command(words[0]+" "+words[1], words[-1])
            else:
                return None

class Processor:
    def __init__(self):
        self.validDevices = {"fans", "lights"}
        self.allowedRules = [TurnOnOffRule()]#can add more rules here for later

    def process(self, input_str):
        words = input_str.split(" ")
        command = None
        for rule in self.allowedRules:
            command = rule.match(words, self.validDevices)
            if command is not None:
                print(f"Command processed successfully : {command}")
        if command is None:
            print("command didnt match")

class Demo:
    def run():
        processor = Processor()
        input1 = "Turn on Fans"
        input2 = "Turn on Kitchen lights"

        processor.process(input1)
        processor.process(input2)

if __name__ == "__main__":
    Demo.run()
