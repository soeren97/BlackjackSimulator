"""Setup script for the ShipNeT package."""

import versioneer
from setuptools import find_packages, setup

# Requirements definitions
SETUP_REQUIRES = [
    "setuptools",
]

INSTALL_REQUIRES = [
    "matplotlib",
    "numpy",
    "pandas",
]

EXTRAS_REQUIRE = {
    "develop": [
        "black",
        "isort",
        "flake8",
        "autopep8",
        "pre-commit",
    ],
}

# https://pypi.org/classifiers/
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.11",
    "Environment :: CPU",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name="BlackjackSimulator",
    version=versioneer.get_version(),
    description=("Blackjack simulator"),
    license="MIT License",
    author="Søren Langkilde",
    url="https://github.com/soeren97/BlackjackSimulator",
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_requires=SETUP_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=CLASSIFIERS,
)
