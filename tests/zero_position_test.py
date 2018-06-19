__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import unittest
import beancount_portfolio_allocation.loader as loader


class TestAllocationReportZeroPosition(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.file = "tests/test_inputs/zero-position.beancount"
        self.portfolio = "pension"
        (self.targets, self.allocations,
            self.total) = loader.load(self.file, self.portfolio)

    def test_zero_position_equity_value(self):
        value = self.allocations.value_for_class_subclass("equity", "ca-stock")

        self.assertEqual(value, 0)
