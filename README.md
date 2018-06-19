PythonVerbalExpressions
=======================

[![Build Status](https://travis-ci.org/VerbalExpressions/PythonVerbalExpressions.svg?branch=master)](https://travis-ci.org/VerbalExpressions/PythonVerbalExpressions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Installation
```bash
pip install VerbalExpressions
```
## Usage
```python
from verbalexpressions import VerEx
verbal_expression = VerEx()
```
## Examples

### Testing if we have a valid URL
```python
# Create an example of how to test for correctly formed URLs
verbal_expression = VerEx()
tester = (verbal_expression.
            start_of_line().
            find('http').
            maybe('s').
            find('://').
            maybe('www.').
            anything_but(' ').
            end_of_line()
)

# Create an example URL
test_url = "https://www.google.com"

# Test if the URL is valid
if tester.match(test_url):
    print "Valid URL"

# Print the generated regex
print tester.source() # => ^(http)(s)?(\:\/\/)(www\.)?([^\ ]*)$
```
### Replacing strings
```python
# Create a test string
replace_me = "Replace bird with a duck"

# Create an expression that looks for the word "bird"
expression = VerEx().find('bird')

# Execute the expression in VerEx
result_VerEx = expression.replace(replace_me, 'duck')
print result_VerEx

# Or we can compile and use the regular expression using re
import re
regexp = expression.compile()
result_re = regexp.sub('duck', replace_me)
print result_re
```
### Shorthand for string replace
```python
result = VerEx().find('red').replace('We have a red house', 'blue')
print result
```

## Developer setup : running the tests
```bash
python setup.py develop
python setup.py test
```
## Other implementations  
You can view all implementations on [VerbalExpressions.github.io](http://VerbalExpressions.github.io)
