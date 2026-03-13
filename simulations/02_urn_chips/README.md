# 02 — Urn Chip Probability Simulation

An interactive React simulation exploring a classic Bayesian probability problem involving two urns and chip selection under optimal strategy.

## The Problem

You have **2 indistinguishable urns** in front of you:

| Urn | $1 chips | $10 chips | Total |
|-----|----------|-----------|-------|
| Urn 1 | 4 | 6 | 10 |
| Urn 2 | 3 | 7 | 10 |

You reach into one urn at random and draw a **$1 chip**. You then have the opportunity to draw a second chip — either from the **same urn** or from the **other urn**. Your payout is the value of the second chip.

**Under optimal gameplay, what is your expected payout?**

## The Math

### Step 1 — Bayesian posterior after drawing $1

Since the urns are indistinguishable, use Bayes' theorem to update which urn you likely drew from:

$$P(\text{Urn 1} \mid \$1) = \frac{P(\$1 \mid \text{Urn 1}) \cdot P(\text{Urn 1})}{P(\$1)} = \frac{\frac{4}{10} \cdot \frac{1}{2}}{\frac{4}{10} \cdot \frac{1}{2} + \frac{3}{10} \cdot \frac{1}{2}} = \frac{4}{7}$$

$$P(\text{Urn 2} \mid \$1) = \frac{3}{7}$$

### Step 2 — Expected value of each strategy

Because the urns are **indistinguishable**, the player must commit to a single blind strategy (stay or switch) without knowing which urn they drew from.

**Stay (draw second chip from the same urn):**

- If from Urn 1: 3 × $1 and 6 × $10 remain → EV = $7.00
- If from Urn 2: 2 × $1 and 7 × $10 remain → EV = $8.00

$$EV_{\text{stay}} = \frac{4}{7} \times 7 + \frac{3}{7} \times 8 = \frac{28}{7} + \frac{24}{7} = \boxed{\frac{52}{7} \approx \$7.43}$$

**Switch (draw second chip from the other urn):**

- If from Urn 1, switch to Urn 2 (full): EV = $7.30
- If from Urn 2, switch to Urn 1 (full): EV = $6.40

$$EV_{\text{switch}} = \frac{4}{7} \times 7.30 + \frac{3}{7} \times 6.40 = \frac{242}{35} \approx \$6.91$$

### Answer

$$\boxed{EV_{\text{optimal}} = \frac{52}{7} \approx \$7.43}$$

The optimal strategy is to **stay in the same urn**. Intuitively, drawing a $1 chip makes it more likely you're in Urn 1 (which has proportionally more $1 chips), and Urn 1's remaining pool after removing a $1 chip (6 out of 9 are $10) is better than switching to the full Urn 2 (7 out of 10 are $10).

## Simulation Features

- **Step-by-step mode** — draw a chip, see the expected value for stay vs switch, make your choice, observe the payout
- **Bulk simulation** — run 100 / 1,000 / 10,000 trials instantly under either the stay or switch strategy
- **Convergence tracker** — live comparison of simulated average vs theoretical EV for both strategies independently
- **Trial log** — last 80 trials with urn, action, and payout

## Running the Simulation

This component requires React and Tailwind CSS.

```bash
# In a Vite + React project
cp UrnSimulation.jsx src/components/
```

Then import and render:

```jsx
import UrnSimulation from './components/UrnSimulation';

export default function App() {
  return <UrnSimulation />;
}
```

## File Structure

```
02_urn_chips/
├── UrnSimulation.jsx   # Main React component
└── README.md           # This file
```
