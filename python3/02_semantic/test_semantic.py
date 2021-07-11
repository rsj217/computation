import unittest

from expression import *
from statement import *
from machine import Machine


class TestNumber(unittest.TestCase):

    def setUp(self) -> None:
        self.expr = Number(val=1)
        self.desc = "1"
        self.env = {}

    def test_small_step(self):
        self.assertTrue(isinstance(self.expr, ExprMixin))
        self.assertFalse(self.expr.reducible)
        self.assertEqual(self.desc, str(self.expr))

    def test_big_step(self):
        ans = self.expr.evaluate(self.env)
        self.assertEqual(ans, self.expr)

    def test_denatation(self):
        code = self.expr.to_python
        proc = eval(code)
        ans = proc({})
        self.assertEqual(1, ans)


class TestBoolean(unittest.TestCase):

    def setUp(self) -> None:
        self.expr = Boolean(val=True)
        self.desc = "True"
        self.env = {}

    def test_small_step(self):
        self.assertTrue(isinstance(self.expr, ExprMixin))
        self.assertFalse(self.expr.reducible)
        self.assertEqual(self.desc, str(self.expr))

    def test_big_step(self):
        ans = self.expr.evaluate(self.env)
        self.assertEqual(self.expr, ans)

    def test_denatation(self):
        code = self.expr.to_python
        proc = eval(code)
        ans = proc({})
        self.assertEqual(True, ans)


class TestAdd(unittest.TestCase):

    def setUp(self) -> None:
        self.expr = Add(Number(1), Number(2))
        self.desc = "1 + 2"
        self.env = {}

    def test_small_step(self):
        self.assertTrue(isinstance(self.expr, ExprMixin))

        self.assertTrue(self.expr.reducible)
        self.assertEqual(self.desc, str(self.expr))

        expr = self.expr.reduce(self.env)

        self.assertFalse(expr.reducible)
        self.assertEqual("3", str(expr))

    def test_big_step(self):
        ans = self.expr.evaluate(self.env)
        self.assertEqual("3", str(ans))

    def test_denatation(self):
        code = self.expr.to_python
        proc = eval(code)
        ans = proc({})
        self.assertEqual(3, ans)


class TestMul(unittest.TestCase):

    def setUp(self) -> None:
        self.expr = Add(
            left=Mul(Number(1), Number(2)),
            right=Mul(Number(3), Number(4))
        )
        self.desc = "1 * 2 + 3 * 4"
        self.env = {}

    def test_small_step(self):
        self.assertTrue(isinstance(self.expr, ExprMixin))
        self.assertEqual(self.desc, str(self.expr))

        self.assertTrue(self.expr.reducible)
        expr = self.expr.reduce(self.env)
        self.assertEqual("2 + 3 * 4", str(expr))

        self.assertTrue(expr.reducible)
        expr = expr.reduce(self.env)
        self.assertEqual("2 + 12", str(expr))

        self.assertTrue(expr.reducible)
        expr = expr.reduce(self.env)
        self.assertEqual("14", str(expr))

        self.assertFalse(expr.reducible)
        self.assertEqual("14", str(expr))

    def test_big_step(self):
        ans = self.expr.evaluate(self.env)
        self.assertEqual("14", str(ans))

    def test_denatation(self):
        code = self.expr.to_python
        proc = eval(code)
        ans = proc({})
        self.assertEqual(14, ans)


class TestLessThan(unittest.TestCase):

    def setUp(self) -> None:
        self.expr = LessThan(Number(1), Number(2))
        self.desc = "1 < 2"
        self.env = {}

    def test_small_step(self):
        self.assertTrue(isinstance(self.expr, ExprMixin))
        self.assertEqual(self.desc, str(self.expr))

        self.assertTrue(self.expr.reducible)
        expr = self.expr.reduce(self.env)
        self.assertEqual("True", str(expr))

        self.assertFalse(expr.reducible)

    def test_big_step(self):
        ans = self.expr.evaluate(self.env)
        self.assertEqual("True", str(ans))

    def test_denatation(self):
        code = self.expr.to_python
        proc = eval(code)
        ans = proc({})
        self.assertEqual(True, ans)


class TestVariable(unittest.TestCase):

    def setUp(self) -> None:
        self.expr = Variable("x")
        self.desc = "x"
        self.env = {"x": Number(1)}

    def test_small_step(self):
        self.assertTrue(isinstance(self.expr, ExprMixin))
        self.assertEqual(self.desc, str(self.expr))

        self.assertTrue(self.expr.reducible)
        expr = self.expr.reduce(self.env)
        self.assertEqual("1", str(expr))

        self.assertFalse(expr.reducible)

    def test_big_step(self):
        ans = self.expr.evaluate(self.env)
        self.assertEqual("1", str(ans))

    def test_denatation(self):
        code = self.expr.to_python
        proc = eval(code)
        ans = proc({"x": 1})
        self.assertEqual(1, ans)


class TestNothing(unittest.TestCase):

    def test_small_step(self):
        n = DoNothing()
        self.assertFalse(n.reducible)


