# python -m unittest -v test.py
import unittest
from models import *
from config import *


class PriceTest(unittest.TestCase):
    """Price tests"""

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        cls.s = XMLPriceList(svrauto, 'car_tires')
        cls.p = XMLPriceList(pwrs, 'car_tires')
        cls.t = XMLPriceList(trektyre, 'car_tires_for_order')
        cls.b = XLSPriceList(sak, 'batteries')

        sp = cls.s.extract_next_product_parameters()
        pp = cls.p.extract_next_product_parameters()
        tp = cls.t.extract_next_product_parameters()
        bp = cls.b.extract_next_product_parameters()

        cls.so = CarTire(**sp)
        cls.po = CarTire(**pp)
        cls.to = CarTire(**tp)
        cls.bo = Battery(**bp)

        print("Test has been started")
        print("====================")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("====================")
        print("Test has been finished")

    def setUp(self):
        """Set up for test"""
        # print("Set up for [" + self.shortDescription() + "]")

    def tearDown(self):
        """Tear down for test"""

    def test_level(self):
        """Trying to get nesting levels"""
        self.assertEqual(self.s._get_nesting_level()[0], 2)
        self.assertEqual(self.p._get_nesting_level()[0], 1)
        self.assertEqual(self.t._get_nesting_level()[0], 1)

    def test_product_element(self):
        """Trying to get product elements"""
        sg = self.s._generate_product()
        pg = self.p._generate_product()
        tg = self.t._generate_product()
        bg = self.b._sak_generate_product()

        self.assertEqual(next(sg).tag, 'COMMODITY')
        self.assertEqual(next(pg).tag, 'tires')
        self.assertEqual(next(tg).tag, 'product')
        self.assertIsInstance(next(bg), dict)

    def test_create_product(self):
        """Trying to create product object"""
        self.assertIsNotNone(self.so.title)
        self.assertIsNotNone(self.po.title)
        self.assertIsNotNone(self.to.title)
        self.assertIsNotNone(self.bo.title)

    def test_add_to_db(self):
        """Trying to make a record"""
        db.session.add(self.so)
        db.session.add(self.po)
        db.session.add(self.to)
        db.session.add(self.bo)
        try:
            db.session.commit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()
