# pyright: reportPrivateUsage=false
# flake8: noqa
# type: ignore
import re
import unittest

from verbex import CharClass, SpecialChar, Verbex


class verbexTest(unittest.TestCase):
    """Tests for verbal_expressions.py"""

    # def setUp(self):
    #     Verbex() = Verbex()

    # def tearDown(self):
    #     ...
    #     # Verbex() = None
    #     # self.exp = None

    def test_should_render_verbex_as_string(self):
        self.assertEqual(str(Verbex()._add("^$")), "^$")  # noqa

    def test_should_render_verbex_list_as_string(self):
        self.assertEqual(str(Verbex()._add(["^", "[0-9]", "$"])), "^[0-9]$")  # noqa

    def test_should_match_characters_in_range(self):
        regex = Verbex().letter_range("a", "c").regex()
        for character in ["a", "b", "c"]:
            self.assertRegex(character, regex)

    def test_should_not_match_characters_outside_of_range(self):
        regex = Verbex().letter_range("a", "c").regex()
        self.assertNotRegex("d", regex)

    def test_should_match_start_of_line(self):
        regex = Verbex().find(SpecialChar.START_OF_LINE).find("text ").regex()
        self.assertRegex("text ", regex)

    def test_should_match_end_of_line(self):
        regex = Verbex().find("test").find(SpecialChar.END_OF_LINE).regex()
        self.assertRegex("IGNORE   test", regex)

    def test_should_match_anything(self):
        regex = Verbex().anything().regex()
        self.assertIsNotNone(re.fullmatch(regex, "!@#$%¨&*()__+{}"))

    def test_should_match_anything_but_specified_element_when_element_is_not_found(  # noqa: E501
        self,
    ):
        regex = Verbex().anything_but("X").find(" Files").regex()
        self.assertRegex("Y Files", regex)
        self.assertNotRegex("X Files", regex)

    def test_should_not_match_anything_but_specified_element_when_specified_element_is_found(  # noqa: E501
        self,
    ):
        regex = Verbex().anything_but("X").regex()
        self.assertRegex("Y Files", regex)
        self.assertNotRegex("X", regex)

    def test_should_find_element(self):
        regex = Verbex().find("Wally").regex()
        self.assertRegex("Wally", regex)
        self.assertNotRegex("Nally", regex)

    def test_should_not_find_missing_element(self):
        regex = Verbex().find("Wally").regex()
        self.assertNotRegex("Wall-e", regex)

    def test_should_match_when_maybe_element_is_present(self):
        regex = (
            Verbex()
            .start_of_line()
            .find("Python2.")
            .maybe("7")
            .end_of_line()
            .regex()  #
        )
        self.assertRegex("Python2.7", regex)

    def test_should_match_when_maybe_element_is_missing(self):
        regex = (
            Verbex()
            .start_of_line()
            .find("Python2.")
            .maybe("7")
            .end_of_line()
            .regex()  #
        )
        self.assertRegex("Python2.", regex)

    def test_should_match_on_any_when_element_is_found(self):
        regex = (
            Verbex()
            .start_of_line()
            .any_of("Q")
            .anything()
            .end_of_line()
            .regex()  # E501      #
        )
        self.assertRegex("Query", regex)

    def test_should_not_match_on_any_when_element_is_not_found(self):
        regex = (
            Verbex()
            .start_of_line()
            .any_of("Q")
            .anything()
            .end_of_line()
            .regex()  # E501      #
        )
        self.assertNotRegex("W", regex)

    def test_should_match_when_line_break_present(self):
        regex = (
            Verbex()
            .start_of_line()
            .anything()
            .line_break()
            .anything()
            .end_of_line()
            .regex()
        )
        self.assertRegex("Marco \n Polo", regex)
        self.assertNotRegex("Marco Polo", regex)

    def test_should_match_when_line_break_and_carriage_return_present(self):
        regex = (
            Verbex()
            .start_of_line()
            .anything()
            .line_break()
            .anything()
            .end_of_line()
            .regex()
        )
        self.assertRegex("Marco \r\n Polo", regex)

    def test_should_not_match_when_line_break_is_missing(self):
        regex = (
            Verbex()
            .start_of_line()
            .anything()
            .line_break()
            .anything()
            .end_of_line()
            .regex()
        )
        self.assertNotRegex("Marco Polo", regex)

    def test_should_match_when_tab_present(self):
        regex = (
            Verbex()
            .start_of_line()
            .anything()
            .as_few()
            .find("!")
            .tab()
            .end_of_line()
            .regex()  # E501 #
        )
        self.assertRegex("One tab only!\t", regex)
        self.assertNotRegex("One tab only!\t\t", regex)

    def test_should_not_match_when_tab_is_missing(self):
        regex = Verbex().start_of_line().anything().tab().end_of_line().regex()
        self.assertNotRegex("No tab here", regex)

    def test_should_match_when_word_present(self):
        regex = Verbex().start_of_line().word().end_of_line().regex()
        self.assertRegex("Oneword", regex)

    def test_not_match_when_two_words_are_present_instead_of_one(self):
        regex = Verbex().start_of_line().word().end_of_line().regex()
        self.assertNotRegex("Two words", regex)

    def test_should_match_when_or_condition_fulfilled(self):
        regex = (
            Verbex()
            .start_of_line()
            .find("G")
            .OR(Verbex().find("H"))
            .anything()
            .as_few()
            .find("b")
            .end_of_line()
            .regex()
        )
        self.assertRegex("Github", regex)
        self.assertRegex("Hithub", regex)

    def test_should_not_match_when_or_condition_not_fulfilled(self):
        regex = (
            Verbex()
            .start_of_line()
            .find("G")
            .OR(Verbex().find("H"))
            .anything()
            .as_few()
            .find("b")
            .end_of_line()
            .regex()
        )
        self.assertNotRegex("ithub", regex)

    def test_should_match_on_upper_case_when_lower_case_is_given_and_any_case(
        self,
    ):
        regex = (
            Verbex()
            .start_of_line()
            .find("THOR")
            .end_of_line()
            .with_any_case()
            .regex()  # E501 #
        )
        self.assertRegex("thor", regex)

    def test_should_not_match_on_upper_case_when_lower_case_is_given(
        self,
    ):
        regex = Verbex().start_of_line().find("THOR").end_of_line().regex()
        self.assertNotRegex("thor", regex)

    def test_should_match_multiple_lines(self):
        regex = (
            Verbex()
            .start_of_line()
            .anything()
            .find("Pong")
            .anything()
            .end_of_line()
            .search_by_line()
            .regex()
        )
        self.assertRegex("Ping \n Pong \n Ping", regex)

    def test_should_not_match_multiple_lines(self):
        regex = (
            Verbex()
            .start_of_line()
            .anything()
            .find("Pong")
            .anything()
            .end_of_line()
            .regex()
        )
        self.assertNotRegex("Ping \n Pong \n Ping", regex)

    def test_should_match_email_like(self):
        regex = (
            Verbex()
            .start_of_line()
            .one_or_more(Verbex().any_of(CharClass.LETTER))
            .then("@")
            .one_or_more(Verbex().any_of(CharClass.LETTER))
            .then(".")
            .one_or_more(Verbex().any_of(CharClass.LETTER))
            .end_of_line()
            .regex()
        )
        self.assertRegex("mail@mail.com", regex)

    def test_should_match_url(self):
        regex = (
            Verbex()
            .start_of_line()
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
        self.assertRegex("https://www.google.com/", regex)
        self.assertNotRegex("htps://www.google.com/", regex)

    def test_followed_by(self):
        regex = Verbex().find("!").followed_by(":").regex()
        self.assertRegex("!:", regex)
        self.assertNotRegex("! :", regex)

    def test_not_followed_by(self):
        regex = Verbex().find("!").not_followed_by(":").regex()
        self.assertNotRegex("!:", regex)
        self.assertRegex("! :", regex)

    def test_preceded_by(self):
        regex = Verbex().preceded_by("!").find(":").regex()
        self.assertRegex("!:", regex)
        self.assertNotRegex("! :", regex)

    def test_not_preceded_by(self):
        regex = Verbex().not_preceded_by("!").find(":").regex()
        self.assertNotRegex("!:", regex)
        self.assertRegex("! :", regex)


if __name__ == "__main__":
    unittest.main()
