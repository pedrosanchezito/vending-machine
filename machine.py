from enum import Enum

class Rack:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = 0

class Machine:
    def __init__(self, racks):
        self.amount = 0
        self.racks = {}
        for rack in racks:
            self.racks[rack.code]= rack
        self.coins = {}
        for coin in Coin:
            self.coins[coin] = 0

    def refill(self, code, quantity):
        self.racks[code].quantity += quantity

    def insertCoin(self, coin):
        self.coins[coin] += 1
        self.amount += coin.value

    def pressButton(self, code):
        rack = self.racks[code]
        if rack.price <= self.amount:
            rack.quantity -= 1
            self.amount -= rack.price

class Coin(Enum):
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100
