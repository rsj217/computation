from expression import *
from statement import *
from machine import Machine
from parse import parse


def get_env():
    return {
        "sum": Number(0),
        "i": Number(1),
        "n": Number(101),
    }


def ast_semantic() -> (StmtMixin, Dict):
    env = get_env()
    stmt = While(
        cond=LessThan(
            left=Variable("i"),
            right=Variable("n"),
        ),
        body=Sequence(
            first=Assign("sum", Add(Variable("sum"), Variable("i"))),
            second=Assign("i", Add(Variable("i"), Number(1))),
        )
    )
    print(stmt)
    return stmt, env


def parse_semantic() -> StmtMixin:
    source = """
        sum = 0
        i = 1
        n = 101
        while (i < n){
            sum = sum + i
            i = i + 1
        }
    """
    return parse(source)


def gauss_small_step():
    stmt, env = ast_semantic()
    machine = Machine(stmt, env)
    machine.run(debug=False)
    assert str(machine.env["i"]) == "101"
    assert str(machine.env["sum"]) == "5050"

    env = get_env()
    stmt = parse_semantic()
    machine = Machine(stmt, env)
    machine.run(debug=False)
    assert str(machine.env["i"]) == "101"
    assert str(machine.env["sum"]) == "5050"


def gauss_big_step():
    stmt, env = ast_semantic()
    env = stmt.evaluate(env)
    assert str(env["i"]) == "101"
    assert str(env["sum"]) == "5050"

    env = get_env()
    stmt = parse_semantic()
    env = stmt.evaluate(env)
    assert str(env["i"]) == "101"
    assert str(env["sum"]) == "5050"


def gauss_denatation():
    stmt, _ = ast_semantic()
    code = stmt.to_python
    proc = eval(code)
    env = proc({
        "sum": 0,
        "i": 1,
        "n": 101,
    })
    assert str(env["i"]) == "101"
    assert str(env["sum"]) == "5050"

    stmt = parse_semantic()
    code = stmt.to_python
    proc = eval(code)
    env = proc({
        "sum": 0,
        "i": 1,
        "n": 101,
    })
    assert str(env["i"]) == "101"
    assert str(env["sum"]) == "5050"


if __name__ == '__main__':
    gauss_small_step()
    gauss_big_step()
    gauss_denatation()
