# S.O.S. — Shared Interfaces

## 1. Environment Interface

**File:** `environment/gridworld.py`

| Method | Return Value |
|---|---|
| `reset(seed=None)` | `state, info` |
| `step(action)` | `next_state, reward, terminated, truncated, info` |
| `render()` | Environment visualization |
| `close()` | Release resources |

- States are encoded integers (0–391).
- Actions are integers (0–3).
- `done = terminated or truncated`.
- The environment must be reset after episode completion.

## 2. State Encoder

**File:** `environment/state_encoder.py`

| Function | Output |
|---|---|
| `encode_state(row, col, battery_mask)` | Integer state ID |
| `decode_state(state_id)` | `(row, col, battery_mask)` |

Encoding:

`state_id = (row * 7 + col) * 8 + battery_mask`

## 3. Shared Transition Function

**File:** `environment/gridworld.py`

`transition(state, action)`

Returns:

`next_state, reward, terminated`

This function must be deterministic and must not modify the current environment instance.

Both the interactive environment and the MDP model must use this function.

## 4. MDP Interface

**File:** `environment/mdp.py`

`build_mdp()`

Returns the transition model:

`P[state][action] = [(probability, next_state, reward, terminated)]`

- All valid transitions have probability 1.
- Goal states are absorbing with zero subsequent reward.
- Invalid wall states must be excluded from planning.
- The episode time limit is handled separately.

## 5. Agent Interface

**File:** `agents/base_agent.py`

All agents must implement the following methods:

| Method | Purpose |
|---|---|
| `train(env, **kwargs)` | Train the agent and return training logs |
| `select_action(state, deterministic=True)` | Return an action ID |
| `save(path)` | Save learned parameters |
| `load(path)` | Load learned parameters |

Policy Iteration, Q-Learning, and REINFORCE must follow this interface.

## 6. Shared Configuration

**File:** `config.py`

| Parameter | Value |
|---|---:|
| GRID_SIZE | 7 |
| NUM_STATES | 392 |
| NUM_ACTIONS | 4 |
| MAX_STEPS | 100 |
| GAMMA | 0.9 |

Map coordinates and reward values must remain consistent with `environment_design.md`.

## 7. Training Logs

Each algorithm must provide the following fields:

- `algorithm`
- `run_id`
- `seed`
- `progress_unit`
- `progress_index`
- `episode_reward`
- `episode_steps`
- `success`
- `convergence_delta`
- `training_time_seconds`

Use `iteration` for Policy Iteration and `episode` for Q-Learning and REINFORCE.

Non-applicable fields may be null.

## 8. Evaluation Logs

Each evaluation episode must record:

- `algorithm`
- `run_id`
- `seed`
- `episode`
- `total_reward`
- `steps`
- `success`
- `batteries_collected`
- `hazard_encounters`
- `terminated`
- `truncated`

## 9. Integration Rules

- All algorithms must use the shared environment and configuration.
- Evaluation must not update learned parameters.
- True terminal transitions must not bootstrap future values.
- Truncation must be distinguished from termination.
- Rendering must be disabled during training and automated testing.
- Interface changes require team agreement.

## GridWorld Implementation Details

**Environment class:** `GridWorldEnv`

**Import:**

```python
from environment.gridworld import GridWorldEnv
```

**Initialization:**

```python
env = GridWorldEnv(render_mode=None)
```

### Environment Info Dictionary

| Key | Description |
|---|---|
| `position` | Current robot position (row, col) |
| `battery_mask` | Integer representing collected batteries |
| `batteries_collected` | Number of collected batteries |
| `step_count` | Number of attempted actions |
| `cumulative_reward` | Total episode reward |
| `hazard_encounters` | Number of hazard entries |
| `success` | Whether the robot reached the goal |

### Implementation Rules

- Call `reset()` before starting an episode.
- Reset the environment after termination or truncation.
- Use the shared `transition(state, action)` function for MDP construction.
- Goal states are absorbing with zero subsequent reward.
- Wall states are excluded from valid transitions.
- Use `render_mode=None` during training and evaluation.
- Use `render_mode="human"` for visualization.

## Agent Initialization Contract

- All reinforcement learning agents must inherit from `BaseAgent`.
- Agents should accept `n_states`, `n_actions`, `gamma`, and `seed` as shared constructor parameters.
- Algorithm-specific hyperparameters are configurable independently.
- `train(env, **kwargs)` returns training logs following the shared schema.
- `select_action(state, deterministic=True)` returns an integer action ID.
- Deterministic action selection must not update learned parameters.
- `save(path)` and `load(path)` use explicit model-file paths.

## Configuration Rules

**Fixed across algorithms:**
- Game map and initial state.
- State and action spaces.
- Reward system.
- Maximum episode length.
- Discount factor.
- Experiment seeds and evaluation protocol.

