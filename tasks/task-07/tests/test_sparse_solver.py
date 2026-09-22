import json
import math
import pytest

from sparse_solver import SparseMatrix, load_matrix, solve_cg


DATA = json.load(open("data/cases.json", encoding="utf-8"))


def matrix(case):
    return SparseMatrix(case["row_ptr"], case["col_idx"], case["values"], case["shape"])


@pytest.mark.parametrize("case", DATA.values())
def test_solution_and_residual(case):
    result = solve_cg(matrix(case), case["b"], tol=1e-10)
    assert result["converged"] is True
    assert result["iterations"] <= case["shape"][0]
    assert result["x"] == pytest.approx(case["expected_x"], rel=1e-8, abs=1e-8)
    residual = [a - b for a, b in zip(case["b"], matrix(case).matvec(result["x"]))]
    assert math.hypot(*residual) <= 1e-10 * max(1, math.hypot(*case["b"]))


def test_sparse_matvec_does_not_call_dense_conversion():
    sparse = matrix(DATA["tridiagonal"])
    sparse.to_dense = lambda: (_ for _ in ()).throw(AssertionError("dense conversion"))
    assert sparse.matvec([1, 1, 1, 1, 1]) == pytest.approx([3, 2, 2, 2, 3])


def test_solver_does_not_call_dense_conversion():
    sparse = matrix(DATA["tridiagonal"])
    sparse.to_dense = lambda: (_ for _ in ()).throw(AssertionError("dense conversion"))
    result = solve_cg(sparse, DATA["tridiagonal"]["b"])
    assert result["converged"] is True


def test_relative_tolerance_and_initial_guess():
    case = DATA["scaled"]
    result = solve_cg(matrix(case), case["b"], tol=1e-6, max_iter=1, x0=[1, 1, 2])
    assert result["iterations"] == 0
    assert result["converged"] is True
    assert result["x"] == [1.0, 1.0, 2.0]


def test_zero_rhs_and_budget_reporting():
    sparse = matrix(DATA["tridiagonal"])
    zero = solve_cg(sparse, [0, 0, 0, 0, 0])
    assert zero == {"x": [0.0] * 5, "iterations": 0,
                    "residual_norm": 0.0, "converged": True}
    limited = solve_cg(sparse, DATA["tridiagonal"]["b"], max_iter=1)
    assert limited["iterations"] == 1
    assert limited["converged"] is False


@pytest.mark.parametrize("kwargs", [{"tol": 0}, {"tol": float("nan")}, {"max_iter": 0}, {"max_iter": 1.5}])
def test_invalid_controls(kwargs):
    with pytest.raises(ValueError):
        solve_cg(matrix(DATA["tridiagonal"]), DATA["tridiagonal"]["b"], **kwargs)


def test_invalid_dimensions_and_loader():
    with pytest.raises(ValueError):
        solve_cg(SparseMatrix([0], [], [], (1, 2)), [1])
    with pytest.raises(ValueError):
        solve_cg(matrix(DATA["tridiagonal"]), [1, 2, 3, 4])
    with pytest.raises(ValueError):
        solve_cg(matrix(DATA["tridiagonal"]), DATA["tridiagonal"]["b"], x0=[0, 0])
    loaded = load_matrix("data/tridiagonal.json")
    assert loaded.shape == (5, 5)
    assert loaded.matvec([1, 1, 1, 1, 1]) == pytest.approx([3, 2, 2, 2, 3])


def test_deterministic_result():
    case = DATA["tridiagonal"]
    first = solve_cg(matrix(case), case["b"], tol=1e-12)
    second = solve_cg(matrix(case), case["b"], tol=1e-12)
    assert first == second