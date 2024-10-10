""" Contains base token regexes """
# language/base_tokens.py

from enum import Enum
import re

class BaseTokens(Enum):
    """ Enumeration for all of the base token Regexes

        Enums are singletons, so no worry about compiling
    """
    ProperCase = re.compile(r"""
                    [A-Z]           # singular upper case
                    [a-z]+          # one or more lower case
                    """,
                    re.VERBOSE
                )
    Caps = re.compile(r"""
                    [A-Z]+          # one or more upper case
                    """,
                    re.VERBOSE
                )
    LowerCase = re.compile(r"""
                    [a-z]+          # one ore more lower case
                    """,
                    re.VERBOSE
                )
    Digits = re.compile(r"""
                    \d+             # one or more digit
                    """,
                    re.VERBOSE
                )
    Alphabets = re.compile(r"""
                    [A-Za-z]        # all alphabets
                    """,
                    re.VERBOSE
                )
    Alphanumeric = re.compile(r"""
                    [A-Za-z0-9]+    # all alpha + digits
                    """,
                    re.VERBOSE
                )
    Whitespace = re.compile(r"""
                    \s+             # one or more whitespace
                    """,
                    re.VERBOSE
                )
    StartT = re.compile(r"""
                    ^               # start token
                    """,
                    re.VERBOSE
                )
    EndT = re.compile(r"""
                    $               # end token
                    """,
                    re.VERBOSE
                )
    ProperCaseWSpaces = re.compile(r"""
                    %s              # placeholder for ProperCase
                    (%s%s)*         # placeholder for 0 or more ProperCase,WhiteSpace
                    """ %
                    (ProperCase.pattern, Whitespace.pattern, ProperCase.pattern),
                    re.VERBOSE
                )

    CapsWSpaces = re.compile(r"""
                    %s              # placeholder for Caps
                    (%s%s)*         # placeholder for 0 or more Caps,WhiteSpace
                    """ %
                    (Caps.pattern, Whitespace.pattern, Caps.pattern),
                    re.VERBOSE
                )
    LowerCaseWSpaces = re.compile(r"""
                    %s              # placeholder for lowercase
                    (%s%s)*         # placeholder for 0 or more lowercase,WhiteSpace
                    """ %
                    (LowerCase.pattern, Whitespace.pattern, LowerCase.pattern),
                    re.VERBOSE
                )
    AlphabetsWSpaces = re.compile(r"""
                    %s              # placeholder for Alphabet
                    (%s%s)*         # placeholder for 0 or more Alphabet,WhiteSpace
                    """ %
                    (Alphabets.pattern, Whitespace.pattern, Alphabets.pattern),
                    re.VERBOSE
                )

# to do matches, do BaseToken.Caps.value.match/search/etc
