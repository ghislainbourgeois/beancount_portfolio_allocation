__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import unittest
import beancount_portfolio_allocation.loader as loader


class TestAllocationReportZeroPosition(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.file = "tests/test-zero-position.beancount"
        self.portfolio = "pension"
        (self.targets, self.allocations,
            self.total) = loader.load(self.file, self.portfolio)

    def test_asset_classes(self):
        asset_classes = self.allocations.asset_classes()

        self.assertEqual(len(asset_classes), 3)
        self.assertTrue("cash" in asset_classes)
        self.assertTrue("equity" in asset_classes)
        self.assertTrue("fixed" in asset_classes)

    def test_cash_asset_subclass(self):
        asset_subclasses = self.allocations.asset_subclasses("cash")

        self.assertEqual(len(asset_subclasses), 1)
        self.assertTrue("cash" in asset_subclasses)

    def test_equity_asset_subclass(self):
        asset_subclasses = self.allocations.asset_subclasses("equity")

        self.assertEqual(len(asset_subclasses), 2)
        self.assertTrue("ca-stock" in asset_subclasses)
        self.assertTrue("us-stock" in asset_subclasses)

    def test_cash_value(self):
        value = self.allocations.value_for_class_subclass("cash", "cash")

        self.assertEqual(value, 1080)

    def test_equity_value(self):
        value = self.allocations.value_for_class_subclass("equity", "ca-stock")

        self.assertEqual(value, 0)

    def test_total_invested(self):
        total = self.allocations.total_invested_for_portfolio()

        self.assertEqual(total, 2000)

    def test_allocation_directives(self):
        targets = self.targets

        self.assertEqual(len(targets), 3)
        self.assertTrue("ca-stock" in targets)
        self.assertEqual(targets["ca-stock"], 30)
        self.assertTrue("ca-bond" in targets)
        self.assertEqual(targets["ca-bond"], 40)