**Independently configurable:**
- Learning rates.
- Exploration parameters.
- Convergence thresholds.
- Algorithm-specific training parameters.

## Model Saving and Result Naming

Algorithm identifiers:

- `policy_iteration`
- `q_learning`
- `reinforce`

Use the following naming conventions:

| Output | Filename |
|---|---|
| Model | `{algorithm}_seed{seed}.npz` |
| Training log | `{algorithm}_seed{seed}_training.csv` |
| Evaluation log | `{algorithm}_seed{seed}_evaluation.csv` |
| Metrics | `{algorithm}_metrics.csv` |
| Figure | `{algorithm}_{metric}.png` |

Models must contain the parameters required to reproduce the learned policy. Loading a model must restore its action-selection behavior.

## Reproducibility

- Use the experiment seeds defined in `config.py`.
- Initialize each agent's random-number generator using the assigned seed.
- Record the seed and hyperparameters for every experiment.
- Use separate evaluation episodes without updating learned parameters.

## Termination and Truncation

- Stop episode execution when `terminated or truncated` is true.
- Do not bootstrap future values after true termination.
- For TD learning, bootstrap after external time-limit truncation.
- Policy Iteration models the underlying MDP without the external time limit.
- REINFORCE computes returns from the collected episode trajectory.

## Visualization Contract

- Visualization is implemented separately in `environment/visualization.py`.
- The renderer class is `GridWorldRenderer`.
- The renderer exposes `render(env)` and `close()`.
- Rendering must not modify environment state or learning parameters.
- Training and performance evaluation must run without rendering.

## Environment Usage Example

```python
from environment.gridworld import GridWorldEnv
from config import RIGHT, SEED

env = GridWorldEnv(render_mode=None)

state, info = env.reset(seed=SEED)

next_state, reward, terminated, truncated, info = env.step(RIGHT)

done = terminated or truncated

env.close()
```
## Logging Conventions

- Training logs must be returned as a list of dictionaries.
- Progress and episode indices start at 1.
- Episode rewards represent undiscounted cumulative rewards.
- Training time is cumulative and measured in seconds.
- Non-applicable metrics must be recorded as null.
- Initialize the agent RNG once per independent run.
- Final evaluation must not be used for hyperparameter selection.
- Use one final experiment run per algorithm and seed to avoid overwriting result files.

## State Space Usage

- All agents must use `NUM_STATES = 392` and `NUM_ACTIONS = 4`.
- State IDs must follow the shared encoder.
- Wall states are invalid and must be excluded from MDP construction and policy updates.
- Terminal states are absorbing with zero subsequent reward and zero future value.
- Policy Iteration may include unreachable non-wall states in its transition model, but they must not be treated as reachable gameplay states.
- Q-Learning and REINFORCE must learn through actual environment interactions.
- Unreachable states must not be included in gameplay performance statistics.
- State IDs must not be renumbered or compressed independently.

## Agent Implementation Contract

### Agent Classes

| Algorithm | Module | Class |
|---|---|---|
| Policy Iteration | `agents.policy_iteration` | `PolicyIterationAgent` |
| Q-Learning | `agents.q_learning` | `QLearningAgent` |
| REINFORCE | `agents.reinforce` | `ReinforceAgent` |

### Constructor Parameters

All agents must inherit from `BaseAgent` and accept the following keyword arguments:

- `n_states`
- `n_actions`
- `gamma`
- `seed`

Algorithm-specific constructor parameters:

- Policy Iteration: `theta`, `max_eval_sweeps`, `max_policy_iterations`.
- Q-Learning: `learning_rate`, `epsilon_start`, `epsilon_min`, `epsilon_decay`.
- REINFORCE: `learning_rate`.

Default values must come from `config.py`.

### Training Contract

- Policy Iteration: `train(env, **kwargs)`.
- Q-Learning: `train(env, episodes=TRAIN_EPISODES, **kwargs)`.
- REINFORCE: `train(env, episodes=TRAIN_EPISODES, **kwargs)`.
- All agents return a list of dictionaries following the shared training-log schema.
- Each independent training run must use a newly initialized agent.
- Agents must not modify shared environment rules.

### Action Selection

- `select_action(state, deterministic=True)` returns an integer action ID.
- Policy Iteration returns the action defined by its learned policy.
- Q-Learning uses greedy selection when deterministic and epsilon-greedy selection otherwise.
- REINFORCE uses greedy selection when deterministic and Softmax sampling otherwise.
- Greedy ties are resolved using the smallest action ID.
- Action selection must not update learned parameters.
- Q-Learning epsilon decay occurs once after each training episode.

### Model Persistence

- Policy Iteration saves its policy and value function.
- Q-Learning saves its Q-table.
- REINFORCE saves its policy parameters.
- All agents use the agreed `.npz` model format.
- Loading must restore deterministic action-selection behavior.
- Model dimensions must be validated during loading.