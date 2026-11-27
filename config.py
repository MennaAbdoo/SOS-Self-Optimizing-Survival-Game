"""Shared configuration for the S.O.S. project."""
from pathlib import Path

# Environment settings
GRID_SIZE = 7
NUM_BATTERIES = 3
NUM_STATES = GRID_SIZE ** 2 * (2 ** NUM_BATTERIES)
NUM_ACTIONS = 4
MAX_STEPS = 100

# Start and goal positions
START_POSITION = (0, 0)
GOAL_POSITION = (6, 6)

# Action definitions
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

ACTION_DELTAS = {
    LEFT: (0, -1),
    DOWN: (1, 0),
    RIGHT: (0, 1),
    UP: (-1, 0),
}

# Reward settings
GOAL_REWARD = 100
BATTERY_REWARD = 15
HAZARD_PENALTY = -20
COLLISION_PENALTY = -5
STEP_REWARD = -1

# Reinforcement learning settings
GAMMA = 0.9
SEED = 42


# Action names
ACTION_NAMES = {
    LEFT: "LEFT",
    DOWN: "DOWN",
    RIGHT: "RIGHT",
    UP: "UP",
}

# Shared experiment defaults
EXPERIMENT_SEEDS = (42, 43, 44, 45, 46)
TRAIN_EPISODES = 5000
VALIDATION_EPISODES = 50
EVALUATION_EPISODES = 100

# Policy Iteration defaults
PI_THETA = 1e-8

# Q-Learning defaults
Q_LEARNING_RATE = 0.1
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995

# REINFORCE defaults
REINFORCE_LEARNING_RATE = 0.01

# Result directories
PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"

MODELS_DIR = RESULTS_DIR / "models"
TRAINING_LOGS_DIR = RESULTS_DIR / "training_logs"
EVALUATION_LOGS_DIR = RESULTS_DIR / "evaluation_logs"
METRICS_DIR = RESULTS_DIR / "metrics"
FIGURES_DIR = RESULTS_DIR / "figures"