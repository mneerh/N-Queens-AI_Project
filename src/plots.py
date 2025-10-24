# src/plots.py
import csv, os
import matplotlib.pyplot as plt

def read_csv(path):
    rows = []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            row["N"] = int(row["N"])
            row["time_sec"] = float(row["time_sec"])
            row["checks"] = int(row["checks"])
            rows.append(row)
    return rows

def plot_metric(rows, field, ylabel, title, out_png):
    # Compute the median across seeds for each (algo, N)
    agg = {}
    for row in rows:
        key = (row["algo"], row["N"])
        agg.setdefault(key, []).append(row[field])

    xs = sorted({N for (_, N) in agg.keys()})
    algos = sorted({a for (a, _) in agg.keys()})

    plt.figure()
    for algo in algos:
        ys = []
        for N in xs:
            vals = agg.get((algo, N), [])
            if not vals: 
                continue
            vals.sort()
            median = vals[len(vals)//2]
            ys.append(median)
        plt.plot(xs[:len(ys)], ys, marker="o", label=algo)

    plt.xlabel("N")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.savefig(out_png, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    os.makedirs("plots", exist_ok=True)
    rows = read_csv("results/metrics.csv")
    plot_metric(rows, "time_sec", "Time (sec)", "Median solving time vs N", "plots/time_vs_N.png")
    plot_metric(rows, "checks", "Constraint checks (median)", "Median constraint checks vs N", "plots/checks_vs_N.png")
    print("Saved plots to plots/")