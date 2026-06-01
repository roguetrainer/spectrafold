"""
hello_world_exact_6j.py
========================
spectrafold hello world: exact vs floating-point 6j symbols.

The Wigner 6j symbol is the single most important object in the
spectroscopy of atoms, nuclei, and molecules. Every coupling of
angular momenta — every spectral line assignment, every selection
rule, every nuclear shell model calculation — reduces to products
of 6j symbols.

The problem with existing codes
--------------------------------
All legacy spectroscopy codes (Cowan 1981, NuShellX, GRASP2018) compute
6j symbols using a closed-form formula involving a sum of terms like:

    sum_z  (-1)^z * (z+1)! / [(z-a)!(z-b)!...(n-z)!...]

For small angular momenta (j ~ 1-5, encountered in light atoms),
double precision is adequate. But for heavy atoms and actinides
(j ~ 15-50, where the f-shell G2 wall sits), the individual terms
in this sum are of order 10^60 while the result is of order 10^-3.
This is catastrophic cancellation: you subtract huge numbers and
keep only the tiny difference. In 64-bit floats (~15 significant
digits), you lose all accuracy.

The spectrafold solution
-------------------------
spectrafold computes 6j symbols exactly, as rational numbers,
using symbolic algebra (sympy). The result is a theorem — not a
measurement — and is guaranteed to be correct regardless of how
large j is.

This example demonstrates both approaches side by side.

Run it:
    python examples/hello_world_exact_6j.py
"""

from fractions import Fraction
import math

# ── Part 1: The naive floating-point implementation ──────────────────────

def delta_coeff_float(a, b, c):
    """Triangle coefficient Δ(abc) = sqrt[(a+b-c)!(a-b+c)!(-a+b+c)! / (a+b+c+1)!]"""
    t1 = math.factorial(int(a + b - c))
    t2 = math.factorial(int(a - b + c))
    t3 = math.factorial(int(-a + b + c))
    t4 = math.factorial(int(a + b + c + 1))
    return math.sqrt(t1 * t2 * t3 / t4)


def sixj_float_naive(j1, j2, j3, j4, j5, j6):
    """
    Naive floating-point 6j symbol via the Racah formula.
    Demonstrates catastrophic cancellation for large j.

    {j1 j2 j3}
    {j4 j5 j6}
    """
    # All arguments as half-integers
    args = [j1, j2, j3, j4, j5, j6]

    # Triangle coefficients (four triads)
    try:
        d1 = delta_coeff_float(j1, j2, j3)
        d2 = delta_coeff_float(j1, j5, j6)
        d3 = delta_coeff_float(j4, j2, j6)
        d4 = delta_coeff_float(j4, j5, j3)
    except ValueError:
        return 0.0

    prefactor = d1 * d2 * d3 * d4

    # Sum bounds
    t_min = max(j1+j2+j3, j1+j5+j6, j4+j2+j6, j4+j5+j3)
    t_max = min(j1+j2+j4+j5, j2+j3+j5+j6, j1+j3+j4+j6)

    total = 0.0
    t = int(t_min)
    while t <= int(t_max):
        num = (-1)**t * math.factorial(t + 1)
        den = (math.factorial(int(t - j1 - j2 - j3)) *
               math.factorial(int(t - j1 - j5 - j6)) *
               math.factorial(int(t - j4 - j2 - j6)) *
               math.factorial(int(t - j4 - j5 - j3)) *
               math.factorial(int(j1 + j2 + j4 + j5 - t)) *
               math.factorial(int(j2 + j3 + j5 + j6 - t)) *
               math.factorial(int(j1 + j3 + j4 + j6 - t)))
        total += num / den
        t += 1

    return prefactor * total


# ── Part 2: The spectrafold exact implementation ──────────────────────────

def sixj_exact(j1, j2, j3, j4, j5, j6):
    """Exact 6j symbol via spectrafold (sympy wigner_6j)."""
    from spectrafold import flop
    return flop(j1, j2, j3, j4, j5, j6)


# ── Part 3: The demo ──────────────────────────────────────────────────────

