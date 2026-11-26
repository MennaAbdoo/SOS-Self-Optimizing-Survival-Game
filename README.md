# S.O.S. — Self-Optimizing Survival

**Learn. Adapt. Survive.**

## Project Overview

S.O.S. is a custom 2D survival game developed for the Advanced Machine Learning course (AIE322).

The project investigates how different Reinforcement Learning algorithms enable an autonomous robot to navigate a challenging environment, avoid obstacles and hazards, collect batteries, and reach a safe exit.

## Project Objectives

- Design a custom 2D Reinforcement Learning environment.
- Formulate the game as a Markov Decision Process (MDP).
- Implement three Reinforcement Learning algorithms from scratch.
- Train and evaluate all algorithms using a shared environment and reward function.
- Compare algorithm performance through quantitative metrics and visualizations.

## Reinforcement Learning Algorithms

| Category | Algorithm |
|---|---|
| Dynamic Programming | Policy Iteration |
| Temporal Difference Learning | Q-Learning |
| Policy Gradient | REINFORCE |

## Game Design

The proposed game consists of a 7×7 grid containing:

- Autonomous robot agent
- Obstacles and walls
- Collectible batteries
- Hazardous cells
- Safe exit

The agent learns a policy that maximizes its expected cumulative reward.

## Evaluation Metrics

- Average cumulative reward
- Success rate
- Average steps per episode
- Convergence behavior
- Training time
- Performance variability across independent runs

## Technologies

- Python 3.11
- NumPy
- Gymnasium
- Pygame
- Matplotlib
- Pandas
- Pytest
- Git and GitHub
- GitHub Actions

## Repository Structure

```text
SOS-Self-Optimizing-Survival-Game/
├── .github/
├── environment/
├── agents/
├── training/
├── evaluation/
├── experiments/
├── results/
├── assets/
├── tests/
├── docs/
├── config.py
├── main.py
├── requirements.txt
├── pytest.ini
├── CONTRIBUTING.md
├── CONTRIBUTIONS.md
└── README.md
```

## Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Testing

Run the automated test suite:

```bash
python -m pytest -v
```

GitHub Actions is configured to run automated tests on supported pushes and pull requests.

## Team Responsibilities

| Member | Responsibility |
|---|---|
| Student 1 | Environment Design and Visualization |
| Student 2 | MDP and Policy Iteration |
| Student 3 | Q-Learning |
| Student 4 | REINFORCE |
| Student 5 | Training, Evaluation and Integration |

All team members participate in design, implementation, testing, analysis, documentation, and presentation.

## Academic Information

- Course: Advanced Machine Learning
- Course Code: AIE322
- Semester: Fall 2026

## Project Status

Under Development.