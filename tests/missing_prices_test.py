__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import unittest
import beancount_portfolio_allocation.loader as loader
from beancount.core.data import Decimal
from testfixtures import log_capture


class TestMissingPricesReport(unittest.TestCase):
    @log_capture()
    def setUp(self, capture):
        self.maxDiff = None
        self.file = "tests/test_inputs/missing_prices.beancount"
        self.portfolio = "pension"
        (self.targets, self.allocations,
            self.total) = loader.load(self.file, self.portfolio)
        self.capture = capture

    def test_missing_price_error_message(self):
        self.capture.check(
            ('root',
             'ERROR',
             'Could not get a value for currency AAPL in account Assets:Pension. Using 0. Are you missing a price directive?')
        )

    def test_missing_price_cash_value(self):
        value = self.allocations.value_for_class_subclass("cash", "cash")

        self.assertEqual(value, 0)

    def test_missing_price_equity_value(self):
        value = self.allocations.value_for_class_subclass("equity", "usa")

        self.assertEqual(value, 0)

    def test_missing_price_total_invested(self):
        total = self.allocations.total_invested_for_portfolio()

        self.assertEqual(total, Decimal('24.4495'))
