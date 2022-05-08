from pathlib import Path

from setuptools import setup

SCRIPT_ROOT = Path(__file__).parent
long_description = (SCRIPT_ROOT / "README.md").read_text()

setup(
    name="Verbex",
    version="1.0.2",
    description=(
        "Make difficult regular expressions easy! Python fork based on of the awesome"
        " VerbalExpressions repo - https://github.com/jehna/VerbalExpressions"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=(
        "Victor Titor, Yan Wenjun, diogobeda, Mihai Ionut Vilcu, Peder Soholt, Sameer"
        " Raghuram, Kharms, Richard Broderick"
    ),
    license="GPLv3",
    url="https://github.com/VerbalExpressions/PythonVerbalExpressions",
    test_suite="tests",
    packages=["verbex"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing",
    ],
    include_package_data=True,
)
