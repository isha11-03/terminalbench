# Known Limitations

- This is a local JSON repository, not a concurrent transactional store.
- The CLI reports domain errors through the normal Python exception path.
- Rollout evidence is represented by the required template/results files only;
  no rollout runs are claimed without execution.
