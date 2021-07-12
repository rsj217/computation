"""
this file inspired by
https://github.com/kigawas/computation-py/blob/master/computation/interpreter/parser.py
"""

from typing import List

from lark import Lark, Token
from lark import Transformer as _Transformer

from expression import *
from statement import *


class Unreachable(Exception):
    pass


# note: lark is not exhaustive, so `expr: term ('+' term)*` won't work
GRAMMAR = r"""
%import common.ESCAPED_STRING   -> STRING
%import common.INT              -> NUMBER
%import common.CNAME            -> NAME
%import common.WS
%ignore WS

OP_AND: "&&"
OP_OR: "||"
OP_EQ: "<" | "=="
OP_ADD: "+" | "-"
OP_MUL: "*"
atom: NUMBER | NAME | "(" expr ")"

expr: expr OP_ADD mul_expr | mul_expr
mul_expr: mul_expr OP_MUL atom | atom

or_expr: or_expr OP_OR and_expr | and_expr
and_expr: and_expr OP_AND eq_expr | eq_expr
eq_expr: expr OP_EQ expr

if_stmt: "if" "(" or_expr ")" "{" stmts "}" [("else" "{" stmts "}")]
while_stmt: "while" "(" or_expr ")" "{" stmts "}"
assign_stmt: NAME "=" expr

stmt: expr | if_stmt | while_stmt | assign_stmt
stmts: stmt*
"""

parser = Lark(GRAMMAR, start="stmts", parser="lalr")


def token_to_atom(token: Token) -> ExprMixin:
    if token.type == "NUMBER":
        return Number(int(token.value))
    elif token.type == "NAME":
        return Variable(token.value)
    else:
        raise Unreachable


def eval_binary_expr(
        left,
        op,
        right,
        expected_ops,
        expr_classes,
) -> List[ExprMixin]:
    for expected_op, expr_class in zip(expected_ops, expr_classes):
        if op.value == expected_op:
            return [expr_class(left[0], right[0])]
    raise Unreachable


class Transformer(_Transformer):
    def atom(self, items) -> List[ExprMixin]:
        res = []
        for item in items:
            if isinstance(item, Token):
                res.append(token_to_atom(item))
            else:
                res.append(item[0])
        return res

    def _biexpr(self, items, expected_ops, expr_classes) -> List[ExprMixin]:
        if len(items) == 1:
            return items[0]
        left, op, right = items[0], items[1], items[2]
        return eval_binary_expr(left, op, right, expected_ops, expr_classes)

    def and_expr(self, items) -> List[ExprMixin]:
        return self._biexpr(items, ["&&"], [And])

    def or_expr(self, items) -> List[ExprMixin]:
        return self._biexpr(items, ["||"], [Or])

    def eq_expr(self, items) -> List[ExprMixin]:
        return self._biexpr(items, ["<", "=="], [LessThan, Equal])

    def expr(self, items) -> List[ExprMixin]:
        return self._biexpr(items, ["+", "-"], [Add, Sub])

    def mul_expr(self, items) -> List[ExprMixin]:
        return self._biexpr(items, ["*"], [Mul])

    def if_stmt(self, items) -> StmtMixin:
        cond, conseq = items[0][0], items[1]
        if len(items) == 2:
            return If(cond, conseq, DoNothing())
        elif len(items) == 3:
            return If(cond, conseq, items[2])
        else:
            raise Unreachable

    def while_stmt(self, items) -> (StmtMixin, StmtMixin):
        return While(items[0][0], self.stmt(items[1:]))

    def assign_stmt(self, items) -> StmtMixin:
        return Assign(items[0].value, items[1][0])

    def stmt(self, items) -> StmtMixin:
        if len(items) == 1:
            return items[0]
        else:
            raise Unreachable

    def stmts(self, items) -> StmtMixin:
        if len(items) == 0:
            return DoNothing()
        elif len(items) == 1:
            return items[0]

        return Sequence(items[0], self.stmts(items[1:]))


def parse(program: str):
    tree = parser.parse(program)
    return Transformer().transform(tree)


if __name__ == '__main__':
    source = """
        sum = 0
        i = 1
        n = 101
        while (i < n){
            sum = sum + i
            i = i + 1
        }
    """
    seq = parse(source)
    print(seq)
    ans = eval(seq.to_python)({})
    print(ans)
