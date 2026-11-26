# Contribution Guidelines

## Branching Strategy

- `main`: Stable project versions.
- `develop`: Integration and development branch.
- `feature/environment`: Environment and visualization.
- `feature/policy-iteration`: MDP and Policy Iteration.
- `feature/q-learning`: Q-Learning implementation.
- `feature/reinforce`: REINFORCE implementation.
- `feature/evaluation`: Training, evaluation, and integration.

## Development Workflow

1. Select an assigned GitHub Issue.
2. Switch to your assigned feature branch.
3. Synchronize your branch with `develop`.
4. Implement the assigned task.
5. Write or update relevant tests.
6. Run the automated test suite.
7. Commit your changes with a descriptive message.
8. Push your feature branch.
9. Open a Pull Request targeting `develop`.
10. Request a review from the assigned reviewer.
11. Resolve review comments before merging.
12. Update `CONTRIBUTIONS.md`.

## Coding Guidelines

- Follow consistent Python naming conventions.
- Write readable and modular code.
- Document important functions and classes.
- Follow the agreed shared interfaces.
- Avoid modifying unrelated files.
- Implement the required RL algorithms from scratch.
- Use shared environment settings for fair comparison.

## Testing Guidelines

Run all tests before submitting a Pull Request:

```bash
python -m pytest -v
```

Every implemented feature should include relevant tests.

## Commit Message Convention

Examples:

- `feat: implement gridworld movement`
- `fix: correct terminal state handling`
- `test: add Q-learning update tests`
- `docs: update environment design`
- `refactor: improve state encoding`

## Pull Request Rules

- Do not push directly to `main` or `develop` after initial setup.
- Every feature must be reviewed before merging.
- Automated tests must pass.
- Changes must be related to the assigned task.
- Shared interface changes must be discussed with the team.

## Contribution Tracking

Every member must document their design, implementation, testing, analysis, and documentation contributions in `CONTRIBUTIONS.md`.