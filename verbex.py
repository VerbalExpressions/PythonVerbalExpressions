from verbalexpressions import VerEx, re_escape

verbal_expression = VerEx()
# Create an example of how to test for correctly formed URLs
verbal_expression = VerEx()
tester = (
    verbal_expression.start_of_line()
    .find("http")
    .maybe("s")
    .find("://")
    .maybe("www.")
    .anything_but(" ")
    .end_of_line()
)

# # Create an example URL
# test_url = "https://www.google.com"

# # Test if the URL is valid
# if tester.match(test_url):
#     print "Valid URL"

# # Print the generated regex
# print tester.source() # => ^(http)(s)?(\:\/\/)(www\.)?([^\ ]*)$


# # Create a test string
# replace_me = "Replace bird with a duck"

# # Create an expression that looks for the word "bird"
# expression = VerEx().find('bird')

# # Execute the expression in VerEx
# result_VerEx = expression.replace(replace_me, 'duck')
# print result_VerEx

# # Or we can compile and use the regular expression using re
# import re
# regexp = expression.compile()
# result_re = regexp.sub('duck', replace_me)
# print result_re
