"""Unit tests for the shared BaseAgent interface."""

import pytest
import numpy as np

from agents.base_agent import BaseAgent
from environment.gridworld import GridWorldEnv
from config import NUM_STATES, NUM_ACTIONS, GAMMA, SEED, RIGHT


class DummyAgent(BaseAgent):
    """Minimal agent used only for interface testing."""

    def __init__(
        self,
        n_states=NUM_STATES,
        n_actions=NUM_ACTIONS,
        gamma=GAMMA,
        seed=SEED,
    ):
        self.n_states = n_states
        self.n_actions = n_actions
        self.gamma = gamma
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.action = RIGHT

    def train(self, env, **kwargs):
        return []

    def select_action(self, state, deterministic=True):
        if deterministic:
            return self.action

        return int(self.rng.integers(self.n_actions))

    def save(self, path):
        np.savez(path, action=self.action)

    def load(self, path):
        with np.load(path, allow_pickle=False) as data:
            self.action = int(data["action"].item())


def test_base_agent_is_abstract():
    with pytest.raises(TypeError):
        BaseAgent()


def test_required_methods():
    assert BaseAgent.__abstractmethods__ == {
        "train",
        "select_action",
        "save",
        "load",
    }


def test_incomplete_agent():
    class IncompleteAgent(BaseAgent):
        pass

    with pytest.raises(TypeError):
        IncompleteAgent()


def test_agent_initialization():
    agent = DummyAgent()

    assert isinstance(agent, BaseAgent)
    assert agent.n_states == NUM_STATES
    assert agent.n_actions == NUM_ACTIONS
    assert agent.gamma == GAMMA
    assert agent.seed == SEED


def test_training_output():
    agent = DummyAgent()
    env = GridWorldEnv()

    logs = agent.train(env, episodes=10)

    assert isinstance(logs, list)

    env.close()


def test_deterministic_action():
    agent = DummyAgent()

    actions = [
        agent.select_action(0, deterministic=True)
        for _ in range(10)
    ]

    assert actions == [RIGHT] * 10


def test_stochastic_action():
    agent = DummyAgent()

    for _ in range(100):
        action = agent.select_action(0, deterministic=False)

        assert isinstance(action, int)
        assert 0 <= action < NUM_ACTIONS


def test_seed_reproducibility():
    agent1 = DummyAgent(seed=42)
    agent2 = DummyAgent(seed=42)

    actions1 = [
        agent1.select_action(0, deterministic=False)
        for _ in range(20)
    ]

    actions2 = [
        agent2.select_action(0, deterministic=False)
        for _ in range(20)
    ]

    assert actions1 == actions2


def test_save_and_load(tmp_path):
    agent = DummyAgent()
    model_path = tmp_path / "dummy_agent.npz"

    agent.save(model_path)

    assert model_path.exists()

    loaded_agent = DummyAgent()
    loaded_agent.action = 0
    loaded_agent.load(model_path)

    assert loaded_agent.select_action(0) == RIGHT


def test_environment_compatibility():
    agent = DummyAgent()
    env = GridWorldEnv(render_mode=None)

    state, _ = env.reset(seed=SEED)

    action = agent.select_action(state)

    assert env.action_space.contains(action)

    next_state, reward, terminated, truncated, info = env.step(action)

    assert env.observation_space.contains(next_state)
    assert isinstance(reward, (int, float))
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)

    env.close()
    