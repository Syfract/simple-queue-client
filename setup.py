from setuptools import setup, find_packages

setup(
    name="simple_queue_client",
    version="0.4",
    packages=find_packages(),
    install_requires="requests>=2,<3"
)
