# -*- encoding: utf-8 -*-

import unittest
import re

import six

import verbalexpressions


class VerExTest(unittest.TestCase):
    """ Tests for verbal_expressions.py """

    if six.PY3:
        assertNotRegexpMatches = unittest.TestCase.assertNotRegex

    def setUp(self):
        self.v = verbalexpressions.VerEx()

    def tearDown(self):
        self.v = None
        self.exp = None

    def test_should_render_verex_as_string(self):
        self.assertEqual(str(self.v.add("^$")), "^$")

    def test_should_render_verex_list_as_string(self):
        self.assertEqual(str(self.v.add(["^", "[0-9]", "$"])), "^[0-9]$")

    def test_should_match_characters_in_range(self):
        self.exp = self.v.start_of_line().range("a", "c").regex()
        for character in ["a", "b", "c"]:
            six.assertRegex(self, character, self.exp)

    def test_should_not_match_characters_outside_of_range(self):
        self.exp = self.v.start_of_line().range("a", "c").regex()
        self.assertNotRegexpMatches("d", self.exp)

    def test_should_match_characters_in_extended_range(self):
        self.exp = self.v.start_of_line().range("a", "b", "X", "Z").regex()
        for character in ["a", "b"]:
            six.assertRegex(self, character, self.exp)
        for character in ["X", "Y", "Z"]:
            six.assertRegex(self, character, self.exp)

    def test_should_not_match_characters_outside_of_extended_range(self):
        self.exp = self.v.start_of_line().range("a", "b", "X", "Z").regex()
        self.assertNotRegexpMatches("c", self.exp)
        self.assertNotRegexpMatches("W", self.exp)

    def test_should_match_start_of_line(self):
        self.exp = self.v.start_of_line().regex()
        six.assertRegex(self, "text  ", self.exp, "Not started :(")

    def test_should_match_end_of_line(self):
        self.exp = self.v.start_of_line().end_of_line().regex()
        six.assertRegex(self, "", self.exp, "It's not the end!")

    def test_should_match_anything(self):
        self.exp = self.v.start_of_line().anything().end_of_line().regex()
        six.assertRegex(
            self, "!@#$%¨&*()__+{}", self.exp, "Not so anything..."
        )

    def test_should_match_anything_but_specified_element_when_element_is_not_found(
        self
    ):
        self.exp = (
            self.v.start_of_line().anything_but("X").end_of_line().regex()
        )
        six.assertRegex(self, "Y Files", self.exp, "Found the X!")

    def test_should_not_match_anything_but_specified_element_when_specified_element_is_found(
        self
    ):
        self.exp = (
            self.v.start_of_line().anything_but("X").end_of_line().regex()
        )
        self.assertNotRegexpMatches("VerEX", self.exp, "Didn't found the X :(")

    def test_should_find_element(self):
        self.exp = self.v.start_of_line().find("Wally").end_of_line().regex()
        six.assertRegex(self, "Wally", self.exp, "404! Wally not Found!")

    def test_should_not_find_missing_element(self):
        self.exp = self.v.start_of_line().find("Wally").end_of_line().regex()
        self.assertNotRegexpMatches("Wall-e", self.exp, "DAFUQ is Wall-e?")

    def test_should_match_when_maybe_element_is_present(self):
        self.exp = (
            self.v.start_of_line()
            .find("Python2.")
            .maybe("7")
            .end_of_line()
            .regex()
        )
        six.assertRegex(self, "Python2.7", self.exp, "Version doesn't match!")

    def test_should_match_when_maybe_element_is_missing(self):
        self.exp = (
            self.v.start_of_line()
            .find("Python2.")
            .maybe("7")
            .end_of_line()
            .regex()
        )
        six.assertRegex(self, "Python2.", self.exp, "Version doesn't match!")

    def test_should_match_on_any_when_element_is_found(self):
        self.exp = (
            self.v.start_of_line().any("Q").anything().end_of_line().regex()
        )
        six.assertRegex(self, "Query", self.exp, "No match found!")

    def test_should_not_match_on_any_when_element_is_not_found(self):
        self.exp = (
            self.v.start_of_line().any("Q").anything().end_of_line().regex()
        )
        self.assertNotRegexpMatches("W", self.exp, "I've found it!")

    def test_should_match_when_line_break_present(self):
        self.exp = (
            self.v.start_of_line()
            .anything()
            .line_break()
            .anything()
            .end_of_line()
            .regex()
        )
        six.assertRegex(self, "Marco \n Polo", self.exp, "Give me a break!!")

    def test_should_match_when_line_break_and_carriage_return_present(self):
        self.exp = (
            self.v.start_of_line()
            .anything()
            .line_break()
            .anything()
            .end_of_line()
            .regex()
        )
        six.assertRegex(self, "Marco \r\n Polo", self.exp, "Give me a break!!")

    def test_should_not_match_when_line_break_is_missing(self):
        self.exp = (
            self.v.start_of_line()
            .anything()
            .line_break()
            .anything()
            .end_of_line()
            .regex()
        )
        self.assertNotRegexpMatches(
            "Marco Polo", self.exp, "There's a break here!"
        )

    def test_should_match_when_tab_present(self):
        self.exp = (
            self.v.start_of_line().anything().tab().end_of_line().regex()
        )
        six.assertRegex(self, "One tab only	", self.exp, "No tab here!")

    def test_should_not_match_when_tab_is_missing(self):
        self.exp = (
            self.v.start_of_line().anything().tab().end_of_line().regex()
        )
        self.assertFalse(
            re.match(self.exp, "No tab here"), "There's a tab here!"
        )

    def test_should_match_when_word_present(self):
        self.exp = (
            self.v.start_of_line().anything().word().end_of_line().regex()
        )
        six.assertRegex(self, "Oneword", self.exp, "Not just a word!")

    def test_not_match_when_two_words_are_present_instead_of_one(self):
        self.exp = (
            self.v.start_of_line().anything().tab().end_of_line().regex()
        )
        self.assertFalse(
            re.match(self.exp, "Two words"), "I've found two of them"
        )

    def test_should_match_when_or_condition_fulfilled(self):
        self.exp = (
            self.v.start_of_line()
            .anything()
            .find("G")
            .OR()
            .find("h")
            .end_of_line()
            .regex()
        )
        six.assertRegex(self, "Github", self.exp, "Octocat not found")

    def test_should_not_match_when_or_condition_not_fulfilled(self):
        self.exp = (
            self.v.start_of_line()
            .anything()
            .find("G")
            .OR()
            .find("h")
            .end_of_line()
            .regex()
        )
        self.assertFalse(re.match(self.exp, "Bitbucket"), "Bucket not found")

    def test_should_match_on_upper_case_when_lower_case_is_given_and_any_case_is_true(
        self
    ):
        self.exp = (
            self.v.start_of_line()
            .find("THOR")
            .end_of_line()
            .with_any_case(True)
            .regex()
        )
        six.assertRegex(self, "thor", self.exp, "Upper case Thor, please!")

    def test_should_match_multiple_lines(self):
        self.exp = (
            self.v.start_of_line()
            .anything()
            .find("Pong")
            .anything()
            .end_of_line()
            .search_one_line(True)
            .regex()
        )
        six.assertRegex(
            self, "Ping \n Pong \n Ping", self.exp, "Pong didn't answer"
        )

    def test_should_match_email_address(self):
        self.exp = (
            self.v.start_of_line()
            .word()
            .then("@")
            .word()
            .then(".")
            .word()
            .end_of_line()
            .regex()
        )
        six.assertRegex(self, "mail@mail.com", self.exp, "Not a valid email")

    def test_should_match_url(self):
        self.exp = (
            self.v.start_of_line()
            .then("http")
            .maybe("s")
            .then("://")
            .maybe("www.")
            .word()
            .then(".")
            .word()
            .maybe("/")
            .end_of_line()
            .regex()
        )
        six.assertRegex(
            self, "https://www.google.com/", self.exp, "Not a valid email"
        )
