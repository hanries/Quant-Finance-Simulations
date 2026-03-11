import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from collections import Counter

def simulate_francisco_dice(num_simulations=100000):
    results = []
    results_by_first_roll = {k: [] for k in range(1, 7)}

    for _ in range(num_simulations):
        first_roll = random.randint(1, 6)
        n = 0
        while True:
            next_roll = random.randint(1, 6)
            n += 1
            if next_roll >= first_roll:
                break
        results.append(n)
        results_by_first_roll[first_roll].append(n)

    return results, results_by_first_roll


def print_summary(results, results_by_first_roll):
    estimated_E_N = sum(results) / len(results)
    exact_E_N = 49 / 20

    print("=" * 45)
    print("    Francisco's Dice Roll Simulation")
    print("=" * 45)
    print(f"  Simulations run   : {len(results):,}")
    print(f"  Estimated E[N]    : {estimated_E_N:.4f}")
    print(f"  Exact E[N]        : {exact_E_N:.4f}  (49/20)")
    print(f"  Difference        : {abs(estimated_E_N - exact_E_N):.4f}")
    print("=" * 45)
    print(f"\n  {'First Roll':<12} {'Exact E[N|k]':<16} {'Simulated E[N|k]'}")
    print("  " + "-" * 42)
    for k in range(1, 7):
        p = (7 - k) / 6
        exact = 1 / p
        simulated = sum(results_by_first_roll[k]) / len(results_by_first_roll[k])
        print(f"  k = {k:<8} {exact:<16.4f} {simulated:.4f}")


