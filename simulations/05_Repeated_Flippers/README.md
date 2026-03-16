# Coin Flip Simulation

An interactive browser simulation of a classic probability problem — no dependencies, no build step, just open the HTML file.

---

## The Problem

Start with **N fair coins** lined up. Each round, flip all surviving coins simultaneously. Remove every coin that lands tails. Repeat until one of two outcomes:

- **All-heads** — every surviving coin shows heads on the same round
- **Exhausted** — all remaining coins are removed in the same round

**What is the probability of ending by all-heads?**

The answer is exactly **1/2**, regardless of how many coins you start with. This simulation lets you verify that empirically.

### Why 1/2?

On every round, either all surviving coins show heads (win) or at least one shows tails (game continues or ends by exhaustion). By the memoryless nature of fair coin flips, neither path is favored over the other — so the probability is exactly 50% no matter what N is.

---

## Usage

```
open coin_simulation.html
```

No server, no install, no dependencies. Works in any modern browser.

| Control | Description |
|---|---|
| Coins slider | Set starting coin count (1–50) |
| Play 1 game | Watch an animated game unfold round by round |
| 10 / 100 / 1k / 10k | Run batch games instantly for fast statistics |
| Speed slider | Control animation speed (very slow → instant) |
| Reset all | Clear all data and start fresh |

---

## Features

- **Animated playback** — coins reveal H/T, tails shrink and fade out, surviving heads remain
- **Round history** — every round logged with heads kept and tails removed
- **Running probability chart** — tracks observed all-heads % over all games played, with a 50% reference line
- **Adjustable coin count** — change N at any time; theoretical probability stays 50%

---

## How the Animation Works

The animation uses **CSS transitions** + **JavaScript async/await** — no external library.

Each coin is a `div` with a class that defines its visual state. Swapping the class triggers a browser-native smooth transition:

```css
.coin {
  transition: background 0.22s ease, opacity 0.32s ease, transform 0.32s ease;
}

.coin.s-idle   { background: #1c1c21; opacity: 1; transform: scale(1);   }
.coin.s-heads  { background: #2a3d1a; opacity: 1; transform: scale(1);   }
.coin.s-tails  { background: #3d2a1a; opacity: 1; transform: scale(1);   }
.coin.s-remove {                      opacity: 0; transform: scale(0.3); }
.coin.s-gone   {                      opacity: 0; /* holds layout space */}
```

Each round plays out in three phases:

```js
const sleep = ms => new Promise(r => setTimeout(r, ms));

// Phase 1 — reveal flip result on every active coin
for (let i = 0; i < n; i++) setCoin(i, flipped[i] ? 's-heads' : 's-tails', ...);
await sleep(ms);

// Phase 2 — shrink tails coins away
for (let i = 0; i < n; i++) if (isTails[i]) setCoin(i, 's-remove', ...);
await sleep(ms * 0.5);

// Phase 3 — collapse to invisible (but keep layout space so grid stays stable)
for (let i = 0; i < n; i++) if (isTails[i]) setCoin(i, 's-gone', ...);
```

The `s-gone` class is invisible but still occupies space in the flex grid — this prevents the surviving coins from jumping around after each removal.

---

## The Win Condition Bug

A subtle bug to watch out for when implementing this yourself:

```js
// WRONG — compares against the original starting count
// Once any coin is removed, headsCount can never reach numCoins again
// This makes a win literally impossible → always shows 100% exhausted
if (headsCount === numCoins) return { outcome: 'heads' };

// CORRECT — compares against coins alive this round
// Fires whenever all currently surviving coins flip heads simultaneously
if (headsCount === prevCount) return { outcome: 'heads' };
```

---

## File Structure

Everything lives in a single `coin_simulation.html` file:

```
coin_simulation.html
├── <style>          dark theme, coin state classes, chart, layout
├── HTML             settings, stats, chart, live game, round history panels
└── <script>
    ├── simulate()       core game logic — flips coins, returns outcome + round data
    ├── animateGame()    async playback loop with phase timing
    ├── drawChart()      canvas-based running probability chart
    ├── runMany()        batch runner — no animation, pure statistics
    └── resetAll()       clears all state
```

---

## Browser Compatibility

Requires support for CSS transitions, CSS custom properties, `async/await`, and HTML5 Canvas — available in all modern browsers.
