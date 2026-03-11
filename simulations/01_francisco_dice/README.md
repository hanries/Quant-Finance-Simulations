01 · Francisco's Dice Roll
The Problem
Francisco rolls a fair six-sided die and records the value. He then keeps rolling until he gets a value at least as large as his first roll.
Let N = number of rolls after the first. Find E[N].
The Math
For a first roll of value k, each subsequent roll succeeds with probability:
p_k = (7 - k) / 6
Since rolls are independent Bernoulli trials, N follows a Geometric distribution:
E[N | k] = 1 / p_k = 6 / (7 - k)
Averaging over all first rolls (each equally likely):
E[N] = (1/6) * sum over k=1..6 of [6 / (7-k)]
     = 1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6
     = 49/20
     = 2.45
This is H₆, the 6th Harmonic Number.
Breakdown by First Roll
kP(success)Exact E[N|k]16/6 = 1.0001.0025/6 ≈ 0.8331.2034/6 ≈ 0.6671.5043/6 = 0.5002.0052/6 ≈ 0.3333.0061/6 ≈ 0.1676.00
Running the Simulation
bashpip install matplotlib numpy
python simulation.py
This will:

Run 100,000 simulations
Print a summary comparing simulated vs exact E[N]
Generate a results.png with 5 visualizations