def plot_results(results, results_by_first_roll):
    # ── Color palette ──────────────────────────────────────────────
    BG        = "#0f0f14"
    PANEL     = "#16161e"
    ACCENT    = "#e8c468"
    ACCENT2   = "#7eb8f7"
    TEXT      = "#e8e8f0"
    SUBTEXT   = "#888899"
    GRID      = "#2a2a3a"
    BAR_COLORS = ["#7eb8f7","#85d4a8","#e8c468","#f79d7e","#c07ef7","#f77eb8"]

    plt.rcParams.update({
        "font.family": "monospace",
        "text.color": TEXT,
        "axes.labelcolor": TEXT,
        "xtick.color": SUBTEXT,
        "ytick.color": SUBTEXT,
    })

    fig = plt.figure(figsize=(16, 10), facecolor=BG)
    fig.suptitle(
        "Francisco's Dice Roll — Monte Carlo Simulation",
        fontsize=18, fontweight="bold", color=ACCENT,
        fontfamily="monospace", y=0.97
    )

    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38,
                           left=0.07, right=0.97, top=0.91, bottom=0.09)

    exact_E_N   = 49 / 20
    estimated   = sum(results) / len(results)

    # ── Helper to style axes ────────────────────────────────────────
    def style_ax(ax, title):
        ax.set_facecolor(PANEL)
        ax.set_title(title, color=ACCENT2, fontsize=10,
                     fontfamily="monospace", pad=8)
        ax.spines[:].set_color(GRID)
        ax.tick_params(colors=SUBTEXT, labelsize=8)
        ax.yaxis.label.set_color(SUBTEXT)
        ax.xaxis.label.set_color(SUBTEXT)
        ax.grid(axis="y", color=GRID, linewidth=0.6, linestyle="--", alpha=0.7)

    # ── 1. Distribution of N (overall) ─────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    style_ax(ax1, "Distribution of N (all first rolls)")
    counts = Counter(results)
    max_n  = min(max(counts), 20)
    xs     = list(range(1, max_n + 1))
    ys     = [counts.get(x, 0) / len(results) for x in xs]
    ax1.bar(xs, ys, color=ACCENT, alpha=0.85, width=0.7, zorder=3)
    ax1.axvline(estimated,  color=ACCENT2, linewidth=1.8,
                linestyle="--", label=f"Simulated: {estimated:.3f}")
    ax1.axvline(exact_E_N,  color="#f77eb8", linewidth=1.8,
                linestyle=":",  label=f"Exact: {exact_E_N:.3f}")
    ax1.set_xlabel("N (rolls after first)")
    ax1.set_ylabel("Probability")
    ax1.legend(fontsize=7, facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT)

    # ── 2. E[N|k] — exact vs simulated ─────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    style_ax(ax2, "E[N | first roll = k]")
    ks      = list(range(1, 7))
    exact   = [6 / (7 - k) for k in ks]
    sim_avg = [sum(results_by_first_roll[k]) / len(results_by_first_roll[k]) for k in ks]
    x       = np.arange(6)
    w       = 0.35
    ax2.bar(x - w/2, exact,   width=w, color=ACCENT,  alpha=0.85, label="Exact",     zorder=3)
    ax2.bar(x + w/2, sim_avg, width=w, color=ACCENT2, alpha=0.85, label="Simulated", zorder=3)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"k={k}" for k in ks], fontsize=8)
    ax2.set_ylabel("E[N | k]")
    ax2.legend(fontsize=7, facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT)

    # ── 3. Running estimate of E[N] ─────────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    style_ax(ax3, "Running Estimate of E[N]")
    checkpoints = np.logspace(1, np.log10(len(results)), 300).astype(int)
    running     = [np.mean(results[:n]) for n in checkpoints]
    ax3.plot(checkpoints, running, color=ACCENT, linewidth=1.4, zorder=3)
    ax3.axhline(exact_E_N, color="#f77eb8", linewidth=1.5,
                linestyle="--", label=f"Exact = {exact_E_N}")
    ax3.set_xscale("log")
    ax3.set_xlabel("Number of simulations (log scale)")
    ax3.set_ylabel("Estimated E[N]")
    ax3.legend(fontsize=7, facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT)

    # ── 4. Distribution of N per first roll ─────────────────────────
    ax4 = fig.add_subplot(gs[1, :2])
    style_ax(ax4, "Distribution of N  ·  split by first roll")
    offsets = np.arange(1, 16)
    bar_w   = 0.13
    for i, k in enumerate(range(1, 7)):
        c      = Counter(results_by_first_roll[k])
        total  = len(results_by_first_roll[k])
        probs  = [c.get(n, 0) / total for n in offsets]
        ax4.bar(offsets + (i - 2.5) * bar_w, probs,
                width=bar_w, color=BAR_COLORS[i],
                alpha=0.85, label=f"k={k}", zorder=3)
    ax4.set_xlabel("N")
    ax4.set_ylabel("Probability")
    ax4.set_xticks(offsets)
    ax4.legend(fontsize=7, ncol=6, facecolor=PANEL,
               edgecolor=GRID, labelcolor=TEXT)

    # ── 5. Success probability by first roll ────────────────────────
    ax5 = fig.add_subplot(gs[1, 2])
    style_ax(ax5, "P(success per roll) by first roll k")
    probs = [(7 - k) / 6 for k in range(1, 7)]
    bars  = ax5.bar(ks, probs, color=BAR_COLORS, alpha=0.9, zorder=3)
    for bar, p in zip(bars, probs):
        ax5.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.01,
                 f"{p:.2f}", ha="center", va="bottom",
                 color=TEXT, fontsize=8, fontfamily="monospace")
    ax5.set_xlabel("First roll k")
    ax5.set_ylabel("P(roll ≥ k)")
    ax5.set_xticks(ks)
    ax5.set_ylim(0, 1.15)

    plt.savefig("results.png", dpi=150, bbox_inches="tight", facecolor=BG)
    print("\n  Plot saved as results.png")
    plt.show()


if __name__ == "__main__":
    print("Running simulation...")
    results, results_by_first_roll = simulate_francisco_dice(100000)
    print_summary(results, results_by_first_roll)
    plot_results(results, results_by_first_roll)
