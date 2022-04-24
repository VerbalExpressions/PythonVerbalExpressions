from __future__ import annotations

import re
from enum import Enum
from functools import wraps
from typing import Protocol

try:
    from beartype import beartype  # type: ignore
    from beartype.typing import (  # type: ignore
        Any,
        Callable,
        Dict,
        Iterator,
        List,
        Optional,
        ParamSpec,
        Tuple,
        TypeVar,
        Union,
        cast,
        runtime_checkable,
    )
except ModuleNotFoundError:
    from typing import (
        Any,
        Callable,
        Dict,
        Iterator,
        List,
        Optional,
        ParamSpec,
        Tuple,
        TypeVar,
        Union,
        cast,
        runtime_checkable,
    )

    __P = ParamSpec("__P")
    __R = TypeVar("__R")

    def noop_dec(func: Callable[__P, __R]) -> Callable[__P, __R]:
        return func

    beartype = noop_dec  # type: ignore


P = ParamSpec("P")
R = TypeVar("R")


# work around for bug https://github.com/python/mypy/issues/12660
@runtime_checkable
class HasIter(Protocol):
    def __iter__(self) -> Iterator[Any]:
        ...


# work around for bug https://github.com/python/mypy/issues/12660
@runtime_checkable
class HasItems(Protocol):
    def items(self) -> Tuple[str, Any]:
        ...


class EscapedText(str):
    def __new__(cls, value: str):
        return str.__new__(cls, re.escape(value))


