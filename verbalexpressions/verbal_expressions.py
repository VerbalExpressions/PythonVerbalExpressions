import re


def re_escape(fn):
    def arg_escaped(this, *args):
        t = [isinstance(a, VerEx) and a.s or re.escape(str(a)) for a in args]
        return fn(this, *t)

    return arg_escaped


class VerEx(object):
    """
    --- VerbalExpressions class ---
    the following methods behave different from the original js lib!

    - end_of_line
    - start_of_line
    - or
    when you say you want `$`, `^` and `|`, we just insert it right there.
    No other tricks.

    And any string you inserted will be automatically grouped
    except `tab` and `add`.
    """

    def __init__(self):
        self.s = []
        self.modifiers = {"I": 0, "M": 0, "A": 0}

    def __getattr__(self, attr):
        """ any other function will be sent to the regex object """
        regex = self.regex()
        return getattr(regex, attr)

    def __str__(self):
        return "".join(self.s)

    def add(self, value):
        if isinstance(value, list):
            self.s.extend(value)
        else:
            self.s.append(value)
        return self

    def regex(self):
        """ get a regular expression object. """
        return re.compile(
            str(self),
            self.modifiers["I"] | self.modifiers["M"] | self.modifiers["A"],
        )

    compile = regex

    def source(self):
        """ return the raw string """
        return str(self)

    raw = value = source

    # ---------------------------------------------

    def anything(self):
        return self.add("(.*)")

    @re_escape
    def anything_but(self, value):
        return self.add("([^%s]*)" % value)

    def end_of_line(self):
        return self.add("$")

    @re_escape
    def maybe(self, value):
        return self.add("(%s)?" % value)

    def start_of_line(self):
        return self.add("^")

    @re_escape
    def find(self, value):
        return self.add("(%s)" % value)

    then = find

    # special characters and groups

    @re_escape
    def any(self, value):
        return self.add("([%s])" % value)

    any_of = any

    def line_break(self):
        return self.add(r"(\n|(\r\n))")

    br = line_break

    @re_escape
    def range(self, *args):
        from_tos = [args[i : i + 2] for i in range(0, len(args), 2)]
        return self.add("([%s])" % "".join(["-".join(i) for i in from_tos]))

    def tab(self):
        return self.add(r"\t")

    def word(self):
        return self.add(r"(\w+)")

    def OR(self, value=None):
        """ `or` is a python keyword so we use `OR` instead. """
        self.add("|")
        return self.find(value) if value else self

    def replace(self, string, repl):
        return self.sub(repl, string)

    # --------------- modifiers ------------------------

    # no global option. It depends on which method
    # you called on the regex object.

    def with_any_case(self, value=False):
        self.modifiers["I"] = re.I if value else 0
        return self

    def search_one_line(self, value=False):
        self.modifiers["M"] = re.M if value else 0
        return self

    def with_ascii(self, value=False):
        self.modifiers["A"] = re.A if value else 0
        return self
