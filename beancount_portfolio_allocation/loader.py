__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

from beancount import loader
from beancount.query import query
from beancount.core.data import Custom
from beancount_portfolio_allocation.allocation import Allocations, Position


def load(bean, portfolio):
    entries, errors, options_map = loader.load_file(bean)

    targets = get_allocation_directives(entries, portfolio)

    allocations = get_allocations(entries, options_map, portfolio)

    total = allocations.total_invested_for_portfolio()

    return (targets, allocations, total)


def get_allocation_directives(entries, portfolio):
    res = dict()
    for e in entries:
        if isinstance(e, Custom) and e.type == "allocation":
            if e.values[0].value == portfolio:
                res[e.values[1].value] = e.values[2].value
    return res


def _position_from_row(row):
        symbol = row[0]
        value = row[1]
        asset_class = row[2]
        asset_subclass = row[3]
        account = row[4]
        return Position(symbol, value, asset_class, asset_subclass, account)


def get_allocations(entries, options_map, portfolio):
    allocation_query = r"""
            SELECT currency,
                   value(sum(position)),
                   GETITEM(CURRENCY_META(currency), "asset-class") as c,
                   GETITEM(CURRENCY_META(currency), "asset-subclass") as s,
                   account
            WHERE GETITEM(OPEN_META(account), "portfolio") = "{}"
            GROUP BY currency, c, s, account
            """

    rtypes, rrows = query.run_query(entries,
                                    options_map,
                                    allocation_query,
                                    portfolio,
                                    numberify=True)

    allocations = Allocations()
    for row in rrows:
        position = _position_from_row(row)
        allocations.append(position)
    return allocations
