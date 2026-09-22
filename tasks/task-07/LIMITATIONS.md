# Limitations

- The fixture checks a small deterministic SPD suite, not a broad conditioning
  or performance benchmark.
- CSR validation is intentionally lightweight; production code may need checks
  for sorted columns, duplicate entries, and finite values.
- The benchmark does not require preconditioning or support nonsymmetric
  Krylov methods.