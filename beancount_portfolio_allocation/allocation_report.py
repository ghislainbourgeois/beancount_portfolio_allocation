#!/usr/bin/env python3
__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import beancount_portfolio_allocation.loader as loader


def report(bean, portfolio):
    targets, allocations, total = loader.load(bean, portfolio)

    report = ""
    for k in allocations.asset_classes():
        report += _class_header(k)
        for s in allocations.asset_subclasses(k):
            value = allocations.value_for_class_subclass(k, s)
            percentage = allocations.percentage_for_class_subclass(k, s)
            target = targets.get(s, 0)
            diff = cash_difference(target, percentage, total)
            report += str("%-10s \t %.2f \t %.2f \t\t %.2f \t\t %.2f\n" %
                          (s, value, percentage, target, diff))
        report += "\n"

    return report


def _class_header(asset_class):
    result = asset_class
    result += "\n"
    result += ("=" * 75)
    result += "\n"
    result += "subclass \t amount \t percent \t target \t difference\n"
    result += ("-" * 75)
    result += "\n"
    return result


def percentage_difference(target, percentage):
    return float(target - percentage)


def cash_difference(target, percentage, total):
        return percentage_difference(target, percentage) / 100 * float(total)


def main():
    import argparse
    parser = argparse.ArgumentParser(
                "Report on portfolio asset classes allocation vs targets."
                )
    parser.add_argument('bean', help='Path to the beancount file.')
    parser.add_argument('--portfolio',
                        type=str,
                        help='Name of portfolio to report on',
                        required=True)
    args = parser.parse_args()

    print(report(args.bean, args.portfolio))


if __name__ == "__main__":
    main()
