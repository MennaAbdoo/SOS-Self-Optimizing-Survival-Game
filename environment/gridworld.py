"""Core GridWorld environment and deterministic transition logic."""

from numbers import Integral

import gymnasium as gym
from gymnasium import spaces

from config import (
    NUM_STATES,
    NUM_ACTIONS,
    MAX_STEPS,
    START_POSITION,
    GOAL_POSITION,
    ACTION_DELTAS,
    GOAL_REWARD,
    BATTERY_REWARD,
    HAZARD_PENALTY,
    COLLISION_PENALTY,
    STEP_REWARD,
)

from environment.maps import BATTERIES, HAZARDS, is_walkable
from environment.state_encoder import encode_state, decode_state


def transition(state, action):
    """Return next state, reward, and termination without side effects."""

    if not isinstance(action, Integral) or action not in ACTION_DELTAS:
        raise ValueError("Invalid action.")

    row, col, battery_mask = decode_state(state)

    if not is_walkable((row, col)):
        raise ValueError("Invalid state position.")

    # Terminal states are absorbing
    if (row, col) == GOAL_POSITION:
        return int(state), 0, True

    dr, dc = ACTION_DELTAS[action]
    next_position = (row + dr, col + dc)

    # Wall or boundary collision
    if not is_walkable(next_position):
        return int(state), COLLISION_PENALTY, False

    next_row, next_col = next_position
    terminated = False

    # Goal
    if next_position == GOAL_POSITION:
        reward = GOAL_REWARD
        terminated = True

    # Uncollected battery
    elif (
        next_position in BATTERIES
        and not (battery_mask & BATTERIES[next_position])
    ):
        battery_mask |= BATTERIES[next_position]
        reward = BATTERY_REWARD

    # Hazard
    elif next_position in HAZARDS:
        reward = HAZARD_PENALTY

    # Normal movement or previously collected battery
    else:
        reward = STEP_REWARD

    next_state = encode_state(
        next_row, next_col, battery_mask
    )

    return next_state, reward, terminated


class GridWorldEnv(gym.Env):
    """S.O.S. robot survival environment."""

    metadata = {"render_modes": ["human"], "render_fps": 5}

    def __init__(self, render_mode=None):
        super().__init__()

        if render_mode not in (None, "human"):
            raise ValueError("Unsupported render mode.")

        self.observation_space = spaces.Discrete(NUM_STATES)
        self.action_space = spaces.Discrete(NUM_ACTIONS)

        self.render_mode = render_mode
        self._renderer = None

        self.state = encode_state(*START_POSITION, 0)
        self.step_count = 0
        self.cumulative_reward = 0
        self.hazard_encounters = 0
        self.terminated = False
        self.truncated = False
        self._has_reset = False

    def reset(self, *, seed=None, options=None):
        """Start a new episode."""

        super().reset(seed=seed)

        self.state = encode_state(*START_POSITION, 0)
        self.step_count = 0
        self.cumulative_reward = 0
        self.hazard_encounters = 0
        self.terminated = False
        self.truncated = False
        self._has_reset = True

        return self.state, self._get_info()

    def step(self, action):
        """Execute one action."""

        if not self._has_reset:
            raise RuntimeError("Reset the environment first.")

        if self.terminated or self.truncated:
            raise RuntimeError("Episode finished. Call reset().")

        next_state, reward, terminated = transition(
            self.state, action
        )

        self.state = next_state
        self.step_count += 1
        self.cumulative_reward += reward
        self.terminated = terminated

        if reward == HAZARD_PENALTY:
            self.hazard_encounters += 1

        self.truncated = (
            self.step_count >= MAX_STEPS
            and not self.terminated
        )

        return (
            self.state,
            reward,
            self.terminated,
            self.truncated,
            self._get_info(),
        )

    def _get_info(self):
        """Return additional episode information."""

        row, col, battery_mask = decode_state(self.state)

        return {
            "position": (row, col),
            "battery_mask": battery_mask,
            "batteries_collected": battery_mask.bit_count(),
            "step_count": self.step_count,
            "cumulative_reward": self.cumulative_reward,
            "hazard_encounters": self.hazard_encounters,
            "success": self.terminated,
        }

    def render(self):
        """Render the environment."""

        if self.render_mode is None:
            return

        from environment.visualization import GridWorldRenderer

        if self._renderer is None:
            self._renderer = GridWorldRenderer()

        self._renderer.render(self)

    def close(self):
        """Release visualization resources."""

        if self._renderer is not None:
            self._renderer.close()
            self._renderer = None