class TestAssign(unittest.TestCase):

    def setUp(self) -> None:
        self.stmt = Assign("x", Add(Variable("x"), Number(1)))
        self.desc = "x = x + 1"
        self.env = {"x": Number(2)}

    def test_small_step(self):
        self.assertTrue(isinstance(self.stmt, StmtMixin))
        self.assertEqual(self.desc, str(self.stmt))

        self.assertTrue(self.stmt.reducible)
        stmt, env = self.stmt.reduce(self.env)
        self.assertEqual("x = 2 + 1", str(stmt))

        self.assertTrue(stmt.reducible)
        stmt, env = stmt.reduce(env)
        self.assertEqual("x = 3", str(stmt))

        self.assertTrue(stmt.reducible)
        expr, env = stmt.reduce(env)
        self.assertEqual(DoNothing(), expr)

        self.assertFalse(expr.reducible)
        self.assertEqual("3", str(env["x"]))

    def test_big_step(self):
        env = self.stmt.evaluate(self.env)
        self.assertEqual("3", str(env["x"]))

    def test_denatation(self):
        code = self.stmt.to_python
        proc = eval(code)
        env = proc({"x": 2})
        self.assertEqual(3, env["x"])


class TestAssignMachine(unittest.TestCase):

    def setUp(self) -> None:
        self.stmt = Assign("x", Add(Variable("x"), Number(1)))
        self.desc = "x = x + 1"
        self.env = {"x": Number(2)}

    def test_small_step(self):
        self.assertTrue(isinstance(self.stmt, StmtMixin))
        self.assertEqual(self.desc, str(self.stmt))

        m = Machine(self.stmt, self.env)
        m.run()

        self.assertFalse(m.stmt.reducible)
        self.assertEqual("3", str(m.env["x"]))


class TestIf(unittest.TestCase):

    def setUp(self) -> None:
        self.stmt = If(
            cond=Variable("x"),
            consequence=Assign("y", Number(1)),
            alternative=Assign("y", Number(2)),
        )
        self.desc = "if (x) {y = 1} else {y = 2}"

    def test_small_step(self):
        env = {"x": Boolean(True)}
        self.assertTrue(isinstance(self.stmt, StmtMixin))
        self.assertEqual(self.desc, str(self.stmt))
        m = Machine(self.stmt, env)
        m.run()
        self.assertEqual("True", str(m.env["x"]))
        self.assertEqual("1", str(m.env["y"]))

        env = {"x": Boolean(False)}
        m = Machine(self.stmt, env)
        m.run()
        self.assertEqual("False", str(m.env["x"]))
        self.assertEqual("2", str(m.env["y"]))

    def test_big_step(self):
        env = {"x": Boolean(True)}
        env = self.stmt.evaluate(env)
        self.assertEqual("True", str(env["x"]))
        self.assertEqual("1", str(env["y"]))

    def test_denatation(self):
        code = self.stmt.to_python
        print(code)
        proc = eval(code)
        env = proc({"x": True})
        self.assertEqual(1, env["y"])


class TestSequence(unittest.TestCase):

    def setUp(self) -> None:
        self.stmt = Sequence(
            first=Assign("x", Add(Number(1), Number(1))),
            second=Assign("y", Add(Variable("x"), Number(1))),
        )
        self.desc = "x = 1 + 1;y = x + 1"

    def test_small_step(self):
        env = {}
        self.assertTrue(isinstance(self.stmt, StmtMixin))
        self.assertEqual(self.desc, str(self.stmt))
        m = Machine(self.stmt, env)
        m.run()
        self.assertEqual("2", str(m.env["x"]))
        self.assertEqual("3", str(m.env["y"]))

    def test_big_step(self):
        env = {}
        env = self.stmt.evaluate(env)
        self.assertEqual("2", str(env["x"]))
        self.assertEqual("3", str(env["y"]))

    def test_denatation(self):
        code = self.stmt.to_python
        proc = eval(code)
        env = proc({"x": True})
        self.assertEqual(2, env["x"])
        self.assertEqual(3, env["y"])


class TestWhile(unittest.TestCase):

    def setUp(self) -> None:
        self.stmt = While(
            cond=LessThan(Variable("x"), Number(5)),
            body=Assign("x", Mul(Variable("x"), Number(3))),
        )
        self.desc = "while (x < 5) {x = x * 3}"

    def test_small_step(self):
        env = {"x": Number(1)}
        self.assertTrue(isinstance(self.stmt, StmtMixin))
        self.assertEqual(self.desc, str(self.stmt))
        m = Machine(self.stmt, env)
        m.run()
        self.assertEqual("9", str(m.env["x"]))

    def test_big_step(self):
        env = {"x": Number(1)}
        env = self.stmt.evaluate(env)
        self.assertEqual("9", str(env["x"]))

    def test_denatation(self):
        code = self.stmt.to_python
        proc = eval(code)
        env = {"x": 1}
        env = proc(env)
        self.assertEqual(9, env["x"])


if __name__ == '__main__':
    unittest.main()
