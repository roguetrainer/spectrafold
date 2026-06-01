"""
Tests for the five Origami ISA opcodes.
All assertions use exact sympy arithmetic — no tolerances needed.
"""
import pytest
from sympy import Rational, sqrt, Integer
from spectrafold.core.opcodes import (
    flip, flop, split, splat, twist, twist_eigenvalue, verify_pentagon
)


class TestFlip:
    def test_scalar(self):
        assert flip(0) == 1

    def test_half_integer(self):
        assert flip(Rational(1, 2)) == -1

    def test_integer(self):
        assert flip(1) == 1
        assert flip(2) == 1

    def test_f_shell(self):
        # f7/2 shell: flip = (-1)^7 = -1
        assert flip(Rational(7, 2)) == -1

    def test_g_shell(self):
        # 1g9/2 shell: flip = (-1)^9 = -1
        assert flip(Rational(9, 2)) == -1


class TestFlop:
    def test_known_6j(self):
        # {1 1 1; 1 1 1} = +1/6
        assert flop(1, 1, 1, 1, 1, 1) == Rational(1, 6)

    def test_pandya_6j(self):
        # {0 1 1; 1 1 1} = -1/3  (X(3872) E1 decay, Paper 350 x354f)
        assert flop(0, 1, 1, 1, 1, 1) == Rational(-1, 3)

    def test_triangle_violation_zero(self):
        # Violates triangle inequality: result should be 0
        assert flop(0, 0, 1, 0, 0, 1) == 0

    def test_symmetry(self):
        # 6j symbol is symmetric under interchange of columns
        j1, j2, j3, j4, j5, j6 = 1, 2, 1, 2, 1, 2
        assert flop(j1, j2, j3, j4, j5, j6) == flop(j2, j1, j3, j5, j4, j6)


class TestSplit:
    def test_scalar(self):
        assert split(0) == 1

    def test_half(self):
        assert split(Rational(1, 2)) == sqrt(2)

    def test_one(self):
        assert split(1) == sqrt(3)

    def test_two(self):
        assert split(2) == sqrt(5)

    def test_frobenius_axiom(self):
        # SPLIT(j) * SPLAT(j) = 1
        for j in [0, Rational(1, 2), 1, Rational(3, 2), 2]:
            assert split(j) * splat(j) == 1


class TestSplat:
    def test_scalar(self):
        assert splat(0) == 1

    def test_half(self):
        from sympy import sqrt
        assert splat(Rational(1, 2)) == 1 / sqrt(2)

    def test_inverse_of_split(self):
        for j in [0, Rational(1, 2), 1, 2]:
            assert split(j) * splat(j) == 1


class TestTwist:
    def test_scalar(self):
        assert twist(0) == 1

    def test_half_integer(self):
        assert twist(Rational(1, 2)) == -1

    def test_equals_flip_for_su2(self):
        # For SU(2), TWIST = FLIP
        for j in [0, Rational(1, 2), 1, Rational(3, 2), 2]:
            assert twist(j) == flip(j)

    def test_eigenvalue_singlet(self):
        # S_1·S_2 eigenvalue for singlet (S=0): -3/4
        assert twist_eigenvalue(0) == Rational(-3, 4)

    def test_eigenvalue_triplet(self):
        # S_1·S_2 eigenvalue for triplet (S=1): +1/4
        assert twist_eigenvalue(1) == Rational(1, 4)

    def test_hyperfine_splitting(self):
        # Delta_TWIST = 1 (triplet - singlet), Paper 350 x354ab
        assert twist_eigenvalue(1) - twist_eigenvalue(0) == 1


class TestPentagon:
    def test_pentagon_j1(self):
        # Orthogonality sum for j=1: sum_{j12} (2j12+1)|{1 1 j12; 1 1 1}|^2 = 1/3
        passed, lhs, rhs = verify_pentagon(1, 1, 1, 1, 1)
        assert passed, f"Pentagon failed for j=1: lhs={lhs}, rhs={rhs}"

    def test_pentagon_j2(self):
        passed, lhs, rhs = verify_pentagon(2, 1, 2, 1, 2)
        assert passed, f"Pentagon failed for j=2: lhs={lhs}, rhs={rhs}"
