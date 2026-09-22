# Limitations

- Inputs are required to be finite Python real numbers; infinities are rejected
  rather than assigned a special probability convention.
- This is a single-vector API, not a batched tensor implementation.
- Accuracy is bounded by IEEE-754 double precision and the quality of the
  platform `math` implementation.
- The Dockerfile uses the configured package index to install pytest during
  image build; runtime execution itself needs no network.