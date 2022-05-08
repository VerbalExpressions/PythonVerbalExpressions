Verbex: Python verbal based regular expressions
================================================

![Build Status](https://github.com/rbroderi/Verbex/actions/workflows/main.yml/badge.svg?event=push)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Installation
```bash
pip install Verbex
```
## Usage
```python
from verbex import Verbex
verbex = Verbex()
```

## Documentation
[API](https://rbroderi.github.io/Verbex/verbex/verbex.html)
## Examples

### Testing if we have a valid URL
```python
# Create an example of how to test for correctly formed URLs
verbex = Verbex()
tester = (verbex.
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
if re.match(test_url.regex,test_url):
    print("Valid URL")

# Print the generated regex
print(tester) # => ^(http)(s)?(\:\/\/)(www\.)?([^\ ]*)$
```
### Replacing strings
```python
# Create a test string
replace_me = "Replace bird with a duck"

# Create an expression that looks for the word "bird"
expression = Verbex().find('bird')

# Compile and use the regular expression using re
import re
regexp = expression.compile()
result_re = regexp.sub('duck', replace_me)
print(result_re)
```

## Developer setup : running the tests
```bash
python setup.py develop
python setup.py test
```
## Other implementations
You can view all implementations on [VerbalExpressions.github.io](http://VerbalExpressions.github.io)
