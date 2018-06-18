__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import logging

from beancount import loader
from beancount.query import query
from beancount.core.data import Custom
from beancount_portfolio_allocation.allocation import Allocations, Position


def load(bean, portfolio):
    entries, errors, options_map = loader.load_file(bean)

    if _missing_operating_currency(options_map):
        logging.error("Missing operating_currency")
        exit(1)

    targets = get_allocation_directives(entries, portfolio)

    allocations = get_allocations(entries, options_map, portfolio)

    total = allocations.total_invested_for_portfolio()

    return (targets, allocations, total)


def _missing_operating_currency(o):
    return 'operating_currency' not in o or len(o['operating_currency']) < 1


def get_allocation_directives(entries, portfolio):
    res = dict()
    for e in entries:
        if isinstance(e, Custom) and e.type == "allocation":
            if e.values[0].value == portfolio:
                res[e.values[1].value] = e.values[2].value
    return res


def _position_from_row(row):
        symbol = row[0]
        asset_class = row[1]
        asset_subclass = row[2]
        account = row[3]
        price = row[4]
        value = row[5]
        return Position(symbol, value, asset_class, asset_subclass, account, price)


def get_allocations(entries, options_map, portfolio):
    allocation_query = r"""
            SELECT currency,
                   GETITEM(CURRENCY_META(currency), "asset-class") as c,
                   GETITEM(CURRENCY_META(currency), "asset-subclass") as s,
                   account,
                   getprice(currency, "{1}", today()) as price,
                   convert(value(sum(position)), "{1}")
            WHERE GETITEM(OPEN_META(account), "portfolio") = "{0}"
            GROUP BY currency, c, s, account, price
            """

    target_currency = options_map['operating_currency'][0]
    rtypes, rrows = query.run_query(entries,
                                    options_map,
                                    allocation_query,
                                    portfolio,
                                    target_currency,
                                    numberify=True)

    allocations = Allocations()
    for row in rrows:
        position = _position_from_row(row)
        allocations.append(position)
    return allocations
