# python -m unittest -v test.py
import unittest
from models import PriceList, PriceHandler
from config import *


s = PriceList(svrauto, 'car_tires')
p = PriceList(pwrs, 'car_tires')
t = PriceList(trektyre, 'car_tires_for_order')

sh = PriceHandler(s)
ph = PriceHandler(p)
th = PriceHandler(t)

sg = sh.generate_product()
pg = ph.generate_product()
tg = th.generate_product()


class PriceTest(unittest.TestCase):
    """Calc tests"""

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("Test has been started")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("Test has been finished")

    def setUp(self):
        """Set up for test"""
        # print("Set up for [" + self.shortDescription() + "]")

    def tearDown(self):
        """Tear down for test"""

    def test_level(self):
        """Trying to get nesting levels"""
        self.assertEqual(s.get_nesting_level()[0], 2)
        self.assertEqual(p.get_nesting_level()[0], 1)
        self.assertEqual(t.get_nesting_level()[0], 1)

    def test_product_element(self):
        """Trying to get product elements"""
        self.assertEqual(next(sg).tag, 'COMMODITY')
        self.assertEqual(next(pg).tag, 'tires')
        self.assertEqual(next(tg).tag, 'product')


if __name__ == '__main__':
    unittest.main()
