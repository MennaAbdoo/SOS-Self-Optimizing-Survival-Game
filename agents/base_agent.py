"""Shared interface for all reinforcement learning agents."""

from abc import ABC, abstractmethod


class BaseAgent(ABC):

    @abstractmethod
    def train(self, env, **kwargs):
        """Train the agent and return training logs."""
        pass

    @abstractmethod
    def select_action(self, state, deterministic=True):
        """Return an action ID for the given state."""
        pass

    @abstractmethod
    def save(self, path):
        """Save learned parameters."""
        pass

    @abstractmethod
    def load(self, path):
        """Load learned parameters."""
        pass