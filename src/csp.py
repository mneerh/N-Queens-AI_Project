from collections import deque
import random, time

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

def select_unassigned_variable(csp, assignment, domains, use_mrv=True, use_degree=True):
    unassigned = [v for v in csp.variables if v not in assignment]
    if use_mrv:
        mrv = min(len(domains[v]) for v in unassigned)
        unassigned = [v for v in unassigned if len(domains[v]) == mrv]
    if use_degree and len(unassigned) > 1:
        degrees = {v: sum(1 for n in csp.neighbors[v] if n not in assignment) for v in unassigned}
        maxdeg = max(degrees.values())
        unassigned = [v for v in unassigned if degrees[v] == maxdeg]
    return random.choice(unassigned)

def order_domain_values(csp, var, assignment, domains, use_lcv=True):
    vals = list(domains[var])
    if not use_lcv:
        return vals
    def conflicts(val):
        count = 0
        for n in csp.neighbors[var]:
            if n not in assignment:
                for y in domains[n]:
                    if not csp.consistent_pair(var, val, n, y):
                        count += 1
        return count
    return sorted(vals, key=conflicts)

def backtracking_search(csp, inference="none", timeout=None, seed=None,
                        use_mrv=True, use_degree=True, use_lcv=True):
    if seed is not None:
        random.seed(seed)
    start_domains = {v: list(csp.domains[v]) for v in csp.variables}
    assignment = {}
    t0 = time.perf_counter()

    def elapsed():
        return time.perf_counter() - t0

    def bt(domains):
        if timeout and elapsed() > timeout:
            return None, "timeout"
        if len(assignment) == len(csp.variables):
            return dict(assignment), "success"

        var = select_unassigned_variable(csp, assignment, domains, use_mrv, use_degree)

        for val in order_domain_values(csp, var, assignment, domains, use_lcv):
            ok = True
            for n in csp.neighbors[var]:
                if n in assignment and not csp.consistent_pair(var, val, n, assignment[n]):
                    ok = False
                    break
            if not ok:
                continue

            assignment[var] = val
            csp.assignments += 1
            new_domains = {v: list(domains[v]) for v in domains}

            consistent = True
            if inference == "fc":
                for n in csp.neighbors[var]:
                    if n not in assignment:
                        new_domains[n] = [y for y in new_domains[n] if csp.consistent_pair(var, val, n, y)]
                        if not new_domains[n]:
                            consistent = False
                            break
            elif inference == "mac":
                _, consistent = ac3(csp, new_domains, deque((n, var) for n in csp.neighbors[var]))

            if consistent:
                result, status = bt(new_domains)
                if status == "timeout":
                    return None, "timeout"
                if result is not None:
                    return result, status

            assignment.pop(var, None)

        return None, "failure"

    result, status = bt(start_domains)
    return {
        "solution": result,
        "status": status,
        "checks": csp.checks,
        "assignments": csp.assignments,
        "time_sec": elapsed()
    }

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