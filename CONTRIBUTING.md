# Contributing to NASA POWER S3 Client

Thank you for your interest in contributing to the NASA POWER S3 Client! We welcome contributions from the community to help make this library better.

## Branching Strategy

- **main**: Stable, production-ready code.
- **develop**: Integration branch for new features and fixes. All PRs should target this branch.
- **feature/*** or **fix/***: Feature or bugfix branches created from `develop`.

## Getting Started

1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/nasa-power.git
   cd nasa-power
   ```
3. Install dependencies:
   ```bash
   pip install -e .[dev]
   pre-commit install
   ```

## Testing Requirements

We maintain a high standard for code quality.
- All Pull Requests must include tests covering the new functionality or bug fix.
- We aim for **80% test coverage** minimum.
- Run tests locally before submitting:
  ```bash
  pytest
  ```

## Developer Certificate of Origin (DCO)

To ensure you have the right to submit your code, we require all commits to be signed off. By signing off your contribution, you agree to the DCO (Developer Certificate of Origin).

```text
Signed-off-by: Random J. User <random@developer.example.org>
```

You can do this automatically with git:
```bash
git commit -s -m "Your commit message"
```

## Code Style

We use `black`, `isort`, and `codespell` to maintain code quality. These are configured as pre-commit hooks, so they will run automatically on commit.

If you cannot use pre-commit (e.g., on Windows without admin rights), you can run these tools manually:

```bash
# Format code
black src/
isort src/

# Check spelling
codespell src/ docs/
```

## Reporting Issues

If you find a bug or have a feature request, please open an issue describing the problem or proposal.
