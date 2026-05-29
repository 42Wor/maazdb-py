# FILE PATH: maazdb-py/setup.py

from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

def read_requirements():
    requirements = []
    if os.path.exists(os.path.join(this_directory, "requirements.txt")):
        with open(os.path.join(this_directory, "requirements.txt"), encoding="utf-8") as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return requirements

setup(
    name="maazdb-py",
    version="2.0.0", # Upgraded to 2.0.0
    author="Maaz Waheed",
    author_email="wwork4287@gmail.com",
    description="Official Python Driver for MaazDB (Protocol v2.1)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/42Wor/maazdb-py",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.900",
            "twine>=3.0.0",
            "build>=0.7.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="database, driver, maazdb, client, nosql",
    project_urls={
        "Documentation": "https://maazdb.vercel.app/docs",
        "Source": "https://github.com/42Wor/maazdb-py",
        "Tracker": "https://github.com/42Wor/maazdb-py/issues",
    },
    package_data={
        "maazdb": ["py.typed", "*.pyi"],
    },
    zip_safe=False,
)