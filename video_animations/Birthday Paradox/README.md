# Birthday Problem

**How many people do you need in a room before there's a 50% chance two share a birthday?**

Video explainer and Manim animation source code for the *hanrius* YouTube channel.

---

## The Problem

Most people's instinct is 365 / 2 = 183. The real answer is **23**.

The mistake is asking the wrong question. Instead of "does anyone share *my* birthday" (linear), the right question is "do *any two people* share a birthday" (quadratic). With 23 people there are 253 pairs — 253 chances for a match.

## The Math

Computing the complement is easiest — find P(no match) and subtract from 1.

```
P(no match with n people) = (365/365) · (364/365) · (363/365) · ... · ((365-n+1)/365)
```

At n = 23:

```
P(no match) ≈ 0.4927
P(at least one match) ≈ 0.5073  — just over 50%
```

The probability hits 70% at n = 30, 89% at n = 40, and 99% at n = 57.

---

## Repo Structure

```
birthday-problem/
├── birthday.py     # Full Manim animation source
└── README.md       # This file
```

---

## Running the Animation

### Install dependencies

```bash
# Mac
brew install py-cairo ffmpeg
pip install manim

# Windows / Linux
# See https://docs.manim.community/en/stable/installation.html
```

### Preview individual scenes (fast, low quality)

```bash
manim -pql birthday.py Hook
manim -pql birthday.py WrongIntuition
manim -pql birthday.py RightQuestion
manim -pql birthday.py Complement
manim -pql birthday.py ProbCurve
manim -pql birthday.py Outro
```

### Render the full video (high quality)

```bash
manim -pqh birthday.py BirthdayProblem
```

Output lands in `media/videos/birthday/1080p60/BirthdayProblem.mp4`.

---

## Scenes

| Scene | Class | Description |
|---|---|---|
| 1 | `Hook` | "23" on screen, then the question |
| 2 | `WrongIntuition` | 365/2 = 183 appears and gets crossed out |
| 3 | `RightQuestion` | Pairs vs people, 253 pairs with 23 people |
| 4 | `Complement` | Telescoping product counts down live to 0.4927 |
| 5 | `ProbCurve` | S-curve draws itself, n=23/30/40/57 labeled |
| 6 | `Outro` | Takeaway lines and channel tag |

## Adjusting Timing

Every animation has a `run_time` parameter. Pauses use `self.wait(seconds)`.

```python
self.play(FadeIn(number), run_time=1.5)   # slow the animation
self.wait(3)                               # hold before next animation
```

The countdown in `Complement` is controlled by:
```python
run_time=0.2   # per person step — increase to slow down
```

The curve draw speed in `ProbCurve` is:
```python
self.play(Create(curve), run_time=3)   # increase to draw slower
```

---

## Dependencies

- [Manim Community Edition](https://www.manim.community/) v0.18+
- Python 3.8+
- ffmpeg
- Cairo
