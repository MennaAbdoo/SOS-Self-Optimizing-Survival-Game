"""Unit tests for the shared GridWorld environment."""

import pytest

from config import (
    NUM_STATES, NUM_ACTIONS, MAX_STEPS,
    GRID_SIZE, START_POSITION, GOAL_POSITION,
    LEFT, DOWN, RIGHT, UP,
    STEP_REWARD, COLLISION_PENALTY,
    BATTERY_REWARD, HAZARD_PENALTY, GOAL_REWARD,
)

from environment.gridworld import GridWorldEnv, transition
from environment.state_encoder import encode_state
from environment.maps import (
    WALLS, BATTERIES, validate_map,
    get_reachable_positions,
)


@pytest.fixture
def env():
    environment = GridWorldEnv(render_mode=None)
    environment.reset(seed=42)
    yield environment
    environment.close()


def test_initialization(env):
    assert env.observation_space.n == NUM_STATES
    assert env.action_space.n == NUM_ACTIONS


def test_reset(env):
    env.step(DOWN)
    env.step(DOWN)

    state, info = env.reset(seed=42)

    assert state == 0
    assert info["position"] == START_POSITION
    assert info["battery_mask"] == 0
    assert info["batteries_collected"] == 0
    assert info["step_count"] == 0
    assert info["cumulative_reward"] == 0
    assert info["hazard_encounters"] == 0
    assert not info["success"]


@pytest.mark.parametrize(
    "action, expected_position",
    [
        (LEFT, (2, 3)),
        (DOWN, (3, 3)),
        (RIGHT, (2, 5)),
        (UP, (1, 4)),
    ],
)
def test_movement(env, action, expected_position):
    env.state = encode_state(2, 4, 0)

    _, reward, terminated, truncated, info = env.step(action)

    # DOWN hits a wall at (3, 4).
    if action == DOWN:
        assert info["position"] == (2, 4)
        assert reward == COLLISION_PENALTY
    else:
        assert info["position"] == expected_position
        assert reward == STEP_REWARD

    assert not terminated
    assert not truncated


def test_normal_movement(env):
    state, reward, terminated, truncated, info = env.step(RIGHT)

    assert state == encode_state(0, 1, 0)
    assert reward == STEP_REWARD
    assert not terminated
    assert not truncated


def test_wall_collision(env):
    env.step(RIGHT)

    state, reward, _, _, info = env.step(DOWN)

    assert state == encode_state(0, 1, 0)
    assert reward == COLLISION_PENALTY
    assert info["position"] == (0, 1)


@pytest.mark.parametrize("action", [LEFT, UP])
def test_boundary_collision(env, action):
    state, reward, _, _, info = env.step(action)

    assert state == 0
    assert reward == COLLISION_PENALTY
    assert info["position"] == START_POSITION


def test_battery_collection(env):
    env.step(DOWN)

    state, reward, _, _, info = env.step(DOWN)

    assert state == encode_state(2, 0, 2)
    assert reward == BATTERY_REWARD
    assert info["battery_mask"] == 2
    assert info["batteries_collected"] == 1


def test_repeated_battery_visit(env):
    env.step(DOWN)
    env.step(DOWN)
    env.step(UP)

    _, reward, _, _, info = env.step(DOWN)

    assert reward == STEP_REWARD
    assert info["batteries_collected"] == 1


def test_hazard_penalty(env):
    env.state = encode_state(1, 2, 0)

    _, reward, terminated, truncated, info = env.step(RIGHT)

    assert reward == HAZARD_PENALTY
    assert info["hazard_encounters"] == 1
    assert not terminated
    assert not truncated


def test_goal_termination(env):
    env.state = encode_state(5, 6, 0)

    _, reward, terminated, truncated, info = env.step(DOWN)

    assert reward == GOAL_REWARD
    assert terminated
    assert not truncated
    assert info["success"]
    assert info["position"] == GOAL_POSITION


def test_episode_truncation(env):
    for _ in range(MAX_STEPS):
        _, _, terminated, truncated, info = env.step(UP)

    assert not terminated
    assert truncated
    assert info["step_count"] == MAX_STEPS
    assert not info["success"]


def test_goal_priority_at_time_limit(env):
    env.state = encode_state(5, 6, 0)
    env.step_count = MAX_STEPS - 1

    _, reward, terminated, truncated, _ = env.step(DOWN)

    assert reward == GOAL_REWARD
    assert terminated
    assert not truncated


