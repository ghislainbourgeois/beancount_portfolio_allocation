__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import unittest
import beancount_portfolio_allocation.loader as loader
import beancount_portfolio_allocation.allocation_report as allocation_report
from beancount.core.data import Decimal
from testfixtures import log_capture


class TestMultiCurrencyMissingPricesReport(unittest.TestCase):
    @log_capture()
    def setUp(self, capture):
        self.maxDiff = None
        self.file = "tests/multicurrency-portfolio.beancount"
        self.portfolio = "pension"
        (self.targets, self.allocations,
            self.total) = loader.load(self.file, self.portfolio)
        capture.check(
                ('root', 'ERROR', 'Could not get a value for currency AAPL in account Assets:Pension. Using 0. Are you missing a price directive?')
        )

    def test_asset_classes(self):
        asset_classes = self.allocations.asset_classes()

        self.assertEqual(len(asset_classes), 1)
        self.assertTrue("equity" in asset_classes)

    def test_cash_asset_subclass(self):
        asset_subclasses = self.allocations.asset_subclasses("cash")

        self.assertEqual(len(asset_subclasses), 0)

    def test_equity_asset_subclass(self):
        asset_subclasses = self.allocations.asset_subclasses("equity")

        self.assertEqual(len(asset_subclasses), 2)
        self.assertTrue("usa" in asset_subclasses)
        self.assertTrue("uk" in asset_subclasses)

    def test_cash_value(self):
        value = self.allocations.value_for_class_subclass("cash", "cash")

        self.assertEqual(value, 0)

    def test_equity_value(self):
        value = self.allocations.value_for_class_subclass("equity", "usa")

        self.assertEqual(value, 0)

    def test_total_invested(self):
        total = self.allocations.total_invested_for_portfolio()

        self.assertEqual(total, Decimal('24.4495'))

    def test_allocation_directives(self):
        targets = self.targets

        self.assertEqual(len(targets), 0)
