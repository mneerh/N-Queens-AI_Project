# src/solvers/search.py
import time
from collections import deque
from src.core.csp import ac3

def select_unassigned_variable(csp, assignment, domains, use_mrv=True, use_degree=True):
    unassigned = [v for v in csp.variables if v not in assignment]
    if use_mrv:
        mrv = min(len(domains[v]) for v in unassigned)
        unassigned = [v for v in unassigned if len(domains[v]) == mrv]
    if use_degree and len(unassigned) > 1:
        degrees = {v: sum(1 for n in csp.neighbors[v] if n not in assignment) for v in unassigned}
        maxdeg = max(degrees.values())
        unassigned = [v for v in unassigned if degrees[v] == maxdeg]
    return min(unassigned) 

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

def backtracking_search(csp, inference="none", timeout=None,
                        use_mrv=True, use_degree=True, use_lcv=True):
    start_domains = {v: list(csp.domains[v]) for v in csp.variables}
    assignment = {}
    t0 = time.perf_counter()
    def elapsed(): return time.perf_counter() - t0

    def bt(domains):
        if timeout and elapsed() > timeout:
            return None, "timeout"
        if len(assignment) == len(csp.variables):
            return dict(assignment), "success"

        var = select_unassigned_variable(csp, assignment, domains, use_mrv, use_degree)
        for val in order_domain_values(csp, var, assignment, domains, use_lcv):
            if timeout and elapsed() > timeout:
                return None, "timeout"
            #local check
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