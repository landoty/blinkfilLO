""" Definitions for the string transformation language """
# src/language/expressions.py
import pdb
from typing import Union
from enum import Enum
from .base_tokens import BaseTokens

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

    def to_formula(self) -> str:
        """ Convert to a LibreOffice formula """
        formula = "CONCAT("
        for expr in self.substr_exprs:
            if isinstance(expr, SubStringExpr):
                substr = "MID(<input>,"
                best = []
                # check all left
                for l in expr.pl:
                    if len(l) > len(best):
                        best = l

                left_index = best.to_formula()
                substr += f"{left_index},"

                # check all right
                best = []
                for r in expr.pr:
                    if len(r) > len(best):
                        best = r

                right_index = best.to_formula()

                substr += f"{right_index}-({left_index})"
                formula += f"{substr})"
                formula += ","

            elif isinstance(expr, ConstStringExpr):
                formula += expr.to_formula()
                formula += ","

        formula = formula[0:-1]
        formula += ")"
        return formula

    def __repr__(self) -> str:
        """ Output a BlinkFill-formatted formula """
        return f"{' '.join(se.__repr__() for se in self.substr_exprs)}"

class ConstStringExpr(Expr):
    """ Constant string sub expression """
    def __init__(
        self,
        string: str
    ):
        self.const_str = string

    def __key(self):
        return self.const_str

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self) -> str:
        return f"ConstStr({self.const_str})"

    def __eq__(self, other) -> bool:
        if hasattr(other, "const_str"):
            return self.const_str == other.const_str
        return False

    def __len__(self) -> int:
        return len(self.const_str)

    def to_formula(self) -> str:
        return f"\"{self.const_str}\""

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
        return f"SubStr({self.pl.__repr__()}, {self.pr.__repr__()}"

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other) -> bool:
        if isinstance(other, SubStringExpr):
            return self.pl == other.pl and self.pr == other.pr
        return False

    def __len__(self) -> int:
        return len(self.v)

    @staticmethod
    def intersect(substr1, substr2) -> 'SubStringExpr':
        """ intersect two substring expressions """
        if not hasattr(substr1, "pl") or not hasattr(substr2, "pl"):
            return None

        left = substr1.pl & substr2.pl
        if len(left) == 0:
            return None

        right = substr1.pr & substr2.pr
        if len(right) == 0:
            return None

        max_substr = substr1.v if len(substr1.v) > len(substr2.v) else substr2.v
        return SubStringExpr(
                    substr = max_substr,
                    left=left,
                    right=right
                )

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
        return f"PosExpr('{self.tok}',{self.idx},{self.direction.value})"

    def __key(self):
        return (self.tok,self.idx,self.direction.value)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, PosExpr):
            return self.tok == other.tok  and \
                    self.idx == other.idx and \
                    self.direction == other.direction
        return False

    def __len__(self) -> int:
        return len(self.tok)

    def to_formula(self) -> str:
        # special case if token is the start or end token
        if self.tok == BaseTokens.StartT.name:
            return "0+1"
        elif self.tok == BaseTokens.EndT.name:
            return "LEN(<input>)"

        formula = "SEARCH("
        # build regex
        regex = "REGEX(<input>,"
        if hasattr(BaseTokens, self.tok):
            regex += f"\"{BaseTokens.no_verbose(getattr(BaseTokens,self.tok).value.pattern)}\""
        else:
            regex += f"\"{self.tok}\""

        regex += ",,"
        if isinstance(self.idx, int):
            regex += f"{self.idx})"
        else:
            regex += f"{self.idx[0]})"
        # build the rest of the search
        formula += regex
        formula += ",<input>,1)"

        # get the end index
        if self.direction == Direction.End:
            formula += f"+LEN({regex})"

        return formula


class ConstPosExpr(Expr):
    """ Constant Position Expression """
    def __init__(self,
        idx
    ):
        self.idx = idx

    def __repr__(self) -> str:
        return f"ConstPos({self.idx})"

    def __key(self) -> int:
        return self.idx

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, ConstPosExpr):
            return self.idx == other.idx
        return False

    def __len__(self):
        return 1

    def to_formula(self) -> str:
        return str(self.idx)

class Direction(Enum):
    Start = "Start"
    End = "End"

def gen_sub_str_expr(vk, l, r, sid, idg: 'InputDataGraph'):
    """ Generate all substring expressions for the given string

    vk: string to generate SubStrExpr's for
    l: left position
    r: right position
    sid: unique string index
    """
    def _to_exprs(node: tuple) -> set[PosExpr]:
        """ Convert a node in the idg to expressions in the language """
        start_edges = []
        end_edges = []

        # node is is left/start
        if node in idg.edge_labels:
            for r_edge in idg.edge_labels[node]:
                for label in idg.edge_labels[node][r_edge]:
                    pos = PosExpr(
                                tok=label[0],
                                idx=label[1],
                                direction=Direction.Start
                            )
                    start_edges.append(pos)

        # node is right/end
        for l_edge in idg.edge_labels:
            if node in idg.edge_labels[l_edge]:
                for label in idg.edge_labels[l_edge][node]:
                    pos = PosExpr(
                                tok=label[0],
                                idx=label[1],
                                direction=Direction.End
                            )
                    end_edges.append(pos)
        return set(start_edges + end_edges)

    vl = set([])
    vr = set([])
    for v in idg.nodes:
        if (sid, l) in idg.node_labels[v]:
            vl |= _to_exprs(v)
        if (sid, r) in idg.node_labels[v]:
            vr |= _to_exprs(v)

    vl.add(ConstPosExpr(idx=l))
    vr.add(ConstPosExpr(idx=r))

    return SubStringExpr(
                substr=vk,
                left=vl,
                right=vr
            )
