# src/algorithms.py
from src.solvers.backtracking import solve_bt
from src.solvers.forward_checking import solve_fc
from src.solvers.mac import solve_mac

def solve_nqueens(N, algo="BT", timeout=None, seed=None):
    if algo == "BT":
        return solve_bt(N, timeout=timeout)
    if algo == "FC":
        return solve_fc(N, timeout=timeout)
    if algo == "MAC":
        return solve_mac(N, timeout=timeout)
    raise ValueError(f"Unknown algo: {algo}")