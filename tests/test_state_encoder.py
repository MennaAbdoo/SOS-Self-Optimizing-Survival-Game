"""Unit tests for state encoding and decoding."""

import pytest

from config import GRID_SIZE, NUM_STATES, NUM_BATTERIES
from environment.state_encoder import encode_state, decode_state


def test_state_space_size():
    assert NUM_STATES == GRID_SIZE ** 2 * 2 ** NUM_BATTERIES
    assert NUM_STATES == 392


def test_initial_state():
    assert encode_state(0, 0, 0) == 0


def test_maximum_state_id():
    assert encode_state(6, 6, 7) == 391


def test_encoding():
    assert encode_state(2, 0, 2) == 114


def test_decoding():
    assert decode_state(114) == (2, 0, 2)


def test_all_states_round_trip():
    for state_id in range(NUM_STATES):
        components = decode_state(state_id)
        assert encode_state(*components) == state_id


def test_unique_state_ids():
    state_ids = {
        encode_state(row, col, mask)
        for row in range(GRID_SIZE)
        for col in range(GRID_SIZE)
        for mask in range(2 ** NUM_BATTERIES)
    }

    assert len(state_ids) == NUM_STATES
    assert state_ids == set(range(NUM_STATES))


@pytest.mark.parametrize("mask", range(8))
def test_battery_masks(mask):
    state_id = encode_state(2, 0, mask)

    assert decode_state(state_id) == (2, 0, mask)


@pytest.mark.parametrize(
    "row, col",
    [
        (-1, 0),
        (0, -1),
        (7, 0),
        (0, 7),
    ],
)
def test_invalid_coordinates(row, col):
    with pytest.raises(ValueError):
        encode_state(row, col, 0)


@pytest.mark.parametrize("mask", [-1, 8, 1.5])
def test_invalid_battery_mask(mask):
    with pytest.raises(ValueError):
        encode_state(0, 0, mask)


@pytest.mark.parametrize("state_id", [-1, 392, 1.5, "114"])
def test_invalid_state_id(state_id):
    with pytest.raises(ValueError):
        decode_state(state_id)


@pytest.mark.parametrize(
    "row, col, mask",
    [
        (1.5, 0, 0),
        (0, "1", 0),
        (0, 0, "2"),
    ],
)
def test_invalid_component_types(row, col, mask):
    with pytest.raises(ValueError):
        encode_state(row, col, mask)