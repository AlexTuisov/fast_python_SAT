import numpy as np

from formula import CNF


class FastCNF:
    def __init__(self, slow_cnf: CNF):
        self.length = len(slow_cnf.clauses)
        self.width = max(map(len, slow_cnf.clauses))
        self.clauses = np.zeros((self.length, self.width), dtype=np.int32)


class Solver:
    def __init__(self):
        pass
