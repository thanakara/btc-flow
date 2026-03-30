# Composite Action vs Reusable Workflow

## Reusable Workflow

Reuses an entire **job** on its own runner.

```yaml
# .github/workflows/setup.yaml
on:
    workflow_call:

jobs:
    setup:
        runs-on: ubuntu-latest
        steps:
            - run: uv sync --frozen
```

```yaml
# .github/workflows/ci.yaml
jobs:
    setup:
        uses: ./.github/workflows/setup.yaml  # separate runner

    lint:
        needs: setup  # fresh runner — setup's .venv is GONE ❌
```

- Runs on its **own isolated runner**
- Fresh filesystem — nothing carries over to the calling job
- Good for: sharing entire job sequences (e.g. a full deploy job)

---

## Composite Action

Reuses **steps** within a job.

```yaml
# .github/actions/setup-python/action.yaml
runs:
    using: composite
    steps:
        - uses: actions/checkout@...
        - uses: astral-sh/setup-uv@...
        - uses: actions/cache@...
        - run: uv sync --frozen
          shell: bash
```

```yaml
# .github/workflows/ci.yaml
jobs:
    lint:
        runs-on: ubuntu-latest
        steps:
            - uses: ./.github/actions/setup-python  # same runner
            - run: uv run ruff check .              # .venv available ✅
```

- Runs on the **same runner** as the calling job
- Shared filesystem — `.venv` is available to subsequent steps
- Good for: sharing setup steps (checkout, install, cache)

---

## Summary

| | Composite Action | Reusable Workflow |
|---|---|---|
| Reuses | Steps | Jobs |
| Runner | Same as caller | Own isolated runner |
| Filesystem | Shared | Fresh |
| `.venv` persists | ✅ Yes | ❌ No |
| Good for | Setup steps | Full job sequences |

> For caching `.venv` across steps in the same job — always use a **composite action**.
> `actions/cache` does persist across jobs via GitHub's remote cache store, but each job
> still needs to explicitly restore it on its own fresh runner.
