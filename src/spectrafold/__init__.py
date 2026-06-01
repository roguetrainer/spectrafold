"""
spectrafold
===========
Exact diagrammatic calculus for spectroscopy.

The Origami ISA — five opcodes (FLIP, FLOP, SPLIT, SPLAT, TWIST) — gives a
universal, exact, compositional language for angular momentum recoupling.
Every result is a sympy expression: no floats, no rounding, no guessing.

  "The colours of fireworks, computed exactly."

Quick start
-----------
>>> from spectrafold.core.opcodes import flop, flip, split, splat, twist
>>> flop(1, 1, 1, 1, 1, 1)          # 6j symbol {1 1 1; 1 1 1}
-1/6
>>> flip(1) * flop(0, 1, 1, 1, 1, 1)  # FLIP;FLOP chain (Pandya sign)
-1/3

>>> from spectrafold.spectroscopy.pandya import pandya_transform
>>> from spectrafold.spectroscopy.g2wall import g2_casimir

Papers
------
347 Spiders for Spectra      doi:10.5281/zenodo.20458996
348 Spiders for Nuclei       doi:10.5281/zenodo.20490046
349 The Origami Calculus      doi:10.5281/zenodo.20474914
350 Spiders for Quarkonium   doi:10.5281/zenodo.20490294
"""

from spectrafold.core.opcodes import (
    flip,
    flop,
    split,
    splat,
    twist,
    twist_eigenvalue,
    wigner3j,
    verify_pentagon,
)

__version__ = "0.1.0"
__author__ = "Ian R. C. Buckley"
__all__ = [
    "flip", "flop", "split", "splat", "twist",
    "twist_eigenvalue", "wigner3j", "verify_pentagon",
]
