""" Definitions for the string transformation language """
# src/language/expressions.py

from typing import Union
from enum import Enum

class Expr:
    def __repr__(self) -> str:
        """ Virtual method __repr__ """
        raise RuntimeError("Expressions must implement \"__repr__\"")

class StringExpr(Expr):
    """ top-level expression """
    def __init__(
        self,
        substr_exprs: list[Union['SubStringExpr', 'ConstStringExpr']] = []
    ):
        self.substr_exprs = substr_exprs

    def add_substr(self, substr_expr):
        """ add a new substring expression to the expression """
        self.substr_exprs.append(substr_expr)

    def __repr__(self) -> str:
        """ Output a BlinkFill-formatted formula """
        return f"{' '.join(se.__repr__ for se in self.substr_exprs)}"

class ConstStringExpr(Expr):
    """ Constant string sub expression """
    def __init__(
        self,
        string: str
    ):
        self.const_str = string

    def __repr__(self) -> str:
        return f"ConstStr({self.const_str})"

class SubStringExpr(Expr):
    """ Substring Expression """
    def __init__(
        self,
        substr: str,
        left: set['PosExpr'],
        right: set['PosExpr']
    ):
        self.v = substr
        self.pl = left
        self.pr = right

    def __repr__(self) -> str:
        return f"SubStr({self.v}, {self.pl.__repr__}, {self.pr.__repr__}"

class PosExpr(Expr):
    """ Position Expression w/ Token """
    def __init__(self,
        tok,
        idx,
        direction: 'Direction'
    ):
        self.tok = tok
        self.idx = idx
        self.direction = direction

    def __repr__(self) -> str:
        return f"({self.tok},{self.idx},{self.direction.value}"

class ConstPosExpr(Expr):
    """ Constant Position Expression """
    def __init__(self,
        idx
    ):
        self.idx = idx

    def __repr__(self) -> str:
        return f"ConstPos({self.idx})"

class Direction(Enum):
    Start = "Start"
    End = "End"
