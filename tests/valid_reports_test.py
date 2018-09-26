__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import pytest
import beancount_portfolio_allocation.loader as loader
import beancount_portfolio_allocation.allocation_report as allocation_report

from collections import namedtuple


@pytest.fixture(scope="module", params=[
    "tests/test_inputs/account_based_asset_class.beancount",
    "tests/test_inputs/portfolio.beancount"
])
def filename(request):
    return "tests/test_inputs/account_based_asset_class.beancount"


@pytest.fixture(scope="module")
def portfolio_name():
    return "pension"


@pytest.fixture(scope="module")
def portfolio(filename, portfolio_name):
    (targets, allocations,
        total) = loader.load(filename, portfolio_name)
    Portfolio = namedtuple('Portfolio', 'targets allocations total')
    return Portfolio(targets=targets, allocations=allocations, total=total)


def test_asset_classes(portfolio):
    asset_classes = portfolio.allocations.asset_classes()

    assert len(asset_classes) == 3
    assert "cash" in asset_classes
    assert "equity" in asset_classes
    assert "fixed" in asset_classes


def test_cash_asset_subclass(portfolio):
    asset_subclasses = portfolio.allocations.asset_subclasses("cash")

    assert len(asset_subclasses) == 1
    assert "cash" in asset_subclasses


def test_equity_asset_subclass(portfolio):
    asset_subclasses = portfolio.allocations.asset_subclasses("equity")

    assert len(asset_subclasses) == 2
    assert "ca-stock" in asset_subclasses
    assert "us-stock" in asset_subclasses


def test_cash_value(portfolio):
    value = portfolio.allocations.value_for_class_subclass("cash", "cash")

    assert value == 380


def test_equity_value(portfolio):
    value = portfolio.allocations.value_for_class_subclass("equity", "ca-stock")

    assert value == 700


def test_total_invested(portfolio):
    total = portfolio.allocations.total_invested_for_portfolio()

    assert total == 2000


def test_allocation_directives(portfolio):
    targets = portfolio.targets

    assert len(targets) == 3
    assert "ca-stock" in targets
    assert targets["ca-stock"] == 30
    assert "ca-bond" in targets
    assert targets["ca-bond"] == 40


def test_main_report(filename, portfolio_name):
    report = allocation_report.report(filename, portfolio_name)

    expected_report = """CASH
====
Subclass      Market Value    Percentage    Target %    Difference
----------  --------------  ------------  ----------  ------------
cash                380.00         19.00        0.00       -380.00


EQUITY
======
Subclass      Market Value    Percentage    Target %    Difference
----------  --------------  ------------  ----------  ------------
ca-stock            700.00         35.00       30.00       -100.00
us-stock            600.00         30.00       30.00          0.00


FIXED
=====
Subclass      Market Value    Percentage    Target %    Difference
----------  --------------  ------------  ----------  ------------
ca-bond             320.00         16.00       40.00        480.00
"""

    assert report == expected_report


def test_report_data(portfolio):
    data = allocation_report.report_data(portfolio.targets,
                                         portfolio.allocations,
                                         portfolio.total)

    expected = {'cash':   [['cash', 380, 19.00, 0.00, -380.00]],
                'equity': [['ca-stock', 700, 35.00, 30.00, -100.00],
                           ['us-stock', 600, 30.00, 30.00, 0.00]],
                'fixed':  [['ca-bond', 320, 16.00, 40.00, 480.00]]}
    assert data == expected
