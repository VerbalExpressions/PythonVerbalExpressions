"""Generate regular expressions from an easier fluent verbal form."""
from __future__ import annotations

import re
from enum import Enum
from functools import wraps

try:
    from typing import (  # <--------------- if Python ≥ 3.9.0
        Annotated,
        ParamSpec,
        Protocol,
        TypeAlias,
        runtime_checkable,
    )
except ImportError:
    from typing_extensions import TypeAlias, Protocol, Annotated, ParamSpec, runtime_checkable  # type: ignore # <--- if Python < 3.9.0 # noqa E501

from typing import Pattern, TypeVar

from beartype import beartype  # type: ignore
from beartype.typing import (  # type: ignore
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
    cast,
)
from beartype.vale import Is  # type: ignore


def _string_len_is_1(text: object) -> bool:
    return isinstance(text, str) and len(text) == 1


Char = Annotated[str, Is[_string_len_is_1]]


P = ParamSpec("P")  # noqa VNE001
R = TypeVar("R")  # noqa VNE001


# work around for bug https://github.com/python/mypy/issues/12660
# fixed in next version of mypy.
@runtime_checkable
class HasIter(Protocol):
    """Workaround for mypy P.args."""

    def __iter__(self) -> Iterator[Any]:
        """Object can be iterated.

        Yields:
            Next object.
        """
        ...


# work around for bug https://github.com/python/mypy/issues/12660
# fixed in next version of mypy
@runtime_checkable
class HasItems(Protocol):
    """Workaround for mypy P.kwargs."""

    def items(self) -> Tuple[str, Any]:
        """Object has items method.

        Returns:
            The dict of items.
        """
        ...


class EscapedText(str):
    """Text that has been escaped for regex.

    Arguments:
        str -- Extend the string class.
    """

    def __new__(cls, value: str) -> EscapedText:
        """Return a escaped regex string.

        Arguments:
            value -- the string to escape

        Returns:
            _description_
        """
        return str.__new__(cls, re.escape(value))


def re_escape(func: Callable[P, R]) -> Callable[P, R]:
    """Automatically escape any string parameters as EscapedText.

    Arguments:
        func -- The function to decorate.

    Returns:
        The decorated function.
    """

    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:  # type: ignore
        escaped_args: List[Any] = []
        escaped_kwargs: Dict[str, Any] = {}
        for arg in cast(HasIter, args):
            if not isinstance(arg, EscapedText) and isinstance(arg, str):
                escaped_args.append(EscapedText(arg))
            else:
                escaped_args.append(arg)
        arg_k: str
        arg_v: Any
        for arg_k, arg_v in cast(HasItems, kwargs).items():
            if not isinstance(arg_v, EscapedText) and isinstance(arg_v, str):
                escaped_kwargs[arg_k] = EscapedText(str(arg_v))
            else:
                escaped_kwargs[arg_k] = arg_v
        return func(*escaped_args, **escaped_kwargs)  # type: ignore

    return inner


class CharClass(Enum):
    """Enum of character classes in regex.

    Arguments:
        Enum -- Extends the Enum class.
    """

    DIGIT = "\\d"
    LETTER = "\\w"
    UPPERCASE_LETTER = "\\u"
    LOWERCASE_LETTER = "\\l"
    WHITESPACE = "\\s"
    TAB = "\\t"

    def __str__(self) -> str:
        """To string method based on Enum value.

        Returns:
            value of Enum
        """
        return self.value


class SpecialChar(Enum):
    """Enum of special charaters, shorthand.

    Arguments:
        Enum -- Extends the Enum class.
    """

    # does not work  / should not be used in [ ]
    LINEBREAK = "(\\n|(\\r\\n))"
    START_OF_LINE = "^"
    END_OF_LINE = "$"
    TAB = "\t"

    def __str__(self) -> str:
        """To string for special chars enum.

        Returns:
            Return value of enum as string.
        """
        return self.value


CharClassOrChars: TypeAlias = Union[str, CharClass]
EscapedCharClassOrSpecial: TypeAlias = Union[str, CharClass, SpecialChar]
VerbexEscapedCharClassOrSpecial: TypeAlias = Union["Verbex", EscapedCharClassOrSpecial]


def _poseur_decorator(*poseur: Any) -> Any:
    """Positional-only arguments runtime checker."""
    import functools

    def caller(func: Callable[P, R]) -> Callable[P, R]:  # type: ignore
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            poseur_args = set(poseur).intersection(kwargs)  # type: ignore
            if poseur_args:
                raise TypeError(
                    "%s() got some positional-only arguments passed as keyword"
                    " arguments: %r" % (func.__name__, ", ".join(poseur_args)),
                )
            return func(*args, **kwargs)  # type: ignore

        return wrapper

    return caller


