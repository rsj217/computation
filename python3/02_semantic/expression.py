from __future__ import annotations
from typing import Dict, Any


class BaseMixin:

    @property
    def value(self) -> Any:
        if hasattr(self, "val"):
            return self.val
        raise AttributeError

    @property
    def reducible(self) -> bool:
        return False


class VarExprMixin(BaseMixin):

    @property
    def reducible(self) -> bool:
        return False


class ExprMixin(BaseMixin):

    @property
    def reducible(self) -> bool:
        return True

    def reduce(self, env: Dict) -> ExprMixin:
        raise NotImplementedError

    def evaluate(self, env: Dict) -> ExprMixin:
        raise NotImplementedError

    @property
    def to_python(self) -> str:
        raise NotImplementedError


class Number(VarExprMixin, ExprMixin):
    def __init__(self, val: int):
        self.val = val

    def __repr__(self):
        return f"{self.val}"

    def __str__(self):
        return f"{self.val}"

    def evaluate(self, env: Dict) -> ExprMixin:
        return self

    @property
    def to_python(self) -> str:
        return f"lambda e: {self.val}"


class Boolean(VarExprMixin, ExprMixin):
    def __init__(self, val: bool):
        self.val = val

    def __repr__(self):
        return f"{self.val}"

    def __eq__(self, other):
        return self.val == other.val

    def evaluate(self, env: Dict) -> ExprMixin:
        return self

    @property
    def to_python(self) -> str:
        return f"lambda e: {self.val}"


class Add(ExprMixin):

    def __init__(self, left: ExprMixin, right: ExprMixin):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} + {self.right}"

    def reduce(self, env: Dict) -> ExprMixin:
        if self.left.reducible:
            return Add(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return Add(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value + self.right.value)

    def evaluate(self, env: Dict) -> ExprMixin:
        return Number(self.left.evaluate(env).value + self.right.evaluate(env).value)

    @property
    def to_python(self) -> str:
        return f"lambda e: ({self.left.to_python})(e) + ({self.right.to_python})(e)"


class Sub(ExprMixin):

    def __init__(self, left: ExprMixin, right: ExprMixin):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} - {self.right}"

    def reduce(self, env: Dict) -> ExprMixin:
        if self.left.reducible:
            return Sub(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return Sub(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value - self.right.value)

    def evaluate(self, env: Dict) -> ExprMixin:
        return Number(self.left.evaluate(env).value - self.right.evaluate(env).value)

    @property
    def to_python(self) -> str:
        return f"lambda e: ({self.left.to_python})(e) - ({self.right.to_python})(e)"


class Mul(ExprMixin):

    def __init__(self, left: ExprMixin, right: ExprMixin):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} * {self.right}"

    def reduce(self, env: Dict) -> ExprMixin:
        if self.left.reducible:
            return Mul(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return Mul(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value * self.right.value)

    def evaluate(self, env: Dict) -> ExprMixin:
        return Number(self.left.evaluate(env).value * self.right.evaluate(env).value)

    @property
    def to_python(self) -> str:
        return f"lambda e: ({self.left.to_python})(e) * ({self.right.to_python})(e)"


class LessThan(ExprMixin):

    def __init__(self, left: ExprMixin, right: ExprMixin):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} < {self.right}"

    def reduce(self, env: Dict) -> ExprMixin:
        if self.left.reducible:
            return LessThan(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return LessThan(self.left, self.right.reduce(env))
        else:
            return Boolean(self.left.value < self.right.value)

    def evaluate(self, env: Dict) -> ExprMixin:
        return Boolean(self.left.evaluate(env).value < self.right.evaluate(env).value)

    @property
    def to_python(self) -> str:
        return f"lambda e: ({self.left.to_python})(e) < ({self.right.to_python})(e)"


class Variable(ExprMixin):

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    def reduce(self, env: Dict) -> ExprMixin:
        return env[self.name]

    def evaluate(self, env: Dict) -> ExprMixin:
        return env[self.name]

    @property
    def to_python(self) -> str:
        return f"lambda e: e['{self.name}']"


class Equal(ExprMixin):

    def __init__(self, left: ExprMixin, right: ExprMixin):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} == {self.right}"

    def reduce(self, env: Dict) -> ExprMixin:
        if self.left.reducible:
            return Equal(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return Equal(self.left, self.right.reduce(env))
        else:
            return Boolean(self.left.value == self.right.value)

    def evaluate(self, env: Dict) -> ExprMixin:
        return Boolean(self.left.evaluate(env).value == self.right.evaluate(env).value)

    @property
    def to_python(self) -> str:
        return f"lambda e: ({self.left.to_python})(e) == ({self.right.to_python})(e)"


class And(ExprMixin):

    def __init__(self, left: ExprMixin, right: ExprMixin):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} && {self.right}"

    def reduce(self, env: Dict) -> ExprMixin:
        if self.left.reducible:
            return And(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return And(self.left, self.right.reduce(env))
        else:
            return Boolean(self.left.value and self.right.value)

    def evaluate(self, env: Dict) -> ExprMixin:
        return Boolean(self.left.evaluate(env).value and self.right.evaluate(env).value)

    @property
    def to_python(self) -> str:
        return f"lambda e: ({self.left.to_python})(e) and ({self.right.to_python})(e)"


class Or(ExprMixin):

    def __init__(self, left: ExprMixin, right: ExprMixin):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} || {self.right}"

    def reduce(self, env: Dict) -> ExprMixin:
        if self.left.reducible:
            return Or(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return Or(self.left, self.right.reduce(env))
        else:
            return Boolean(self.left.value or self.right.value)

    def evaluate(self, env: Dict) -> ExprMixin:
        return Boolean(self.left.evaluate(env).value or self.right.evaluate(env).value)

    @property
    def to_python(self) -> str:
        return f"lambda e: ({self.left.to_python})(e) or ({self.right.to_python})(e)"
