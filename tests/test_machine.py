import unittest
from machine import Rack, Machine, Coin

class MachineTest(unittest.TestCase):
    def test_can_refill_biscuits(self):
        racks = [ Rack("A", "Biscuits", 100) ]
        machine = Machine(racks)
        machine.refill("A", 5)

        # machine.racks: A => Rack, B => Rack
        self.assertEqual(machine.racks["A"].quantity, 5)

    def test_can_refill_several_times(self):
        racks = [ Rack("A", "Biscuits", 100) ]
        machine = Machine(racks)
        machine.refill("A", 5)
        machine.refill("A", 7)

        # machine.racks: A => Rack, B => Rack
        self.assertEqual(machine.racks["A"].quantity, 12)

    def test_user_can_buy_item_A(self):
        racks = [ Rack("A", "Biscuits", 100) ]
        machine = Machine(racks)
        machine.refill("A", 1)
        machine.insertCoin(Coin.DOLLAR)
        machine.pressButton("A")

        self.assertEqual(machine.racks["A"].quantity, 0)
        self.assertEqual(machine.coins[Coin.DOLLAR], 1)

    def test_user_cant_buy_item_A(self):
        racks = [ Rack("A", "Biscuits", 100) ]
        machine = Machine(racks)
        machine.refill("A", 1)
        machine.insertCoin(Coin.QUARTER)
        machine.insertCoin(Coin.QUARTER)
        machine.pressButton("A")

        self.assertEqual(machine.racks["A"].quantity, 1)
        self.assertEqual(machine.coins[Coin.QUARTER], 2)

    def test_user_can_buy_item_A_with_too_much_money(self):
        racks = [ Rack("A", "Biscuits", 100) ]
        machine = Machine(racks)
        machine.refill("A", 1)
        machine.insertCoin(Coin.QUARTER)
        machine.insertCoin(Coin.QUARTER)
        machine.insertCoin(Coin.QUARTER)
        machine.insertCoin(Coin.QUARTER)
        machine.insertCoin(Coin.QUARTER)
        machine.pressButton("A")

        self.assertEqual(machine.racks["A"].quantity, 0)
        self.assertEqual(machine.coins[Coin.QUARTER], 4)
        self.assertEqual(machine.amount, 0)

    def test_change_return_after_purchase(self):
        racks = [ Rack("A", "Biscuits", 100) ]
        machine = Machine(racks)
        machine.refill("A", 1)

        for i in range(5):
            machine.insertCoin(Coin.QUARTER)

        machine.pressButton("A")
        self.assertEqual(machine.coins[Coin.QUARTER], 4)

    def test_change_return_after_purchase_shuffle(self):
        racks = [ Rack("A", "Biscuits", 100) ]
        machine = Machine(racks)
        machine.refill("A", 1)

        for i in range(5):
            machine.insertCoin(Coin.DIME)

        machine.insertCoin(Coin.NICKEL)

        for i in range(3):
            machine.insertCoin(Coin.QUARTER)

        machine.pressButton("A")
        self.assertEqual(machine.coins[Coin.DIME], 3)
        self.assertEqual(machine.coins[Coin.NICKEL], 0)
        self.assertEqual(machine.coins[Coin.QUARTER], 3)

    def test_change_return_after_purchase_no_exact_change(self):
        racks = [ Rack("A", "Biscuits", 100) ]
        machine = Machine(racks)
        machine.refill("A", 1)

        for i in range(8):
            machine.insertCoin(Coin.DIME)

        machine.insertCoin(Coin.QUARTER)

        machine.pressButton("A")
        self.assertEqual(machine.coins[Coin.DIME], 8)
        self.assertEqual(machine.coins[Coin.QUARTER], 1)
