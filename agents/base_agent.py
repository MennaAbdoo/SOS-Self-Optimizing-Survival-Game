"""Shared abstract interface for reinforcement learning agents."""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Common interface for Policy Iteration, Q-Learning and REINFORCE."""

    @abstractmethod
    def train(self, env, **kwargs):
        """
        Train the agent using the shared environment.

        Args:
            env: GridWorld environment.
            **kwargs: Algorithm-specific training parameters.

        Returns:
            Training logs following the shared logging schema.
        """
        pass

    @abstractmethod
    def select_action(self, state, deterministic=True):
        """
        Select an action for the given encoded state.

        Args:
            state: Integer state ID.
            deterministic: Whether to use deterministic action selection.

        Returns:
            Integer action ID.
        """
        pass

    @abstractmethod
    def save(self, path):
        """Save learned parameters to the specified path."""
        pass

    @abstractmethod
    def load(self, path):
        """Load learned parameters from the specified path."""
        pass