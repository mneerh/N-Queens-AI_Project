from .csp import nqueens_csp, backtracking_search

def solve_nqueens(N, algo="BT", timeout=None, seed=None):
    csp = nqueens_csp(N)
    mode = {"BT":"none", "FC":"fc", "MAC":"mac"}[algo]
    res = backtracking_search(
        csp, inference=mode, timeout=timeout, seed=seed,
        use_mrv=True, use_degree=True, use_lcv=True
    )
    return res