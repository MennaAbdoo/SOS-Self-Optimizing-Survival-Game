"""State encoding and decoding utilities."""

from numbers import Integral
from config import GRID_SIZE, NUM_BATTERIES, NUM_STATES

NUM_MASKS = 2 ** NUM_BATTERIES


def encode_state(row, col, battery_mask):
    """Convert a state into a unique integer ID."""

    if not all(isinstance(x, Integral) for x in
               (row, col, battery_mask)):
        raise ValueError("State components must be integers.")

    if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
        raise ValueError("Invalid grid position.")

    if not 0 <= battery_mask < NUM_MASKS:
        raise ValueError("Invalid battery mask.")

    return int((row * GRID_SIZE + col) * NUM_MASKS + battery_mask)


def decode_state(state_id):
    """Convert an integer ID into its state components."""

    if not isinstance(state_id, Integral):
        raise ValueError("State ID must be an integer.")

    if not 0 <= state_id < NUM_STATES:
        raise ValueError("Invalid state ID.")

    position_index, battery_mask = divmod(int(state_id), NUM_MASKS)
    row, col = divmod(position_index, GRID_SIZE)

    return row, col, battery_mask