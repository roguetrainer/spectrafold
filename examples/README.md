# spectrafold examples

Runnable Python scripts demonstrating the spectrafold library.
Each script is self-contained and prints results to stdout.

## Running

```bash
pip install spectrafold
python examples/hello_world_exact_6j.py
```

## Scripts

| Script | What it demonstrates |
|--------|---------------------|
| [hello_world_exact_6j.py](hello_world_exact_6j.py) | The killer feature: exact vs floating-point 6j symbols. Shows catastrophic cancellation in naive float computation vs exact rational result from spectrafold. The hello-world example for why exact arithmetic matters. |

## Annotated notebooks

The `docs/tutorials/` folder contains Jupyter notebook versions with
prose explanations, equations, and plots.

## The one-line pitch

```python
from spectrafold import flop
flop(0, 1, 1, 1, 1, 1)   # → -1/3  (exact rational, not -0.33333333333333337)
```
