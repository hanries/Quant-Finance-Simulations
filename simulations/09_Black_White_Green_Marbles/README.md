# Marble Probability — Monte Carlo Simulation

A standalone interactive simulation that estimates the probability of a classical combinatorics problem using Monte Carlo methods, and verifies it against the exact analytical answer.

---

## The Problem

> Jake has **200 black**, **400 white**, and **600 green** marbles in a container. He draws marbles one by one without replacement. What is the probability that **at least 1 white and 1 green marble remain** in the container right after the last black marble is drawn?

---

## Exact Answer

$$P = \frac{7}{12} \approx 0.5833$$

### Derivation (Law of Total Probability)

Condition on what the **absolute last marble** in the sequence is. Since each of the 1200 marbles is equally likely to be last:

$$P(\text{last is green}) = \frac{600}{1200} = \frac{1}{2}, \qquad P(\text{last is white}) = \frac{400}{1200} = \frac{1}{3}$$

If the last marble is **black**, the event is impossible (the last black was just drawn with nothing left). So:

$$P[\mathcal{B}] = P[\mathcal{B} \mid \text{last is green}] \cdot \frac{1}{2} + P[\mathcal{B} \mid \text{last is white}] \cdot \frac{1}{3}$$

**Case 1 — last marble is green:** The green at position 1200 is guaranteed to still be in the bag when the last black is drawn. We only need the last black to precede the last white. Among the 600 black+white marbles, each is equally likely to be drawn last among that group — so:

$$P[\mathcal{B} \mid \text{last is green}] = \frac{400}{600} = \frac{2}{3}$$

**Case 2 — last marble is white:** Symmetrically, the white is guaranteed. We only need the last black to precede the last green. Among the 800 black+green marbles:

$$P[\mathcal{B} \mid \text{last is white}] = \frac{600}{800} = \frac{3}{4}$$

**Putting it together:**

$$P[\mathcal{B}] = \frac{2}{3} \cdot \frac{1}{2} + \frac{3}{4} \cdot \frac{1}{3} = \frac{1}{3} + \frac{1}{4} = \frac{7}{12}$$

---

## How the Simulation Works

Rather than shuffling all 1200 marbles each trial (slow), the simulation exploits the same structure as the analytical solution:

1. **Sample the last marble** — draw a uniform random integer in `[0, 1200)`. Map to black/white/green by count.
2. **If last is black** — trial is a loss.
3. **If last is green** — sample one marble uniformly from the 600 black+white marbles. Win if it's white (i.e., index ≥ 200).
4. **If last is white** — sample one marble uniformly from the 800 black+green marbles. Win if it's green (i.e., index ≥ 200).

This reduces each trial to **2 random samples** instead of a full Fisher-Yates shuffle, making it practical to run 10,000 trials instantly in the browser.

---

## Features

| Feature | Description |
|---|---|
| **Live convergence chart** | Plots estimated probability vs. trial count, converging to the 7/12 reference line |
| **Conditional breakdown** | Tracks win rates separately for "last = green" and "last = white" branches, verifying 2/3 and 3/4 |
| **Trial log** | Shows individual trial outcomes with running probability estimate |
| **Speed control** | 1×, 10×, or 100× simulation speed |
| **10,000 trials** | Enough for ~0.5% standard error |

---

## Usage

No dependencies. No build step. Just open the file.

```bash
open marble_montecarlo.html
# or drag into any browser
```

---

## Files

```
marble_montecarlo.html   # Self-contained simulation (HTML + CSS + JS)
README.md
```

---

## Part of the QUANT · DAILY Series

This simulation accompanies an episode of [hanrius](https://youtube.com/@hanrius) — a YouTube channel covering one quant finance interview question per day.
