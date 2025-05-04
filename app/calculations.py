def add(num1:int, num2: int):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

def multipy(num1: int, num2: int):
    return num1 * num2

def devide(num1: int, num2: int):
    return num1 / num2

class insufficent_funds(Exception):
    pass

class BankAccount():
    def __init__(self, startig_balance = 0):
        self.balance = startig_balance
    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise insufficent_funds("Insufficeint funds in account")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1