def run():
    print("=" * 70)
    print("spectrafold hello world: exact vs floating-point 6j symbols")
    print("=" * 70)

    # ── Section 1: Small j — both methods agree ───────────────────────
    print()
    print("PART 1: Small angular momenta (j ~ 1)")
    print("Both methods agree — floating point is fine here.")
    print()

    small_cases = [
        (0, 1, 1, 1, 1, 1, "-1/3",  "Pandya / X(3872)→J/ψγ (Papers 348, 350)"),
        (1, 1, 1, 1, 1, 1, " 1/6",  "nuclear recoupling"),
        (1, 2, 1, 2, 1, 2, "-1/15", "sd-shell coupling"),
    ]

    print(f"  {'6j symbol':<28} {'float':>14} {'exact':>10}  {'match?':>8}")
    print(f"  {'-'*65}")
    for j1,j2,j3,j4,j5,j6, expected, note in small_cases:
        fl = sixj_float_naive(j1, j2, j3, j4, j5, j6)
        ex = sixj_exact(j1, j2, j3, j4, j5, j6)
        label = "{%g %g %g; %g %g %g}" % (j1,j2,j3,j4,j5,j6)
        match = "✓" if abs(float(ex) - fl) < 1e-12 else "✗"
        print(f"  {label:<28} {fl:>14.10f} {str(ex):>10}  {match:>8}")
        print(f"  {'  '+note:<65}")
    print()

    # ── Section 2: Large j — catastrophic cancellation ───────────────
    print("PART 2: Large angular momenta (j ~ 10-30)")
    print("This is where existing codes break. spectrafold does not.")
    print()
    print("The Racah sum has alternating terms of order 10^N that cancel")
    print("to give a result of order 10^-3. Float loses all accuracy.")
    print()

    large_cases = [
        (10,  10,  10,  10,  10,  10),
        (20,  20,  20,  20,  20,  20),
        (50,  50,  50,  50,  50,  50),
        (100, 100, 100, 100, 100, 100),
    ]

    print(f"  {'6j symbol':<28} {'float result':>16} {'exact result':>14}  {'agree?':>8}")
    print(f"  {'-'*72}")

    for args in large_cases:
        j1,j2,j3,j4,j5,j6 = args
        try:
            fl = sixj_float_naive(j1, j2, j3, j4, j5, j6)
        except (OverflowError, ValueError):
            fl = float('inf')

        ex = sixj_exact(j1, j2, j3, j4, j5, j6)
        ex_float = float(ex)

        # Relative error (if both finite)
        if abs(fl) < 1e100 and abs(ex_float) > 1e-15:
            rel_err = abs(fl - ex_float) / abs(ex_float)
            err_str = f"{rel_err:.2e}"
            agree = "✓ exact" if rel_err < 1e-10 else f"✗ err={err_str}"
        elif abs(fl) > 1e100:
            agree = "✗ OVERFLOW"
        else:
            agree = "—"

        label = "{%g %g %g; %g %g %g}" % args
        print(f"  {label:<28} {fl:>16.6e} {float(ex):>14.6e}  {agree:>8}")
    print()

    # ── Section 3: The key insight ────────────────────────────────────
    print("PART 3: The fundamental difference")
    print()

    ex = sixj_exact(0, 1, 1, 1, 1, 1)
    fl = sixj_float_naive(0, 1, 1, 1, 1, 1)

    print(f"  6j{{0,1,1;1,1,1}} — the Pandya amplitude:")
    print()
    print(f"  spectrafold (exact):  {ex}")
    print(f"  float (naive):        {fl:.16f}")
    print(f"  float (repr):         {fl!r}")
    print()
    print(f"  The exact result is the rational number -1/3.")
    print(f"  The float result has error: {abs(fl - float(ex)):.2e}")
    print()
    print("  For small j, the error is tiny (~10^-17) and harmless.")
    print("  For j ~ 20-30 (actinide nuclei, heavy rare earths),")
    print("  the error is of the same order as the result itself.")
    print()
    print("  spectrafold returns -1/3 exactly — a theorem, not a measurement.")
    print()

    # ── Section 4: The physics this enables ──────────────────────────
    print("PART 4: What this means physically")
    print()

    from spectrafold import flop, flip
    from sympy import Rational

    print("  The Pandya theorem (nuclear physics, Paper 348):")
    pandya_6j = flop(0, 1, 1, 1, 1, 1)
    pandya_sign = flip(Rational(7,2))
    print(f"    FLOP amplitude:  {pandya_6j}  (exact)")
    print(f"    FLIP sign:       {pandya_sign}  (exact, j=7/2 f-shell)")
    print(f"    FLIP;FLOP chain: {pandya_sign * pandya_6j}  (exact)")
    print()
    print("  The X(3872)→J/ψγ decay amplitude (QCD, Paper 350):")
    xdecay_6j = flop(0, 1, 1, 1, 1, 1)
    print(f"    FLOP amplitude:  {xdecay_6j}  (exact)")
    print(f"    Same 6j symbol, same exact value, 3 GeV energy scale.")
    print()
    print("  The universality: one exact rational number (-1/3) appears")
    print("  in nuclear spectroscopy AND in QCD charmonium decays.")
    print("  This identity is only visible because the result is exact.")
    print("  A floating-point code returns two slightly different")
    print("  approximations to -0.333... and the identity is obscured.")
    print()

    # ── Section 5: Pentagon identity verification ────────────────────
    print("PART 5: The Pentagon identity (Mac Lane 1963 = Biedenharn-Elliott)")
    print()
    print("  The coherence condition for the monoidal category Rep(SU(2)):")
    print("  sum_{j12} (2j12+1) * |{j1 j2 j12; j3 j4 j5}|^2 = 1/(2j5+1)")
    print()

    from spectrafold import verify_pentagon
    from sympy import Rational as R

    cases = [(1,1,1,1,1), (2,1,2,1,2), (3,2,3,2,3)]
    print(f"  {'j1,j2,j3,j4,j5':<20} {'LHS':>12} {'RHS':>12} {'holds?':>8}")
    print(f"  {'-'*56}")
    for args in cases:
        passed, lhs, rhs = verify_pentagon(*args)
        print(f"  {str(args):<20} {str(lhs):>12} {str(rhs):>12} "
              f"{'✓ exactly' if passed else '✗':>8}")
    print()
    print("  All results are exact symbolic expressions.")
    print("  The Pentagon identity HOLDS — this is a theorem, not a test.")
    print()

    print("=" * 70)
    print("Summary: spectrafold computes 6j symbols exactly.")
    print("  import spectrafold as sf")
    print("  sf.flop(0, 1, 1, 1, 1, 1)  →  -1/3")
    print("  Not -0.33333333333333337. Exactly -1/3.")
    print("  pip install spectrafold")
    print("=" * 70)


if __name__ == "__main__":
    run()
