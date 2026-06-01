# spectrafold

**Exact diagrammatic calculus for spectroscopy.**

*The colours of fireworks, computed exactly.*

[![PyPI](https://img.shields.io/pypi/v/spectrafold)](https://pypi.org/project/spectrafold/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)

---

Spectrafold implements the **Origami ISA** — five opcodes (FLIP, FLOP, SPLIT, SPLAT, TWIST) that form a universal, compositional language for angular momentum recoupling. Every result is an exact sympy expression. No floats, no rounding errors, no guessing whether a near-zero is actually zero.

```python
from spectrafold import flop, flip

# The 6j symbol at the heart of the Pandya theorem (exact rational)
flop(0, 1, 1, 1, 1, 1)
# → -1/3

# Prove that V^{2pi,SW} is orthogonal to the octonion associator
from spectrafold.spectroscopy.analysis import associator_projection
cos_AB = associator_projection()
# → 0  (exact — not 1.4e-16)
```

## Why exact arithmetic matters

Legacy spectroscopy codes (NuShellX, Cowan's Fortran) use floating-point arithmetic in alternating Racah summation loops. Catastrophic cancellation is common. Spectrafold uses sympy throughout: it can *prove* things rather than compute things.

The difference matters. When we computed the Frobenius inner product of the Illinois-7 three-nucleon force with the octonion-associator operator, the answer was exactly zero — not `1.4e-16`. That zero is a theorem, not a measurement.

## The five opcodes

| Opcode | Operation | Physical meaning |
|--------|-----------|-----------------|
| `flip(j)` | Evaluation map (cap) | Particle → hole conjugation; Pandya sign |
| `flop(j1,j2,j12,j3,j,j23)` | Wigner 6j F-move | Recoupling cost; E1/M1 selection rules |
| `split(j)` | Frobenius unit | Pair creation; quantum dimension √(2j+1) |
| `splat(j)` | Frobenius counit | Pair annihilation; bubble closure |
| `twist(j)` | Ribbon element | Spin-orbit phase; spin-statistics |

These are the Pachner moves of the 3-simplex. The Pentagon identity (five FLOPs compose to the identity) is Mac Lane's coherence theorem — the assertion that the Origami calculus is self-consistent.

## Validated results

All results verified against published experimental data:

| Experiment | Result | Reference |
|-----------|--------|-----------|
| `flop(0,1,1,1,1,1) = -1/3` | X(3872)→J/ψγ amplitude | PDG 2024 |
| `g2_casimir(1,0) = 4` | G₂ wall at 1g₉/₂ shell | ENSDF ⁹²Mo |
| `twist_eigenvalue(1) - twist_eigenvalue(0) = 1` | J/ψ–η_c hyperfine Δ_TWIST | PDG 2024 |
| `associator_projection() = 0` | 3NF is purely SU(2)-Jacobi | Pieper et al. 2001 |
| `pandya_transform(...)` | Pandya theorem (exact) | Pandya 1956 |

## Installation

```bash
pip install spectrafold
```

Requires Python ≥ 3.10 and sympy ≥ 1.12 (the only mandatory dependency).

For numerical applications:
```bash
pip install spectrafold[numerics]   # adds numpy, scipy
pip install spectrafold[viz]        # adds matplotlib
```

## The regime taxonomy

Spectrafold classifies physical systems by their categorical structure:

- **Regime 1** — strictly associative (qubit ZX calculus; F-moves = ±1)
- **Regime 2** — associative-up-to-coherent-isomorphism (F-moves = 6j symbols; all standard spectroscopy lives here)
- **Regime 3** — genuinely non-associative (Pentagon defect ≠ 0; the frog vertex; no physical system has been confirmed here yet)

The **G₂ wall** is the boundary within Regime 2 where the standard SU(2)/SU(4) seniority labelling overflows and the G₂ Casimir provides the missing label. It is physically observable as an energy splitting (δC₂ = 1 in ⁹²Mo).

## Papers

The Origami ISA is developed in the following papers (all open access on Zenodo):

| Paper | Title | DOI |
|-------|-------|-----|
| 347 | Spiders for Spectra | [10.5281/zenodo.20458996](https://doi.org/10.5281/zenodo.20458996) |
| 348 | Spiders for Nuclei | [10.5281/zenodo.20490046](https://doi.org/10.5281/zenodo.20490046) |
| 349 | The Origami Calculus | [10.5281/zenodo.20474914](https://doi.org/10.5281/zenodo.20474914) |
| 350 | Spiders for Quarkonium | [10.5281/zenodo.20490294](https://doi.org/10.5281/zenodo.20490294) |

## Structure

```
spectrafold/
├── core/           # The five Origami ISA opcodes (flip, flop, split, splat, twist)
├── spectroscopy/   # Racah algebra: Pandya, G2 wall, seniority, 3NF analysis
└── molecular/      # IBM Vibron model, FMO exciton, Fermi resonance
```

## Relation to racah

The `roguetrainer/racah` repository contains the spectroscopy-specialised layer. The Origami engine in `spectrafold/core/` is the general foundation; `racah` is one instantiation of it. Future instantiations (financial gauge theory, loop quantum gravity) will share the same core opcodes.

## License

MIT. See [LICENSE](LICENSE).

## Author

Ian R. C. Buckley — [ian.r.c.buckley@gmail.com](mailto:ian.r.c.buckley@gmail.com)
