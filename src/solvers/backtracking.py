from src.core.nqueens import nqueens_csp
from .search import backtracking_search

def solve_bt(N, timeout=None):
    csp = nqueens_csp(N)
    return backtracking_search(csp, inference="none", timeout=timeout,
                               use_mrv=True, use_degree=True, use_lcv=True)