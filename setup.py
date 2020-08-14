from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="scripts",
    version="0.0.1",
    author="D-Bhatta",
    author_email="email",
    description="Notes and code about python features",
    long_description="Notes and code about python features",
    long_description_content_type="text/markdown",
    url="https://github.com/D-Bhatta/Python-Features.git",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
