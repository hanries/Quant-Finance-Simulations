# Coin Parity Simulation

A browser-based simulation for exploring the probability of an even number of heads when flipping coins — with and without a fair coin in the mix.

---

## The Problem

**n coins are laid out in front of you. One is fair, the rest have probability 0 < λ < 1 of showing heads. If all n coins are flipped, what is the probability of an even number of heads?**

The surprising answer: always **1/2**, regardless of λ or n — because the fair coin acts as a perfect parity randomizer.

This simulation lets you verify that result and explore the harder variant where the fair coin is removed.

---

## Two Variants

### With fair coin
- 1 fair coin (p = 1/2) + n−1 biased coins (p = λ)
- **Theory:** P(even) = 1/2 always

### Without fair coin
- n biased coins, each with P(H) = λ
- **Theory:** P(even) = [1 + (1 − 2λ)ⁿ] / 2
- Result now depends on both λ and n

---

## How to Use

1. Open `coin_parity_simulation.html` in any modern browser — no server or install needed.
2. Toggle between **With fair coin** and **Without fair coin** using the tabs.
3. Adjust the three sliders:
   - **n** — number of coins (2–20)
   - **λ** — bias of the non-fair coins (0.01–0.99)
   - **Flips** — number of simulations per run (100–10,000)
4. Click **Run simulation** to flip all coins and record results.
5. The chart tracks the simulated P(even) across repeated runs, plotted against the theoretical dashed line.

---

## The Math

### Why the fair coin forces P(even) = 1/2

Condition on the fair coin using the Law of Total Probability:

```
P(even total) = P(H_fair) · P(odd on rest) + P(T_fair) · P(even on rest)
             = (1/2)(1 − p) + (1/2)(p)
             = 1/2
```

The p terms cancel exactly. It doesn't matter what the biased coins do.

### Without the fair coin — the generating function approach

For n independent coins each with P(H) = λ, encode the probabilities as a polynomial:

```
f(x) = [(1 − λ) + λx]ⁿ
```

Expanding gives f(x) = Σ P(k heads) · xᵏ. Evaluate at x = ±1:

```
f(1)  = 1                          (all probabilities sum to 1)
f(−1) = (1 − 2λ)ⁿ                 (each factor becomes 1 − 2λ)
```

Averaging isolates even terms:

```
P(even) = [f(1) + f(−1)] / 2 = [1 + (1 − 2λ)ⁿ] / 2
```

### Solving the recursion

The same result follows from the recurrence Eₖ = Eₖ₋₁(1 − 2λ) + λ, with E₀ = 1.

Substituting dₖ = Eₖ − 1/2 reduces this to dₖ = (1 − 2λ)dₖ₋₁, giving:

```
Eₙ = 1/2 + (1 − 2λ)ⁿ · (1/2) = [1 + (1 − 2λ)ⁿ] / 2
```

---

## Files

| File | Description |
|------|-------------|
| `coin_parity_simulation.html` | The simulation (self-contained, no dependencies) |
| `README.md` | This file |

---

## Dependencies

None. Chart.js is loaded from a CDN (`cdnjs.cloudflare.com`) at runtime. An internet connection is required for the chart to render.
