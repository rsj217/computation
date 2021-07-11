from __future__ import annotations
from typing import Dict

from expression import VarExprMixin, ExprMixin, Boolean


class StmtMixin:

    @property
    def reducible(self) -> bool:
        return True

    def reduce(self, env: Dict) -> (StmtMixin, Dict):
        raise NotImplementedError

    def evaluate(self, env: Dict) -> Dict:
        raise NotImplementedError

    @property
    def to_python(self) -> str:
        raise NotImplementedError


class DoNothing(VarExprMixin, StmtMixin):

    def __repr__(self):
        return "do-nothing"

    def __eq__(self, other):
        return isinstance(other, DoNothing)

    def evaluate(self, env: Dict) -> Dict:
        return env

    @property
    def to_python(self) -> str:
        return f"lambda e: e"


class Assign(StmtMixin):

    def __init__(self, name: str, expr: ExprMixin):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return f"{self.name} = {self.expr}"

    def reduce(self, env: Dict) -> (StmtMixin, Dict):
        if self.expr.reducible:
            return Assign(self.name, self.expr.reduce(env)), env
        env[self.name] = self.expr
        return DoNothing(), env

    def evaluate(self, env: Dict) -> Dict:
        return env | {self.name: self.expr.evaluate(env)}

    @property
    def to_python(self) -> str:
        return f'lambda e: e | {{"{self.name}": ({self.expr.to_python})(e)}}'


class If(StmtMixin):

    def __init__(self, cond: ExprMixin, consequence: StmtMixin, alternative: StmtMixin):
        self.cond = cond
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return f"if ({self.cond}) {{{self.consequence}}} else {{{self.alternative}}}"

    def reduce(self, env: Dict) -> (StmtMixin, Dict):
        if self.cond.reducible:
            return If(self.cond.reduce(env), self.consequence, self.alternative), env
        else:
            if self.cond == Boolean(True):
                return self.consequence, env
            else:  # self.cond == Boolean(False)
                return self.alternative, env

    def evaluate(self, env: Dict) -> Dict:
        cond = self.cond.evaluate(env)
        if cond == Boolean(True):
            return self.consequence.evaluate(env)
        else:  # cond == Boolean(False)
            return self.alternative.evaluate(env)

    @property
    def to_python(self) -> str:
        return f"lambda e: ({self.consequence.to_python})(e) if ({self.cond.to_python})(e) else ({self.alternative.to_python})(e)"


class Sequence(StmtMixin):
    def __init__(self, first: StmtMixin, second: StmtMixin):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"{self.first};{self.second}"

    def reduce(self, env: Dict) -> (StmtMixin, Dict):
        if self.first.reducible:
            reduced_first, reduced_env = self.first.reduce(env)
            return Sequence(reduced_first, self.second), reduced_env
        else:
            return self.second.reduce(env)

    def evaluate(self, env: Dict) -> Dict:
        return self.second.evaluate(self.first.evaluate(env))

    @property
    def to_python(self):
        return f"lambda e: ({self.second.to_python})(({self.first.to_python})(e))"


class While(StmtMixin):

    def __init__(self, cond: ExprMixin, body: StmtMixin):
        self.cond = cond
        self.body = body

    def __repr__(self):
        return f"while ({self.cond}) {{{self.body}}}"

    def reduce(self, env: Dict) -> (StmtMixin, Dict):
        return If(self.cond, Sequence(self.body, self), DoNothing()), env

    def evaluate(self, env: Dict) -> Dict:
        cond = self.cond.evaluate(env)
        if cond == Boolean(True):
            return self.evaluate(self.body.evaluate(env))
        else:  # cond == Boolean(False)
            return env

    @property
    def to_python(self) -> str:
        return f"(lambda f: (lambda x: x(x))(lambda x: f(lambda *args: x(x)(*args))))(lambda wh: lambda e: e if ({self.cond.to_python})(e) is False else wh(({self.body.to_python})(e)))"
