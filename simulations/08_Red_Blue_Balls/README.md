# Ball Bag — Monte Carlo Simulation

An interactive browser-based simulation of a classic probability puzzle, built with vanilla HTML, CSS, and JavaScript.

---

## The Puzzle

A bag contains **20 blue balls** and **14 red balls**. Each round you randomly draw two balls, remove them, and add one back according to this rule:

| Balls drawn | Ball added back |
|---|---|
| Same color (both blue or both red) | Blue |
| Different colors (one of each) | Red |

You repeat this until only one ball remains. **What color is the last ball?**

---

## The Math

The key insight is that **the parity of red balls is a conserved invariant** — it never changes throughout the process.

Every possible draw changes the red ball count by exactly **0 or −2**:

- Two blues drawn → add blue: red count unchanged (Δ = 0)
- Two reds drawn → add blue: red count decreases by 2 (Δ = −2)
- One of each drawn → add red: red count goes −1 + 1 = 0 (Δ = 0)

Since the parity of red balls is preserved, the outcome is fully determined by the **initial red ball count**:

- **Even number of red balls** → red count stays even → can never reach 1 (odd) → **last ball is always blue**
- **Odd number of red balls** → red count stays odd → can reach exactly 1 → **last ball is always red**

The number of blue balls is irrelevant.

### The two cases from the puzzle

| Setup | Red count | Parity | Last ball |
|---|---|---|---|
| 20 blue, 14 red | 14 | Even | Blue |
| 20 blue, 13 red | 13 | Odd | Red |

---

## Features

- **Configurable inputs** — set any number of blue balls, red balls, and simulation count
- **Run simulation** — executes up to 100,000 independent trials and reports results
- **Reset button** — clears all results and restores default values (20 blue, 14 red, 10,000 sims)
- **Result distribution** — animated bar chart showing blue vs red outcome percentages
- **Theoretical prediction** — explains the parity invariant for the current input values
- **Sample trace chart** — line chart showing how blue, red, and total ball counts evolve over rounds in a single simulation run, rendered with Chart.js

---

## Usage

No installation or build step required. Just open the file in any modern browser:

```bash
open ball_monte_carlo.html
# or double-click ball_monte_carlo.html
```

Requires an internet connection on first load to fetch fonts (Google Fonts) and the Chart.js library from the Cloudflare CDN. After the first load, Chart.js is cached by the browser.

---

## Files

| File | Description |
|---|---|
| `ball_monte_carlo.html` | The simulation — self-contained, single file |
| `README.md` | This file |

---

## Implementation Notes

**Simulation logic (`simulate` function)**

Each round, two balls are drawn without replacement using weighted random sampling. The function returns the color of the last remaining ball and a full trace array of `[blue, red, total]` counts at each round — used to render the sample trace chart.

**Why the result is always deterministic**

The simulation confirms 100% of outcomes match the theoretical prediction. Try any values: as long as the red count is even, every single trial ends on blue; odd red count means every trial ends on red. The blue count has zero effect.

**Dependencies**

- [Chart.js 4.4.1](https://www.chartjs.org/) — loaded from `cdnjs.cloudflare.com`
- [DM Mono](https://fonts.google.com/specimen/DM+Mono) + [Fraunces](https://fonts.google.com/specimen/Fraunces) — loaded from Google Fonts

---

## License

Free to use and modify.
