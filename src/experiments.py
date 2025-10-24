# src/experiments.py
import argparse, csv, os
from src.algorithms import solve_nqueens

def run_suite(out_csv, Ns, seeds, timeout):
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    fields = ["algo","N","seed","time_sec","checks","assignments","status"]
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for N in Ns:
            for seed in seeds:
                for algo in ["BT","FC","MAC"]:
                    res = solve_nqueens(N, algo=algo, timeout=timeout, seed=seed)
                    w.writerow({
                        "algo": algo, "N": N, "seed": seed,
                        "time_sec": f"{res['time_sec']:.6f}",
                        "checks": res["checks"],
                        "assignments": res["assignments"],
                        "status": res["status"]
                    })
                    print(f"N={N} algo={algo} seed={seed} -> {res['status']} {res['time_sec']:.3f}s checks={res['checks']}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true", help="Run Ns [4,8] with seed=0")
    p.add_argument("--full", action="store_true", help="Run Ns [8,16,32,64] with seeds [0,1,2]")
    p.add_argument("--timeout", type=int, default=1200, help="Per-run timeout seconds (default 20 min)")
    args = p.parse_args()

    if args.quick:
        Ns, seeds = [4,8], [0]
    elif args.full:
        Ns, seeds = [8,16,32,64], [0,1,2]
    else:
        Ns, seeds = [8], [0]

    run_suite("results/metrics.csv", Ns, seeds, timeout=args.timeout)