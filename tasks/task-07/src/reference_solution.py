"""Reference implementation for TASK-07."""
import json
import math


class SparseMatrix:
    def __init__(self, row_ptr, col_idx, values, shape):
        self.row_ptr = list(row_ptr)
        self.col_idx = list(col_idx)
        self.values = list(values)
        self.shape = tuple(shape)
        if len(self.row_ptr) != self.shape[0] + 1:
            raise ValueError("invalid CSR row_ptr")

    def to_dense(self):
        rows, cols = self.shape
        dense = [[0.0] * cols for _ in range(rows)]
        for row in range(rows):
            for pos in range(self.row_ptr[row], self.row_ptr[row + 1]):
                dense[row][self.col_idx[pos]] = self.values[pos]
        return dense

    def matvec(self, vector):
        rows, cols = self.shape
        if len(vector) != cols:
            raise ValueError("incompatible vector dimension")
        result = []
        for row in range(rows):
            total = 0.0
            for pos in range(self.row_ptr[row], self.row_ptr[row + 1]):
                total += self.values[pos] * vector[self.col_idx[pos]]
            result.append(total)
        return result


def load_matrix(path):
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    return SparseMatrix(payload["row_ptr"], payload["col_idx"],
                        payload["values"], payload["shape"])


def solve_cg(matrix, b, tol=1e-8, max_iter=None, x0=None):
    rows, cols = matrix.shape
    if rows != cols or len(b) != rows:
        raise ValueError("incompatible dimensions")
    if tol <= 0 or not math.isfinite(tol):
        raise ValueError("tol must be positive and finite")
    limit = rows if max_iter is None else max_iter
    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("max_iter must be a positive integer")
    if x0 is None:
        x = [0.0] * rows
    else:
        if len(x0) != rows:
            raise ValueError("incompatible initial guess")
        x = [float(value) for value in x0]
    b = [float(value) for value in b]
    norm_b = math.sqrt(math.fsum(value * value for value in b))
    residual = [rhs - value for rhs, value in zip(b, matrix.matvec(x))]
    residual_norm = math.sqrt(math.fsum(value * value for value in residual))
    threshold = tol * max(1.0, norm_b)
    if residual_norm <= threshold:
        return {"x": x, "iterations": 0, "residual_norm": residual_norm, "converged": True}
    direction = list(residual)
    residual_sq = math.fsum(value * value for value in residual)
    for iteration in range(1, limit + 1):
        product = matrix.matvec(direction)
        denominator = math.fsum(a * c for a, c in zip(direction, product))
        if denominator <= 0 or not math.isfinite(denominator):
            return {"x": x, "iterations": iteration - 1,
                    "residual_norm": residual_norm, "converged": False}
        step = residual_sq / denominator
        x = [a + step * c for a, c in zip(x, direction)]
        residual = [a - step * c for a, c in zip(residual, product)]
        new_sq = math.fsum(value * value for value in residual)
        residual_norm = math.sqrt(new_sq)
        if residual_norm <= threshold:
            return {"x": x, "iterations": iteration,
                    "residual_norm": residual_norm, "converged": True}
        direction = [a + new_sq / residual_sq * c for a, c in zip(residual, direction)]
        residual_sq = new_sq
    return {"x": x, "iterations": limit,
            "residual_norm": residual_norm, "converged": False}