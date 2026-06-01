"""
racah.core.opcodes
==================
The five Origami ISA generators, implemented over exact sympy arithmetic.

Every function returns a sympy Rational or expression — never a float.
This is the library's defining property: it can prove things
(e.g. cos(A,B) = 0 exactly) rather than computing 1.43e-16 and guessing.

The five opcodes correspond to the Pachner moves of the 3-simplex
(Ponzano-Regge 1968; Mac Lane 1963; Paper 349):

    FLIP   — evaluation map (cap/cup); time-reversal of a wire
    FLOP   — 6j F-move; the cost of reassociation (Pentagon identity)
    SPLIT  — Frobenius unit; pair creation, opening a J=0 bubble
    SPLAT  — Frobenius counit; pair annihilation, closing a bubble
    TWIST  — ribbon element; spin-orbit phase on a wire

References
----------
Racah (1942) Phys. Rev. 62, 438.
Ponzano & Regge (1968) Spectroscopic and Group Theoretical Methods in Physics.
Mac Lane (1963) Rice Univ. Stud. 49(4), 28.
Buckley (2026) Paper 349: The Origami Calculus. doi:10.5281/zenodo.20474914
"""

from sympy import Rational, sqrt, Integer
from sympy.physics.wigner import wigner_6j, wigner_3j, clebsch_gordan


# ---------------------------------------------------------------------------
# FLIP — evaluation map (cap/cup), time-reversal on a wire of spin j
# ---------------------------------------------------------------------------

def flip(j):
    """
    FLIP opcode: the evaluation map (cap) on a wire of spin j.

    In the pivotal category Rep(SU(2)), bending a wire of spin j through
    a cap introduces a phase factor. For the standard normalisation:

        FLIP(j) = (-1)^{2j}

    For integer j this is +1; for half-integer j this is -1 (Kramers).
    This is the Pandya particle-hole sign (Paper 348, x353c).

    Parameters
    ----------
    j : int or half-int (as Rational or integer)
        The spin label of the wire.

    Returns
    -------
    sympy.Integer
        +1 or -1.

    Examples
    --------
    >>> flip(0)       # scalar wire: no phase
    1
    >>> flip(Rational(1,2))  # spin-1/2: Kramers sign
    -1
    >>> flip(1)       # spin-1: no phase
    1
    """
    j = Rational(j)
    return Integer((-1) ** int(2 * j))


# ---------------------------------------------------------------------------
# FLOP — 6j F-move; the reassociation cost (Pentagon identity)
# ---------------------------------------------------------------------------

def flop(j1, j2, j12, j3, j, j23):
    """
    FLOP opcode: the Wigner 6j symbol {j1 j2 j12; j3 j j23}.

    This is the amplitude for the F-move in Rep(SU(2)):
    reassociating (j1 ⊗ j2) ⊗ j3 → j1 ⊗ (j2 ⊗ j3) costs exactly this
    6j symbol. The Pentagon identity asserts that five FLOPs compose
    to the identity — this is Mac Lane's coherence theorem for monoidal
    categories (Paper 349).

    The 6j symbol is the core of the Racah algebra and the Origami
    calculus. Every spectroscopic recoupling is a product of FLOPs.

    Parameters
    ----------
    j1, j2, j12, j3, j, j23 : int or half-int (Rational)
        The six angular momentum labels of the tetrahedron vertex.
        Standard notation: {j1 j2 j12; j3 j j23}.

    Returns
    -------
    sympy.Rational
        The exact 6j symbol value.

    Examples
    --------
    >>> flop(1, 1, 1, 1, 1, 1)   # {1 1 1; 1 1 1}
    Rational(1, 6)
    >>> flop(0, 1, 1, 1, 1, 1)   # {0 1 1; 1 1 1} — Pandya / X(3872) E1
    Rational(-1, 3)
    """
    return wigner_6j(j1, j2, j12, j3, j, j23)


