with open("README.md", "r", encoding="utf-8") as fh:
    longdesc = fh.read()

setuptools.setup(
    name="usempl_npp",
    version="0.0.0",
    author="Richard W. Evans",
    license="CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    description="Package for creating normalized peak plot of U.S. nonfarm employment (PAYEMS) in last 15 recessions",
    long_description_content_type="text/markdown",
    long_description=longdesc,
    url="https://github.com/OpenSourceEcon/USempl_NormPeakPlot",
    download_url="https://github.com/OpenSourceEcon/USempl_NormPeakPlot",
    project_urls={
        "Issue Tracker": "https://github.com/OpenSourceEcon/USempl_NormPeakPlot/issues",
    },
    packages=["usempl_npp"],
    package_data={
        "usempl_npp": [
            "data/usempl_2022-11-01.csv",
            "data/usempl_annual_1919-1938.csv",
            "data/usempl_pk_2022-11-01.csv",
        ]
    },
    include_packages=True,
    python_requires=">=3.10.8",
    install_requires=[
        "numpy>=1.23.4",
        "scipy>=1.9.3",
        "pandas>=1.5.2",
        "pandas-datareader>=0.10.0",
        "bokeh>=2.4.3, <3.0",
        "pytest>=7.1.2",
        "pytest-cov",
        "pytest-pycodestyle",
        "coverage>=6.3.2",
        "codecov>=2.1.11",
        "black>=22.6.0",
        "pip>=22.3.1",
        "linecheck>=0.1.0",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tests_require=["pytest"],
)
