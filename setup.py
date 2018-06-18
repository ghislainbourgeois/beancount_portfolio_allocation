__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="beancount_portfolio_allocation",
        version="0.2.0",
        packages=setuptools.find_packages(),
        entry_points={
            'console_scripts': [
                'bean-portfolio-allocation-report = beancount_portfolio_allocation.allocation_report:main',
            ],
        },

        install_requires=['beancount>=2.1.2'],
        tests_require=['testfixtures'],

        test_suite="tests",

        author="Ghislain Bourgeois",
        author_email="ghislain.bourgeois@gmail.com",
        description="Beancount portfolio allocation report",
        long_description=long_description,
        long_description_content_type="text/markdown",
        license="GPLv2",
        keywords="beancount report portfolio allocation",
        url="https://github.com/ghislainbourgeois/beancount_portfolio_allocation/",

        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
            "Operating System :: OS Independent",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Financial and Insurance Industry",
            "Topic :: Office/Business :: Financial",
            "Topic :: Office/Business :: Financial :: Accounting",
            "Topic :: Office/Business :: Financial :: Investment",
        ),
)
