"""
spectrafold.spectroscopy.pandya
================================
The Pandya transform as a FLIP;FLOP opcode chain.

The Pandya theorem relates particle-particle (pp) matrix elements to
particle-hole (ph) matrix elements via:

    <j1 j2^{-1}; J | V | j3 j4^{-1}; J> =
        -sum_{J'} (2J'+1) { j1  j2  J' }  <j1 j4; J' | V | j3 j2; J'>
                           { j4  j3  J  }

In the Origami ISA this is a two-instruction program:
    FLIP  — bend the j2 wire through a cap (particle → hole), cost (-1)^{2j2}
    FLOP  — 6j recoupling of the resulting diagram, cost {j1 j2 J'; j4 j3 J}

Paper 348, §3; experiment x353c.
doi:10.5281/zenodo.20490046
"""

from sympy import Rational, sqrt, simplify
from spectrafold.core.opcodes import flip, flop, split


def pandya_transform(j1, j2, j3, j4, J, pp_elements):
    """
    Pandya transform: convert pp matrix elements to ph matrix elements.

    Parameters
    ----------
    j1, j2, j3, j4 : int or half-int
        Single-particle angular momentum quantum numbers.
        The ph matrix element has j2 as the hole (j2^{-1}).
    J : int or half-int
        Total angular momentum of the ph pair.
    pp_elements : dict
        Particle-particle matrix elements {J_prime: <j1 j4; J'|V|j3 j2; J'>}.
        Keys are the intermediate coupling J' values; values are sympy
        expressions or numbers.

    Returns
    -------
    sympy expression
        The exact ph matrix element <j1 j2^{-1}; J|V|j3 j4^{-1}; J>.

    Notes
    -----
    The FLIP cost (-1)^{2j2} accounts for the particle-to-hole conjugation
    (time-reversal of the j2 wire). The FLOP cost is the 6j symbol.
    Both are exact sympy rationals.

    Examples
    --------
    Reproduce x353c (Paper 348): f7/2 shell Pandya check.

    >>> from sympy import Rational
    >>> j = Rational(7, 2)
    >>> # Diagonal pp matrix element
    >>> pp = {Rational(7,2): Rational(-1, 1)}
    >>> ph = pandya_transform(j, j, j, j, Rational(7,2), pp)
    """
    j1, j2, j3, j4, J = (Rational(x) for x in (j1, j2, j3, j4, J))

    flip_cost = flip(j2)   # (-1)^{2j2}

    result = 0
    for J_prime, V_pp in pp_elements.items():
        J_prime = Rational(J_prime)
        # Check triangle inequalities before calling flop
        if not _triangle(j1, j4, J_prime):
            continue
        if not _triangle(j3, j2, J_prime):
            continue
        if not _triangle(j1, j2, J):
            continue
        dim = 2 * J_prime + 1
        sixj = flop(j1, j2, J, j4, j3, J_prime)
        result += dim * sixj * V_pp

    return simplify(flip_cost * (-1) * result)


def _triangle(j1, j2, j3):
    """Check triangle inequality |j1-j2| <= j3 <= j1+j2."""
    j1, j2, j3 = Rational(j1), Rational(j2), Rational(j3)
    return abs(j1 - j2) <= j3 <= j1 + j2


def pandya_sign(j2):
    """
    The FLIP cost for the Pandya transform: (-1)^{2j2+1}.

    This is the sign from bending a spin-j2 wire through a cap
    (time-reversal) and the antisymmetry of the two-body state.

    Parameters
    ----------
    j2 : half-int
        The hole spin.

    Returns
    -------
    sympy.Integer
        +1 or -1.
    """
    j2 = Rational(j2)
    return flip(j2)
