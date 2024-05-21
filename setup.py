import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="robotframework-testnotify",
    version="1.1.0",
    description="Send notifications to chat using Robot Framework.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/barbosamp/robotframework-testnotification.git",
    author="Marcos Barbosa",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    packages=["TestNotification"],
    include_package_data=True,
    install_requires=["requests"],
)