# setup.py

from setuptools import setup, find_packages

setup(
    name="playwright_extension",  # Package name
    version="0.1.0",  # Package version
    packages=find_packages(),  # Automatically find packages
    install_requires=[  # Dependencies
        "playwright==1.43.0",
        "playwright-stealth",
        "fake-useragent",
        "setuptools",
    ],
    author="boysugi",  # Your name
    author_email="snoodledolitol@gmail.com",  # Your email
    description="A simple python playwright extension",  # Short description
    long_description=open("README.md").read(),  # Long description from README
    long_description_content_type="text/markdown",  # Specify the format
    url="https://github.com/boysugi20/playwright-extension",  # GitHub repository URL
    python_requires=">=3.9",  # Specify Python version
)
