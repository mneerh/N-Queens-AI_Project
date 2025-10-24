
import argparse
from .algorithms import solve_nqueens

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=8)
    p.add_argument("--algo", choices=["BT", "FC", "MAC"], default="MAC")
    p.add_argument("--timeout", type=int, default=60)
    args = p.parse_args()

    res = solve_nqueens(args.N, algo=args.algo, timeout=args.timeout, seed=0)
    print(f"Status: {res['status']}")
    print(f"Time: {res['time_sec']:.4f}s, Checks: {res['checks']}, Assignments: {res['assignments']}")
    if res["solution"]:
        print("Solution (col -> row):", res["solution"])