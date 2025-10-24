# src/core/nqueens.py
from .csp import CSP

def nqueens_csp(N):
    variables = list(range(N))
    domains = {v: list(range(N)) for v in variables}
    neighbors = {i: [j for j in variables if j != i] for i in variables}

    def constraint(X, x, Y, y):
        if X == Y:
            return True
        if x == y:
            return False
        if abs(x - y) == abs(X - Y):
            return False
        return True

    return CSP(variables, domains, neighbors, constraint)