def re_escape(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        escaped_args: List[Any] = []
        escaped_kwargs: Dict[str, Any] = {}
        for arg in cast(HasIter, args):
            if isinstance(arg, str):
                escaped_args.append(EscapedText(re.escape(arg)))
            else:
                escaped_args.append(arg)
        arg_k: str
        arg_v: Any
        for arg_k, arg_v in cast(HasItems, kwargs).items():
            if isinstance(arg_v, str):
                escaped_kwargs[arg_k] = EscapedText(re.escape(str(arg_v)))
            else:
                escaped_kwargs[arg_k] = arg_v
        return func(*escaped_args, **escaped_kwargs)  # type: ignore

    return inner


class CharClass(Enum):
    DIGIT = "\\d"
    LETTER = "\\w"
    UPPERCASE_LETTER = "\\u"
    LOWERCASE_LETTER = "\\l"
    WHITESPACE = "\\s"
    TAB = "\\t"

    def __str__(self):
        return self.value


class SpecialChar(Enum):
    # does not work  / should not be used in [ ]
    LINEBREAK = "(\\n|(\\r\\n))"
    START_OF_LINE = "^"
    END_OF_LINE = "$"

    def __str__(self):
        return self.value


CharClassOrChars = Union[str, CharClass]
EscapedCharClassOrSpecial = Union[str, CharClass, SpecialChar]
VerbexEscapedCharClassOrSpecial = Union["Verbex", EscapedCharClassOrSpecial]


class Verbex:
    """
    VerbalExpressions class.
    the following methods do not try to match the original js lib!
    """

    @re_escape
    @beartype
    def __init__(self, modifiers: re.RegexFlag = re.RegexFlag(0)):
        # self._parts: List[str] = [text]
        self._parts: List[str] = []
        self._modifiers = modifiers

    @property
    def modifiers(self) -> re.RegexFlag:
        return self._modifiers

    def __str__(self):
        """Return regex string representation."""
        return "".join(self._parts)

    @beartype
    def __add(self, value: Union[str, List[str]]):
        """
        Append a transformed value to internal expression to be compiled.

        As possible, this method should be "private".
        """
        if isinstance(value, list):
            self._parts.extend(value)
        else:
            self._parts.append(value)
        return self

    def regex(self):
        """get a regular expression object."""
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
        return self.__add(f"(?<{name}>{str(text)})")

    @re_escape
    @beartype
    def _capture_group_without_name(
        self,
        text: VerbexEscapedCharClassOrSpecial,
    ) -> Verbex:
        return self.__add(f"({str(text)})")

    @re_escape
    @beartype
    def capture_group(
        self,
        /,
        name_or_text: Union[
            Optional[str], VerbexEscapedCharClassOrSpecial
        ] = None,
        text: Optional[VerbexEscapedCharClassOrSpecial] = None,
    ) -> Verbex:
        if name_or_text is not None:
            if text is None:
                _text = name_or_text
                return self._capture_group_without_name(_text)
            if isinstance(name_or_text, str):
                return self._capture_group_with_name(name_or_text, text)
        raise ValueError("text must be specified with optional name")

    @re_escape
    @beartype
    def OR(self, text: VerbexEscapedCharClassOrSpecial):  # noqa N802
        """`or` is a python keyword so we use `OR` instead."""
        self.__add("|")
        self.find(text)

    @re_escape
    @beartype
    def zero_or_more(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        return self.__add(f"(?:{str(text)})*")

    @re_escape
    @beartype
    def one_or_more(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        return self.__add(f"(?:{str(text)})+")

    @re_escape
    @beartype
    def n_times(self, text: VerbexEscapedCharClassOrSpecial, n: int) -> Verbex:
        return self.__add(f"(?:{str(text)}){{{n}}}")

    @re_escape
    @beartype
    def n_times_or_more(
        self, text: VerbexEscapedCharClassOrSpecial, n: int
    ) -> Verbex:
        return self.__add(f"(?:{str(text)}){{{n},}}")

    @re_escape
    @beartype
    def n_to_m_times(
        self, text: VerbexEscapedCharClassOrSpecial, n: int, m: int
    ) -> Verbex:
        return self.__add(f"(?:{str(text)}){{{n},{m}}}")

    @re_escape
    def anything_but(self, text: EscapedCharClassOrSpecial):
        return self.__add(f"[^{text}]*")

    @re_escape
    @beartype
    def maybe(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        # if isinstance(text, Verbex):
        #     return self.__add(f"(?:{str(text)})?")
        return self.__add(f"(?:{str(text)})?")

    @re_escape
    @beartype
    def find(self, text: VerbexEscapedCharClassOrSpecial) -> Verbex:
        return self.__add(str(text))

    # only allow CharclassOrChars

    @re_escape
    @beartype
    def any_of(self, text: CharClassOrChars) -> Verbex:
        return self.__add(f"(?:[{text}])")

    @re_escape
    @beartype
    def not_any_of(self, text: CharClassOrChars) -> Verbex:
        return self.__add(f"(?:[^{text}])")

    # no text input

    def anything(self) -> Verbex:
        return self.__add(".*")

    def asfew(self) -> Verbex:
        return self.__add("?")

    @beartype
    def range(self, start: int, end: int) -> Verbex:
        return self.__add(
            "(?:" + "|".join(str(i) for i in range(start, end + 1)) + ")"
        )

    def word(self) -> Verbex:
        return self.__add("(\\b\\w+\\b)")

    # # --------------- modifiers ------------------------

    def with_any_case(self) -> Verbex:
        self._modifiers |= re.IGNORECASE
        return self

    def search_by_line(self) -> Verbex:
        self._modifiers |= re.MULTILINE
        return self

    def with_ascii(self) -> Verbex:
        self._modifiers |= re.ASCII
        return self


# left over notes from original version
# def __getattr__(self, attr):
#     """ any other function will be sent to the regex object """
#     regex = self.regex()
#     return getattr(regex, attr)

# def range(self, start: int, end: int) -> Verbex:
#     # this was the original? method
#     from_tos = [args[i : i + 2] for i in range(0, len(args), 2)]
#     return self.__add("([%s])" % "".join(["-".join(i) for i in from_tos]))

# def replace(self, string, repl):
#     return self.sub(repl, string)


t = (
    # Verbex().maybe(Verbex().find("tet"))
    Verbex().capture_group(
        "test",
        Verbex().find("what to find"),
    )
    # Verbex()
    # .with_any_case()
    # .maybe("test")
    # .find(RegexEnum.DIGIT)
    # .any("test")
    # .range(10, 20)
)
print(t)
