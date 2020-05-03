from setuptools import setup

setup(
    name="VerbalExpressions",
    version="0.0.2",
    description="Make difficult regular expressions easy! Python port of the awesome VerbalExpressions repo - https://github.com/jehna/VerbalExpressions",
    long_description="Please see https://github.com/VerbalExpressions/PythonVerbalExpressions/blob/master/README.md for more information!",
    author="Victor Titor, Yan Wenjun, diogobeda, Mihai Ionut Vilcu, Peder Soholt, Sameer Raghuram, Kharms",
    license="MIT",
    url="https://github.com/VerbalExpressions/PythonVerbalExpressions",
    test_suite="tests",
    packages=["verbalexpressions"],
    tests_require=["six"],
    extras_require={"dev": ["pre-commit", "black"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing",
    ],
)