class Verbex:
    """
    VerbalExpressions class.

    the following methods do not try to match the original js lib!
    """

    EMPTY_REGEX_FLAG = re.RegexFlag(0)

    @re_escape
    @beartype
    def __init__(self, modifiers: re.RegexFlag = EMPTY_REGEX_FLAG):
        """Create a Verbex object; setting any needed flags.

        Keyword Arguments:
            modifiers -- Regex modifying flags (default: {re.RegexFlag(0)})
        """
        # self._parts: List[str] = [text]
        self._parts: List[str] = []
        self._modifiers = modifiers

    @property
    def modifiers(self) -> re.RegexFlag:
        """Return the modifiers for this Verbex object.

        Returns:
            The modifiers applied to this object.
        """
        return self._modifiers

    def __str__(self) -> str:
        """Return regex string representation."""
        return "".join(self._parts)

    @beartype
    def _add(self, value: Union[str, List[str]]) -> Verbex:
        """
        Append a transformed value to internal expression to be compiled.

        As possible, this method should be "private".
        """
        if isinstance(value, list):
            self._parts.extend(value)
        else:
            self._parts.append(value)
        return self

    def regex(self) -> Pattern[str]:
        """Get a regular expression object."""
        return re.compile(
            str(self),
            self._modifiers,
        )

    # allow VerbexEscapedCharClassOrSpecial

    @re_escape
    @beartype
    def _capture_group_with_name(
        self,
        name: str,
        text: VerbexEscapedCharClassOrSpecial,
    ) -> Verbex:
        return self._add(f"(?<{name}>{str(text)})")

    @re_escape
    @beartype
    def _capture_group_without_name(
        self,
        text: VerbexEscapedCharClassOrSpecial,
    ) -> Verbex:
        return self._add(f"({str(text)})")

    @re_escape
    @beartype
    @_poseur_decorator("self")
    def capture_group(
        self,
        name_or_text: Union[Optional[str], VerbexEscapedCharClassOrSpecial] = None,
        text: Optional[VerbexEscapedCharClassOrSpecial] = None,
    ) -> Verbex:
        """Create a capture group.

        Name is optional if not specified then the first argument is the text.

        Keyword Arguments:
            name_or_text -- The name of the group / text to search for (default: {None})
            text -- The text to search for (default: {None})

        Raises:
            ValueError: If name is specified then text must be as well.

        Returns:
            Verbex with added capture group.
        """
        if name_or_text is not None:
            if text is None:
                _text = name_or_text
                return self._capture_group_without_name(_text)
            if isinstance(name_or_text, str):
                return self._capture_group_with_name(name_or_text, text)
        raise ValueError("text must be specified with optional name")

    @re_escape
    @beartype
    def OR(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:  # noqa N802
        """`or` is a python keyword so we use `OR` instead.

        Arguments:
            text -- Text to find or a Verbex object.

        Returns:
            Modified Verbex object.
        """
        return self._add("|").find(text)

    @re_escape
    @beartype
    def zero_or_more(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Find the text or Verbex object zero or more times.

        Arguments:
            text -- The text / Verbex object to look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?:{str(text)})*")

    @re_escape
    @beartype
    def one_or_more(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Find the text or Verbex object one or more times.

        Arguments:
            text -- The text / Verbex object to look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?:{str(text)})+")

    @re_escape
    @beartype
    def n_times(
        self,
        text: VerbexEscapedCharClassOrSpecial,
        n: int,  # noqa: VNE001
    ) -> Verbex:
        """Find the text or Verbex object n or more times.

        Arguments:
            text -- The text / Verbex object to look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?:{str(text)}){{{n}}}")

    @re_escape
    @beartype
    def n_times_or_more(
        self,
        text: VerbexEscapedCharClassOrSpecial,
        n: int,  # noqa: VNE001
    ) -> Verbex:
        """Find the text or Verbex object at least n times.

        Arguments:
            text -- The text / Verbex object to look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?:{str(text)}){{{n},}}")

    @re_escape
    @beartype
    def n_to_m_times(
        self,
        text: VerbexEscapedCharClassOrSpecial,
        n: int,  # noqa: VNE001
        m: int,  # noqa: VNE001
    ) -> Verbex:
        """Find the text or Verbex object between n and m times.

        Arguments:
            text -- The text / Verbex object to look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?:{str(text)}){{{n},{m}}}")

    @re_escape
    @beartype
    def maybe(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Possibly find the text / Verbex object.

        Arguments:
            text -- The text / Verbex object to possibly find.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?:{str(text)})?")

    @re_escape
    @beartype
    def find(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Find the text or Verbex object.

        Arguments:
            text -- The text / Verbex object to look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(str(text))

    @re_escape
    @beartype
    def then(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Synonym for find.

        Arguments:
            text -- The text / Verbex object to look for.

        Returns:
            Modified Verbex object.
        """
        return self.find(text)

    @re_escape
    @beartype
    def followed_by(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Match if string is followed by text.

        Positive lookahead

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?={text})")

    @re_escape
    @beartype
    def not_followed_by(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Match if string is not followed by text.

        Negative lookahead

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?!{text})")

    @re_escape
    @beartype
    def preceded_by(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Match if string is not preceded by text.

        Positive lookbehind

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?<={text})")

    @re_escape
    @beartype
    def not_preceded_by(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        """Match if string is not preceded by text.

        Negative Lookbehind

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?<!{text})")

    # only allow CharclassOrChars

    @re_escape
    @beartype
    def any_of(self, chargroup: CharClassOrChars) -> Verbex:
        """Find anything in this group of chars or char class.

        Arguments:
            text -- The characters to look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?:[{chargroup}])")

    @re_escape
    @beartype
    def not_any_of(self, text: CharClassOrChars) -> Verbex:
        """Find anything but this group of chars or char class.

        Arguments:
            text -- The characters to not look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"(?:[^{text}])")

    @re_escape
    def anything_but(self, chargroup: EscapedCharClassOrSpecial) -> Verbex:
        """Find anything one or more times but this group of chars or char class.

        Arguments:
            text -- The characters to not look for.

        Returns:
            Modified Verbex object.
        """
        return self._add(f"[^{chargroup}]+")

    # no text input

    def start_of_line(self) -> Verbex:
        """Find the start of the line.

        Returns:
            Modified Verbex object.
        """
        return self.find(SpecialChar.START_OF_LINE)

    def end_of_line(self) -> Verbex:
        """Find the end of the line.

        Returns:
            Modified Verbex object.
        """
        return self.find(SpecialChar.END_OF_LINE)

    def line_break(self) -> Verbex:
        """Find a line break.

        Returns:
            Modified Verbex object.
        """
        return self.find(SpecialChar.LINEBREAK)

    def tab(self) -> Verbex:
        """Find a tab.

        Returns:
            Modified Verbex object.
        """
        return self.find(SpecialChar.TAB)

    def anything(self) -> Verbex:
        """Find anything one or more time.

        Returns:
            Modified Verbex object.
        """
        return self._add(".+")

    def as_few(self) -> Verbex:
        """Modify previous search to not be greedy.

        Returns:
            Modified Verbex object.
        """
        return self._add("?")

    @beartype
    def number_range(self, start: int, end: int) -> Verbex:
        """Generate a range of numbers.

        Arguments:
            start -- Start of the range
            end -- End of the range

        Returns:
            Modified Verbex object.
        """
        return self._add("(?:" + "|".join(str(i) for i in range(start, end + 1)) + ")")

    @beartype
    def letter_range(self, start: Char, end: Char) -> Verbex:
        """Generate a range of letters.

        Arguments:
            start -- Start of the range
            end -- End of the range

        Returns:
            Modified Verbex object.
        """
        return self._add(f"[{start}-{end}]")

    def word(self) -> Verbex:
        """Find a word on word boundary.

        Returns:
            Modified Verbex object.
        """
        return self._add("(\\b\\w+\\b)")

    # # --------------- modifiers ------------------------

    def with_any_case(self) -> Verbex:
        """Modify Verbex object to be case insensitive.

        Returns:
            Modified Verbex object.
        """
        self._modifiers |= re.IGNORECASE
        return self

    def search_by_line(self) -> Verbex:
        """Search each line, ^ and $ match begining and end of line respectively.

        Returns:
            Modified Verbex object.
        """
        self._modifiers |= re.MULTILINE
        return self

    def with_ascii(self) -> Verbex:
        """Match ascii instead of unicode.

        Returns:
            Modified Verbex object.
        """
        self._modifiers |= re.ASCII
        return self


# left over notes from original version
# def __getattr__(self, attr):
#     """ any other function will be sent to the regex object """
#     regex = self.regex()
#     return getattr(regex, attr)

# def replace(self, string, repl):
#     return self.sub(repl, string)


if __name__ == "__main__":
    pass
