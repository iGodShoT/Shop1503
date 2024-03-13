from django.test import TestCase
from shop.utils import *

class CalculateMoneyDefTestCase(TestCase):

    def test_sum_price_count_pass(self):
        result = CalculateMoney().sum_price_count(price=100, count=10)
        self.assertEqual(1000, result)

    def test_sum_price_count_discount(self):
        result = CalculateMoney().sum_price_count(price=200, count=15, discount=5)
        self.assertEqual(2850, result)

class CalculateMoneyTestCase(TestCase, CalculateMoney):
    def test_sum_price_pass(self):
        prices = [294, 2000, 6942]
        result = self.sum_price(prices)
        self.assertEqual(9236, result)