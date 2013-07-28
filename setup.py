#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'VerbalExpressions',
          version = '0.0.1',
          description = 'Make difficult regular expressions easy! Python port of the awesome VerbalExpressions repo - https://github.com/jehna/VerbalExpressions',
          long_description = '''Please see https://github.com/VerbalExpressions/PythonVerbalExpressions/blob/master/README.md for more information!''',
          author = "Mihai Ionut Vilcu, Peder Soholt",
          author_email = "",
          license = 'MIT',
          url = 'https://github.com/VerbalExpressions/PythonVerbalExpressions',
          test_suite='tests',
          scripts = [],
          packages = ['verbalexpressions'],
          classifiers = [],
          zip_safe=True
    )

