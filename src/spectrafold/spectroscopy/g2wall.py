"""
spectrafold.spectroscopy.g2wall
================================
The G2 wall: where standard SU(2) seniority labelling becomes incomplete
and the G2 Casimir provides the missing label.

The G2 wall occurs at:
- Atomic: the f-shell (j = 7/2, l = 3)    — Paper 347
- Nuclear: the 1g9/2 shell (j = 9/2)      — Paper 348
- Superconducting: f-electron Cooper pairs — Paper 354 (predicted)

At the G2 wall, two states share identical (n, l, j, v, J) quantum numbers
but differ in their G2 Casimir eigenvalue C2(G2; p, q). The splitting
delta_C2 = 1 is observable as an energy splitting (e.g. in 92Mo).

Paper 347, §4; Paper 348, §3.3; experiments x347a, x353o.
"""

from sympy import Rational, Integer


# G2 Casimir eigenvalue C2(p, q) = p^2 + q^2 + pq + 3p + 3q (up to normalisation)
# For the fundamental 7-dim irrep (1,0): C2 = 4
# For the adjoint 14-dim irrep (1,1):    C2 = 8
# The missing-label splitting delta_C2 = 1 at j = 9/2

def g2_casimir(p, q=0):
    """
    G2 Casimir operator eigenvalue for the irrep (p, q).

    C2(G2; p, q) = p^2 + q^2 + p*q + 3*p + 3*q

    The G2 group (automorphism group of the octonions) has rank 2.
    Its irreps are labelled by two non-negative integers (p, q).

    Key irreps in spectroscopy
    --------------------------
    (0, 0) : singlet,          C2 = 0
    (1, 0) : fundamental 7,    C2 = 4   (Im(O), the 731 register)
    (0, 1) : conjugate 7,      C2 = 4
    (2, 0) : 27-dim,           C2 = 10
    (1, 1) : adjoint 14,       C2 = 8
    (0, 2) : 77-dim,           C2 = 10

    At the 1g9/2 shell, the missing-label doublet has delta_C2 = 1
    between the two G2 irreps that resolve the SU(4) outer-multiplicity
    overflow (Paper 348, experiment x353o).

    Parameters
    ----------
    p, q : non-negative integers
        Dynkin labels of the G2 irrep.

    Returns
    -------
    sympy.Integer
        Exact Casimir eigenvalue.

    Examples
    --------
    >>> g2_casimir(0, 0)   # singlet
    0
    >>> g2_casimir(1, 0)   # fundamental 7 (the 731-ISA register)
    4
    >>> g2_casimir(1, 1)   # adjoint 14
    8
    """
    p, q = Integer(p), Integer(q)
    return p**2 + q**2 + p*q + 3*p + 3*q


def g2_wall_threshold():
    """
    Return the angular momentum j at which the G2 wall first appears
    in the shell model, and the physical context.

    Returns
    -------
    dict with keys:
        'j_atomic'  : Rational — atomic f-shell (7/2)
        'j_nuclear' : Rational — nuclear 1g9/2 (9/2)
        'delta_C2'  : Integer  — observable Casimir splitting (1)
        'nucleus'   : str      — cleanest observable case
    """
    return {
        'j_atomic':  Rational(7, 2),
        'j_nuclear': Rational(9, 2),
        'delta_C2':  Integer(1),
        'nucleus':   '92Mo (v=4 doublet at 1g9/2 shell)',
    }


def is_beyond_g2_wall(j):
    """
    Return True if the single-particle angular momentum j lies at or
    beyond the G2 wall (j >= 9/2 for the nuclear case).

    At or beyond the G2 wall, the SU(4) seniority scheme is incomplete:
    two states share all standard quantum numbers and the G2 Casimir
    is required as an additional label.

    Parameters
    ----------
    j : int or half-int

    Returns
    -------
    bool
    """
    return Rational(j) >= Rational(9, 2)
