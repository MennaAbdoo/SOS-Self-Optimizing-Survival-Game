# Contributing to S.O.S.

## 1. Branching Strategy

The project uses a personal branch workflow. Each team member works on their assigned branch and submits changes to `main` through Pull Requests.

| Team Member | Assigned Branch |
|---|---|
| Menna Abdo | `menna-abdo` |
| Maryam | `maryam` |
| Mennatullah | `mennatullah` |
| Menna Osama | `menna-osama` |
| Catherine | `catherine` |

The `main` branch represents the stable and integrated version of the project.

## 2. Development Workflow

Before starting a task, switch to your assigned branch and synchronize it with the latest version of `main`.

```bash
git switch YOUR-BRANCH
git pull origin YOUR-BRANCH
git fetch origin
git merge origin/main
```

Implement your assigned task and add the necessary tests.

Run all tests locally:

```bash
python -m pytest -v
```

Stage, commit, and push your changes:

```bash
git add <changed-files>
git commit -m "Describe the implemented task"
git push origin YOUR-BRANCH
```

## 3. Pull Request Requirements

Create a Pull Request with:

- Base branch: `main`
- Compare branch: your personal branch
- A clear description of the implemented changes
- Related issue number
- Testing results
- Documentation updates, if applicable

## 4. Testing and Code Review

Before merging a Pull Request:

- All automated GitHub Actions tests must pass.
- At least one other team member must approve the changes.
- All merge conflicts must be resolved.
- All review comments must be addressed.
- The contribution log must be updated.

If any check fails, fix the issue on your personal branch and push the updated changes.

## 5. Merge Policy

- Direct pushes to `main` are not allowed during team development.
- Changes must be integrated through approved Pull Requests.
- Personal branches must not be deleted after merging.
- Use merge commits to preserve contribution history.
- Synchronize your personal branch with `main` after merging.

## 6. Code Quality

- Write clean, readable, and modular Python code.
- Follow the agreed project interfaces.
- Add meaningful comments and docstrings.
- Implement unit tests for new functionality.
- Do not modify unrelated files.
- Do not commit virtual environments, caches, or sensitive information.

## 7. Team Responsibilities

Every team member must participate in design, implementation, testing, analysis, documentation, and the final presentation.

Record all contributions in `CONTRIBUTIONS.md`.