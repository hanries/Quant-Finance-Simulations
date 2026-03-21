# Monte Carlo: P(T < G < P)

A standalone browser simulation for the coin flip ordering problem.

## The Problem

Ty, Guy, and Psy each flip a fair coin until they get their first heads. Let T, G, and P be the number of flips each needs. What is P(T < G < P)?

**Exact answer: 1/21 ≈ 0.04762**

## The Math

T, G, and P are independent Geometric(1/2) random variables, where:

```
P(X = k) = (1/2)^k,  k = 1, 2, 3, ...
```

We want the probability that all three finish in strict order. By summing over every valid triple (t, g, p) with t < g < p:

```
P(T < G < P) = Σ_{t=1}^∞  Σ_{g=t+1}^∞  Σ_{p=g+1}^∞  (1/2)^t (1/2)^g (1/2)^p
```

Evaluating from the inside out using the geometric series formula:

- Inner sum over p:   Σ_{p=g+1}^∞ (1/2)^p = (1/2)^g
- Middle sum over g:  Σ_{g=t+1}^∞ (1/4)^g  = (1/3)(1/4)^t
- Outer sum over t:   (1/3) Σ_{t=1}^∞ (1/8)^t = (1/3)(1/7) = **1/21**

## Symmetry Check

There are 6 strict orderings of (T, G, P). By symmetry of i.i.d. variables, each is equally likely. They each have probability 1/21, summing to 6/21 = 2/7. The remaining 5/7 is the probability that at least two values tie.

## How to Use

Open `monte_carlo_TGP.html` in any browser — no dependencies, no server needed.

- **Slider** — choose how many simulations to run per batch (1,000 to 100,000)
- **Run** — executes the batch and adds a point to the convergence graph
- **Reset** — clears all history and starts fresh
- **Convergence graph** — tracks the cumulative estimate against the exact answer (dashed line)
- **Ordering distribution** — shows the empirical frequency of all 6 strict orderings plus ties
- **Sample log** — displays the first 12 raw (T, G, P) triples from the last run

## Files

```
monte_carlo_TGP.html   — simulation (self-contained, no install needed)
README.md              — this file
```
