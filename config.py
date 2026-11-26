"""Shared configuration for the S.O.S. project."""

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