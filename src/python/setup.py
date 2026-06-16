# setup.py (if you want to install as a package)
from setuptools import setup, find_packages

setup(
    name="voice-of-brahma",
    version="1.0.0",
    description="Universal Ternary Language Platform",
    author="Seliim Ahmed",
    author_email="amit.khanna.1082@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
