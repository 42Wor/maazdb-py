from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Read requirements from requirements.txt if it exists
def read_requirements():
    requirements = []
    if os.path.exists(os.path.join(this_directory, "requirements.txt")):
        with open(os.path.join(this_directory, "requirements.txt"), encoding="utf-8") as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return requirements

setup(
    # Basic package information
    name="maazdb-py",
    version="1.0.0",
    author="Maaz",
    author_email="your.email@example.com",  # Add your email
    description="Official Python Driver for MaazDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/42Wor/maazdb-py",  # Your GitHub repo
    
    # Package discovery
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    
    # Python version requirement
    python_requires=">=3.7",
    
    # Dependencies
    install_requires=read_requirements(),  # Or specify directly:
    # install_requires=[
    #     "requests>=2.25.0",  # If you make HTTP requests
    #     "websocket-client>=1.0.0",  # If using WebSockets
    # ],
    
    # Optional dependencies for development
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
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    
    # Package classifiers for PyPI
    classifiers=[
        "Development Status :: 4 - Beta",  # Or "5 - Production/Stable" when ready
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends",
        "License :: OSI Approved :: MIT License",  # Choose appropriate license
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    
    # Keywords for PyPI search
    keywords="database, driver, maazdb, client, nosql",
    
    # Project URLs
    project_urls={
        "Documentation": "https://maazdb.vercel.app/docs",  # If you have docs
        "Source": "https://github.com/42Wor/maazdb-py",
        "Tracker": "https://github.com/42Wor/maazdb-py/issues",
    },
    
    # Include package data files
    package_data={
        "maazdb": ["py.typed", "*.pyi"],  # For type hints
    },
    
    # Entry points if you want to create CLI commands
    entry_points={
        "console_scripts": [
            # "maazdb-cli = maazdb.cli:main",  # Uncomment if you have a CLI
        ],
    },
    
    # ZIP safe flag
    zip_safe=False,
)