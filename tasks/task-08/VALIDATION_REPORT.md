# Validation Report

## Local validation

- `bash run-tests.sh`: 10 passed.
- `bash solution.sh`: 10 passed.
- `docker compose build --no-cache && docker compose run --rm task bash run-tests.sh`: 10 passed.
- TASK-08 prompt: 228 words, under the 600-word limit.

## Fresh-container validation

The Dockerfile installs pytest and copies the complete task. The fresh build
and container test completed successfully. The repository-wide structure script
currently fails on pre-existing TASK-02 and TASK-03 prompts over 600 words;
TASK-08 itself satisfies the limit and no unrelated task files were changed.
