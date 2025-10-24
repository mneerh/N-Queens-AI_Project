# src/core/csp.py
from collections import deque

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = {v: list(domains[v]) for v in variables}
        self.neighbors = neighbors
        self.constraints = constraints
        self.checks = 0
        self.assignments = 0

    def consistent_pair(self, X, x, Y, y):
        self.checks += 1
        return self.constraints(X, x, Y, y)

def ac3(csp, domains=None, queue=None):
    if domains is None:
        domains = {v: list(csp.domains[v]) for v in csp.variables}
    if queue is None:
        queue = deque((Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi])
    while queue:
        Xi, Xj = queue.popleft()
        if revise(csp, domains, Xi, Xj):
            if not domains[Xi]:
                return domains, False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return domains, True

def revise(csp, domains, Xi, Xj):
    revised = False
    to_remove = []
    for x in list(domains[Xi]):
        if not any(csp.consistent_pair(Xi, x, Xj, y) for y in domains[Xj]):
            to_remove.append(x)
    for x in to_remove:
        domains[Xi].remove(x)
        revised = True
    return revised