# ---------------------------------------------------------------------------
# SPLIT — Frobenius unit; quantum dimension of a wire
# ---------------------------------------------------------------------------

def split(j):
    """
    SPLIT opcode: the Frobenius unit on a wire of spin j.

    Opening a J=0 bubble on a spin-j wire evaluates to the quantum
    dimension of the representation:

        SPLIT(j) = sqrt(2j + 1)

    This is the normalisation factor in the Racah algebra that counts
    the number of magnetic substates. For j=0 (scalar wire): SPLIT = 1.
    For j=1/2: SPLIT = sqrt(2). For j=1: SPLIT = sqrt(3).

    In nuclear spectroscopy, SPLIT creates a seniority-zero pair
    (two nucleons coupled to J=0). In quarkonium, SPLIT(0) = 1 is the
    colour-singlet bubble evaluation (Paper 350).

    Parameters
    ----------
    j : int or half-int (Rational)
        The spin label of the wire.

    Returns
    -------
    sympy expression
        sqrt(2j+1), exact.

    Examples
    --------
    >>> split(0)
    1
    >>> split(Rational(1,2))
    sqrt(2)
    >>> split(1)
    sqrt(3)
    >>> split(2)
    sqrt(5)
    """
    j = Rational(j)
    return sqrt(2 * j + 1)


# ---------------------------------------------------------------------------
# SPLAT — Frobenius counit; bubble closure
# ---------------------------------------------------------------------------

def splat(j):
    """
    SPLAT opcode: the Frobenius counit on a wire of spin j.

    Closing a J=0 bubble on a spin-j wire. By the Frobenius axiom,
    SPLIT followed by SPLAT is the identity on the wire:

        SPLAT(j) * SPLIT(j) = 1   =>   SPLAT(j) = 1 / sqrt(2j+1)

    In the standard normalisation used in Racah algebra, the bubble
    normalisation factor is 1/sqrt(2j+1). The SPLAT evaluation
    appears in:
    - Seniority pair annihilation (nuclear shell model)
    - Colour Casimir for SU(3) (quarkonium, Paper 350)
    - Wigner-Eckart reduced matrix element extraction

    Parameters
    ----------
    j : int or half-int (Rational)
        The spin label of the wire.

    Returns
    -------
    sympy expression
        1/sqrt(2j+1), exact.

    Examples
    --------
    >>> splat(0)
    1
    >>> splat(Rational(1,2))
    1/sqrt(2)
    >>> splat(1)
    1/sqrt(3)
    """
    j = Rational(j)
    d = 2 * j + 1
    return Integer(1) / sqrt(d)


# ---------------------------------------------------------------------------
# TWIST — ribbon element; spin-orbit phase on a wire
# ---------------------------------------------------------------------------

def twist(j):
    """
    TWIST opcode: the ribbon element (topological spin) on a wire of spin j.

    In a ribbon category, the twist θ_j is the phase acquired when a wire
    is rotated by 2π:

        TWIST(j) = (-1)^{2j}  × (quantum dimension factor)

    For the standard half-twist (the spin-statistics connection):

        TWIST(j) = (-1)^{2j}

    This is identical to FLIP for SU(2). The distinction matters for
    higher-rank groups (SU(3), G2) where TWIST and FLIP differ.

    In physical applications:
    - Spin-orbit coupling: TWIST eigenvalue = j(j+1) - l(l+1) - s(s+1)
    - Hyperfine splitting: TWIST on the spin-spin operator S_q·S_qbar
      gives eigenvalue [S(S+1) - 3/2]/2 (Paper 350, x354ab)
    - l-type doubling in molecules: TWIST on the vibrational angular
      momentum wire (Paper 353, x356a)

    Parameters
    ----------
    j : int or half-int (Rational)
        The spin label of the wire.

    Returns
    -------
    sympy.Integer
        (-1)^{2j}: +1 for integer j, -1 for half-integer j.

    Notes
    -----
    For the spin-spin TWIST eigenvalue in a qq-bar system with total
    spin S, use twist_eigenvalue(S) instead.

    Examples
    --------
    >>> twist(0)
    1
    >>> twist(Rational(1,2))
    -1
    >>> twist(1)
    1
    """
    j = Rational(j)
    return Integer((-1) ** int(2 * j))


