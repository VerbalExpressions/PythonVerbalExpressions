# -*- encoding: utf-8 -*-
import unittest
from verbalexpressions import VerEx
import re

class VerExTest(unittest.TestCase):
    '''
        Tests for verbal_expressions.py
    '''
    def setUp(self):
        self.v = VerEx()

    def tearDown(self):
        self.v = None
        self.exp = None

    def test__str__(self):
        self.assertEquals(str(self.v.add('^$')), '^$')

    def test_should_match_characters_in_range(self):
        self.exp = self.v.start_of_line().range('a', 'c').regex()
        for character in ['a', 'b', 'c']:
            self.assertRegexpMatches(character, self.exp)

    def test_should_not_match_characters_outside_of_range(self):
        self.exp = self.v.start_of_line().range('a', 'c').regex()
        self.assertNotRegexpMatches('d', self.exp)

    def test_should_match_characters_in_extended_range(self):
        self.exp = self.v.start_of_line().range('a', 'b', 'X', 'Z').regex()
        for character in ['a', 'b']:
            self.assertRegexpMatches(character, self.exp)
        for character in ['X', 'Y', 'Z']:
            self.assertRegexpMatches(character, self.exp)

    def test_should_not_match_characters_outside_of_extended_range(self):
        self.exp = self.v.start_of_line().range('a', 'b', 'X', 'Z').regex()
        self.assertNotRegexpMatches('c', self.exp)
        self.assertNotRegexpMatches('W', self.exp)


    def test_start_of_line(self):
        self.exp = self.v.start_of_line().regex()
        self.assertRegexpMatches('text  ', self.exp, 'Not started :(')

    def test_end_of_line(self):
        self.exp = self.v.start_of_line().end_of_line().regex()
        self.assertRegexpMatches('', self.exp, 'It\'s not the end!')

    def test_anything(self):
        self.exp = self.v.start_of_line().anything().end_of_line().regex()
        self.assertRegexpMatches('!@#$%¨&*()__+{}', self.exp, 'Not so anything...')

    def test_anything_but(self):
        self.exp = self.v.start_of_line().anything_but('X').end_of_line().regex()
        self.assertRegexpMatches('Y Files', self.exp, 'Found the X!')

    def test_anything_but_false(self):
        self.exp = self.v.start_of_line().anything_but('X').end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'VerEX'), 'Didn\'t found the X :(')

    def test_find_true(self):
        self.exp = self.v.start_of_line().find('Wally').end_of_line().regex()
        self.assertRegexpMatches('Wally', self.exp, '404! Wally not Found!')

    def test_find_false(self):
        self.exp = self.v.start_of_line().find('Wally').end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'Wall-e'), 'DAFUQ is Wall-e?')

    def test_maybe(self):
        self.exp = self.v.start_of_line().find('Python2.').maybe('7').end_of_line().regex()
        self.assertRegexpMatches('Python2.7', self.exp, 'Version doesn\'t match!')

    def test_any_true(self):
        self.exp = self.v.start_of_line().any('Q').anything().end_of_line().regex()
        self.assertRegexpMatches('Query', self.exp, 'No match found!')

    def test_any_false(self):
        self.exp = self.v.start_of_line().any('Q').anything().end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'W'), 'I\'ve found it!')

    def test_line_break_true_n(self):
        self.exp = self.v.start_of_line().anything().line_break().anything().end_of_line().regex()
        self.assertRegexpMatches('Marco \n Polo', self.exp, 'Give me a break!!')

    def test_line_break_true_rn(self):
        self.exp = self.v.start_of_line().anything().line_break().anything().end_of_line().regex()
        self.assertRegexpMatches('Marco \r\n Polo', self.exp, 'Give me a break!!')

    def test_line_break_false(self):
        self.exp = self.v.start_of_line().anything().line_break().anything().end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'Marco Polo'), 'There\'s a break here!')

    def test_tab_true(self):
        self.exp = self.v.start_of_line().anything().tab().end_of_line().regex()
        self.assertRegexpMatches('One tab only	', self.exp, 'No tab here!')

    def test_tab_false(self):
        self.exp = self.v.start_of_line().anything().tab().end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'No tab here'), 'There\'s a tab here!')

    def test_word_true(self):
        self.exp = self.v.start_of_line().anything().word().end_of_line().regex()
        self.assertRegexpMatches('Oneword', self.exp, 'Not just a word!')

    def test_word_false(self):
        self.exp = self.v.start_of_line().anything().tab().end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'Two words'), 'I\'ve found two of them')

    def test_or_true(self):
        self.exp = self.v.start_of_line().anything().find('G').OR().find('h').end_of_line().regex()
        self.assertRegexpMatches('Github', self.exp, 'Octocat not found')

    def test_or_false(self):
        self.exp = self.v.start_of_line().anything().find('G').OR().find('h').end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'Bitbucket'), 'Bucket not found')

    def test_any_case(self):
        self.exp = self.v.start_of_line().find('THOR').end_of_line().with_any_case(True).regex()
        self.assertRegexpMatches('thor', self.exp, 'Upper case Thor, please!')

    def test_multi_line(self):
        self.exp = self.v.start_of_line().anything().find('Pong').anything().end_of_line().search_one_line(True).regex()
        self.assertRegexpMatches('Ping \n Pong \n Ping', self.exp, 'Pong didn\'t answer')

    def test_email(self):
        self.exp = self.v.start_of_line().word().then('@').word().then('.').word().end_of_line().regex()
        self.assertRegexpMatches('mail@mail.com', self.exp, 'Not a valid email')

    def test_url(self):
        self.exp = self.v.start_of_line().then('http').maybe('s').then('://').maybe('www.').word().then('.').word().maybe('/').end_of_line().regex()
        self.assertRegexpMatches('https://www.google.com/', self.exp, 'Not a valid email')
