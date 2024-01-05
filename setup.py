from setuptools import setup, find_packages

setup(
    name="azf_wrappers",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "azure-functions>=1.0.0,<2.0.0",
    ],
)
