import unittest

from expression import *
from statement import *
from machine import Machine
from parse import parse


def do_interpret(stmt: StmtMixin) -> Dict:
    machine = Machine(stmt, {})
    machine.run(debug=False)
    env = machine.env
    for k, v in env.items():
        env[k] = v.value
    return env


class TestParse(unittest.TestCase):

    def test_do_nothing(self):
        stmt = parse(" ")
        self.assertTrue(isinstance(stmt, DoNothing))

    def test_assign(self):
        code = """
            x = 5
            x = x + 1
            x = x - 2 - 3
            x = x + 3 + 2
        """
        stmt = parse(code)
        answer = {"x": 6}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))

        code = """
            x = 1 + 2 + 1 - 2
            y = x * 2
        """
        stmt = parse(code)
        answer = {"x": 2, "y": 4}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))

        code = """
            x = 1 - (0 - 1)
            y = x * 1
        """
        stmt = parse(code)
        answer = {"x": 2, "y": 2}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))

        code = """
            x = 5
            x = 1 + x * 2
        """
        stmt = parse(code)
        answer = {"x": 11}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))

        code = """
            x = 5
            x = (1 + x) * 2
        """
        stmt = parse(code)
        answer = {"x": 12}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))

    def test_if(self):
        code = """
            a = 1
            b = 1
            if (a < 0 + 2 && b < 2) {
                a = a + 1
            } else {
                b = b + 1
            }
            if (a < 2 || b < 1) {
                b = b + 1
            }
        """
        stmt = parse(code)
        answer = {"a": 2, "b": 1}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))

        code = """
            a = 1
            b = 1
            c = 0
            d = 0
            if (a < 2 && b < 2) {
                a = a + 1
                c = a
            } else {
                d = b
            }
            if (a + 1 < 1 * 3) {
                b = b + 1
            } else {
                d = d + 1
            }
            if (b == 1 || a < 2) {
                b = b + 1
            }
        """
        stmt = parse(code)
        answer = {"a": 2, "b": 2, "c": 2, "d": 1}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))

    def test_while(self):
        code = """
            x = 1
            while (x < 50) {
                x = x + 3
            }
        """
        stmt = parse(code)
        answer = {"x": 52}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))

        code = """
            a = 0
            b = 0
            while (a < 5) {
                a = a + 1
                b = b + a + 1 + 1
                b = b - 1
            }    
        """
        stmt = parse(code)
        answer = {"a": 5, "b": 20}
        env = do_interpret(stmt)
        self.assertEqual(answer, env)
        self.assertEqual(answer, eval(stmt.to_python)({}))


if __name__ == '__main__':
    unittest.main()
