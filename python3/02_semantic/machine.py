from typing import Dict
from statement import StmtMixin


class Machine:
    def __init__(self, stmt: StmtMixin, env: Dict):
        self.stmt = stmt
        self.env = env

    def step(self):
        self.stmt, self.env = self.stmt.reduce(self.env)

    def run(self, debug=True):
        while self.stmt.reducible:
            if debug:
                print(self.stmt, self.env)
            self.step()

        if debug:
            print(self.stmt, self.env)
