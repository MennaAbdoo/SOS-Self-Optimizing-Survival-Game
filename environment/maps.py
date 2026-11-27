"""Fixed GridWorld map definition."""

from config import GRID_SIZE, START_POSITION, GOAL_POSITION
from collections import deque
from config import ACTION_DELTAS, NUM_BATTERIES

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

def get_reachable_positions(start=START_POSITION):
    """Find all reachable positions using BFS."""

    if not is_walkable(start):
        raise ValueError("Invalid starting position.")

    visited = {start}
    queue = deque([start])

    while queue:
        row, col = queue.popleft()

        for dr, dc in ACTION_DELTAS.values():
            next_position = (row + dr, col + dc)

            if is_walkable(next_position) and next_position not in visited:
                visited.add(next_position)
                queue.append(next_position)

    return visited


def validate_map():
    """Validate map layout and reachability."""

    groups = [
        {START_POSITION},
        {GOAL_POSITION},
        set(WALLS),
        set(HAZARDS),
        set(BATTERIES),
    ]

    # Check boundaries
    for group in groups:
        for position in group:
            if not is_inside_grid(position):
                raise ValueError(f"Invalid position: {position}")

    # Check overlapping elements
    occupied = set()

    for group in groups:
        if occupied.intersection(group):
            raise ValueError("Map elements overlap.")

        occupied.update(group)

    # Check battery count and masks
    if len(BATTERIES) != NUM_BATTERIES:
        raise ValueError("Invalid number of batteries.")

    expected_masks = {1 << i for i in range(NUM_BATTERIES)}

    if set(BATTERIES.values()) != expected_masks:
        raise ValueError("Invalid battery masks.")

    # Check reachability
    reachable = get_reachable_positions()

    if GOAL_POSITION not in reachable:
        raise ValueError("Goal is unreachable.")

    if not set(BATTERIES).issubset(reachable):
        raise ValueError("Some batteries are unreachable.")

    return True