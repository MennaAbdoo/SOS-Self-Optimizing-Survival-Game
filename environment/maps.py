"""Fixed GridWorld map definition."""

from config import GRID_SIZE, START_POSITION, GOAL_POSITION

WALLS = frozenset({
    (0, 3),
    (1, 1),
    (1, 5),
    (2, 2),
    (3, 4),
    (4, 0),
    (5, 2),
    (6, 4),
})

HAZARDS = frozenset({
    (1, 3),
    (3, 2),
    (4, 4),
    (6, 0),
})

# Battery positions and their corresponding bit masks
BATTERIES = {
    (0, 6): 0b100,
    (2, 0): 0b010,
    (5, 5): 0b001,
}


def is_inside_grid(position):
    """Check whether a position is inside the grid."""
    row, col = position
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE


def is_walkable(position):
    """Check whether the robot can enter a position."""
    return is_inside_grid(position) and position not in WALLS