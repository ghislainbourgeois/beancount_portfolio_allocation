__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import unittest
import beancount_portfolio_allocation.loader as loader
from testfixtures import log_capture


class TestOperatingCurrencyMissingReport(unittest.TestCase):
    def setUp(self):
        self.file = "tests/test_inputs/no-main-currency.beancount"
        self.portfolio = "pension"

    @log_capture()
    def test_missing_operating_currency_errors_and_exit(self, capture):
        with self.assertRaises(SystemExit):
            (self.targets, self.allocations,
                self.total) = loader.load(self.file, self.portfolio)
        capture.check(
            ('root',
             'ERROR',
             'Missing operating_currency')
        )