def twist_eigenvalue(S, s_quark=Rational(1, 2)):
    """
    TWIST eigenvalue for the spin-spin operator S_1 · S_2 in a
    composite system with individual spins s_quark and total spin S.

        TWIST(S) = [S(S+1) - 2 s_quark(s_quark+1)] / 2

    Used for hyperfine splittings in quarkonium (Paper 350, x354ab)
    and spin-orbit terms in nuclear spectroscopy.

    Parameters
    ----------
    S : int or half-int (Rational)
        Total spin of the composite system.
    s_quark : Rational, default 1/2
        Individual constituent spin.

    Returns
    -------
    sympy.Rational
        Exact eigenvalue of S_1 · S_2.

    Examples
    --------
    >>> twist_eigenvalue(0)   # singlet: eta_c, eta_b
    Rational(-3, 4)
    >>> twist_eigenvalue(1)   # triplet: J/psi, Upsilon
    Rational(1, 4)
    >>> twist_eigenvalue(1) - twist_eigenvalue(0)  # splitting = 1
    1
    """
    S = Rational(S)
    sq = Rational(s_quark)
    return (S * (S + 1) - 2 * sq * (sq + 1)) / 2


# ---------------------------------------------------------------------------
# Convenience: the 3j symbol (used in E1/M1 transitions, Wigner-Eckart)
# ---------------------------------------------------------------------------

def wigner3j(j1, j2, j3, m1, m2, m3):
    """
    Wigner 3j symbol (exact sympy rational).
    Used in Wigner-Eckart theorem applications and selection rule checks.

    Parameters
    ----------
    j1, j2, j3 : angular momentum quantum numbers
    m1, m2, m3 : magnetic quantum numbers (must satisfy m1+m2+m3=0)

    Returns
    -------
    sympy expression
        Exact 3j symbol.
    """
    return wigner_3j(j1, j2, j3, m1, m2, m3)


# ---------------------------------------------------------------------------
# Pentagon identity verification
# ---------------------------------------------------------------------------

def verify_pentagon(j1, j2, j3, j4, j5):
    """
    Verify the 6j orthogonality relation (a consequence of the Pentagon
    identity) for given spins.

    The orthogonality sum:
        sum_{j12} (2*j12+1) * {j1 j2 j12; j3 j4 j5}^2 = 1 / (2*j5+1)

    This follows from the Pentagon (Biedenhahn-Elliott) identity and
    is the standard machine-checkable form of the coherence condition
    for the monoidal category Rep(SU(2)).  It is the Pachner 2→3 move
    identity (Paper 349).

    Parameters
    ----------
    j1, j2, j3, j4, j5 : int or half-int

    Returns
    -------
    passed : bool — True if the identity holds exactly.
    lhs    : sympy expression — computed sum.
    rhs    : sympy expression — 1/(2*j5+1).
    """
    from sympy import simplify
    from sympy.physics.wigner import wigner_6j as w6j

    j1, j2, j3, j4, j5 = (Rational(x) for x in (j1, j2, j3, j4, j5))

    # Sum over allowed j12 values
    j12_min = abs(j1 - j2)
    j12_max = j1 + j2
    half = Rational(1, 2)

    lhs = Integer(0)
    j12 = j12_min
    while j12 <= j12_max:
        val = w6j(j1, j2, j12, j3, j4, j5)
        lhs += (2 * j12 + 1) * val * val
        j12 += 1

    rhs = Integer(1) / (2 * j5 + 1)
    passed = simplify(lhs - rhs) == 0
    return passed, simplify(lhs), rhs
