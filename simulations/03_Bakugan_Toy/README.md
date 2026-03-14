# Bakugan vs Beyblade — Monte Carlo Simulation

A browser-based Monte Carlo simulation that estimates the probability that the **3rd Bakugan is manufactured before the 2nd Beyblade**, where each toy's production time follows an Exponential(1) distribution.

## The Problem

Two machines run independently:
- **Machine B** produces Bakugan toys, each taking Exp(1) time
- **Machine Y** produces Beyblade toys, each taking Exp(1) time

At each step, whichever machine finishes first produces its toy. The question is:

> **What is the probability that the 3rd Bakugan appears before the 2nd Beyblade?**

The true analytical answer is **5/16 = 0.3125**.

## How It Works

Each simulation round works as follows:

1. Draw two independent Exp(1) random variables — one per machine
2. The smaller value wins that slot, labelled **B** (Bakugan) or **Y** (Beyblade)
3. Repeat until either the **3rd B** or **2nd Y** appears
4. Record the winner

To generate Exp(1) random variables in JavaScript, the [inverse transform method](https://en.wikipedia.org/wiki/Inverse_transform_sampling) is used:

```js
function expRandom() {
  return -Math.log(1 - Math.random());
}
```

This works because if `U ~ Uniform(0,1)`, then `-log(U) ~ Exp(1)`.

As more simulations are run, the estimated probability converges to **5/16** by the Law of Large Numbers.

## Features

- Run **1, 100, 1,000, or 10,000** simulations at a time
- **Live convergence chart** showing the estimated probability approaching the true answer
- **Step-by-step replay** of the last single simulation showing the toy sequence
- Reset button to start fresh

## Usage

No installation or dependencies required. Just open the HTML file in any modern browser:

```
open bakugan_simulation.html
```

## Tech Stack

- Vanilla HTML/CSS/JavaScript
- [Chart.js 4.4.1](https://www.chartjs.org/) for the convergence chart (loaded via CDN)
