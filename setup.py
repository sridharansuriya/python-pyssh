from setuptools import setup

setup(
    name="pyssh",
    version="0.1.0",
    py_modules=["main", "cli", "interactive", "ssh"],
    install_requires=[
        "paramiko",
    ],
    entry_points={
        "console_scripts": [
            "pyssh = main:main",
        ],
    },
)