def test_episode_statistics(env):
    env.step(DOWN)
    env.step(DOWN)
    env.step(UP)

    _, _, _, _, info = env.step(DOWN)

    assert info["step_count"] == 4
    assert info["cumulative_reward"] == 12
    assert info["batteries_collected"] == 1


def test_map_reachability():
    assert validate_map()

    reachable = get_reachable_positions()

    assert GOAL_POSITION in reachable
    assert set(BATTERIES).issubset(reachable)
    assert len(reachable) == GRID_SIZE ** 2 - len(WALLS)


@pytest.mark.parametrize("action", [LEFT, DOWN, RIGHT, UP])
def test_transition_consistency(env, action):
    expected = transition(env.state, action)

    state, reward, terminated, _, _ = env.step(action)

    assert (state, reward, terminated) == expected


def test_terminal_state_is_absorbing():
    state = encode_state(*GOAL_POSITION, 0)

    assert transition(state, RIGHT) == (state, 0, True)


def test_invalid_action(env):
    with pytest.raises(ValueError):
        env.step(NUM_ACTIONS)


def test_step_after_episode_end(env):
    env.state = encode_state(5, 6, 0)
    env.step(DOWN)

    with pytest.raises(RuntimeError):
        env.step(RIGHT)


def test_step_before_reset():
    environment = GridWorldEnv()

    with pytest.raises(RuntimeError):
        environment.step(RIGHT)

    environment.close()


def test_down_movement(env):
    _, reward, _, _, info = env.step(DOWN)

    assert info["position"] == (1, 0)
    assert reward == STEP_REWARD

def test_goal_is_not_expanded_in_reachability():
    from environment.maps import get_reachable_positions
    from config import GOAL_POSITION

    assert get_reachable_positions(GOAL_POSITION) == {
        GOAL_POSITION
    }


def test_all_walkable_cells_remain_reachable():
    from environment.maps import get_reachable_positions, WALLS
    from config import GRID_SIZE

    reachable = get_reachable_positions()

    assert len(reachable) == GRID_SIZE ** 2 - len(WALLS)

def test_default_visualization_settings():
    from config import DEFAULT_RENDER_FPS

    env = GridWorldEnv()

    assert env.render_mode is None
    assert env.algorithm_name == "Demo"
    assert env.render_fps == DEFAULT_RENDER_FPS

    env.close()


def test_custom_visualization_settings():
    env = GridWorldEnv(
        render_mode="human",
        algorithm_name="Q-Learning",
        render_fps=10,
    )

    assert env.algorithm_name == "Q-Learning"
    assert env.render_fps == 10

    env.close()


def test_headless_render():
    env = GridWorldEnv(render_mode=None)
    env.reset()

    assert env.render() is True
    assert env._renderer is None

    env.close()


def test_invalid_render_fps():
    with pytest.raises(ValueError):
        GridWorldEnv(render_fps=0)

def test_complete_successful_episode():
    from config import DOWN, RIGHT
    from environment.gridworld import GridWorldEnv

    env = GridWorldEnv()
    env.reset(seed=42)

    actions = [
        DOWN, DOWN, RIGHT, DOWN,
        DOWN, RIGHT, RIGHT, DOWN,
        RIGHT, RIGHT, RIGHT, DOWN
    ]

    total_reward = 0

    for action in actions:
        state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

    assert terminated is True
    assert truncated is False
    assert total_reward == 121
    assert info["step_count"] == 12
    assert info["batteries_collected"] == 2
    assert info["hazard_encounters"] == 0
    assert info["position"] == (6, 6)
    assert info["success"] is True

    env.close()


def test_reachable_encoded_states():
    from collections import deque
    from config import NUM_ACTIONS, START_POSITION, GOAL_POSITION
    from environment.gridworld import transition
    from environment.state_encoder import encode_state, decode_state

    initial_state = encode_state(*START_POSITION, 0)

    visited = {initial_state}
    queue = deque([initial_state])

    while queue:
        state = queue.popleft()

        row, col, _ = decode_state(state)

        if (row, col) == GOAL_POSITION:
            continue

        for action in range(NUM_ACTIONS):
            next_state, _, _ = transition(state, action)

            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)

    terminal_states = {
        state for state in visited
        if decode_state(state)[:2] == GOAL_POSITION
    }

    assert len(visited) == 312
    assert len(terminal_states) == 8
    assert len(visited - terminal_states) == 304