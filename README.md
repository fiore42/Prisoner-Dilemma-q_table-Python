# Iterative Prisoner's Dilemma in Python

This repository contains a Python implementation of the Iterative Prisoner's Dilemma, featuring over 25 common strategies along with a reinforcement learning strategy implemented using a q_table approach (not DQN). The program is designed to simulate 9 strategies facing each other in the Prisoner's Dilemma, a standard example of a game analyzed in game theory that shows why two completely rational individuals might not cooperate, even if it appears that it is in their best interest to do so.

For more details on this project, check [this Medium article](https://fiore42.medium.com/from-zero-to-reinforcement-learning-rl-with-gpt4-2977405a0223)

## Features

- **Multiple Strategies**: Over 25 predefined strategies to simulate various scenarios in the Prisoner's Dilemma.
- **Reinforcement Learning Strategy**: A strategy built using a q_table approach to reinforcement learning, providing an advanced and adaptive strategy model.
- **Strategy Selection**: By default, the program randomly selects 9 strategies for each run, always including the `rl_strategy`. However, users have the option to specify a custom list of strategies using `-a`.
- **Verbose Output**: Supports `-v` (verbose) and `-vv` (very verbose) flags for additional debugging and operational insights.

## Getting Started

### Prerequisites

Ensure you have Python installed on your machine. This code is compatible with Python 3.x.

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/fiore42/Prisoner-Dilemma-q_table-Python.git
cd Prisoner-Dilemma-q_table-Python
```

### Usage

Run the program with the default settings:

```bash
python main.py
```

To select specific strategies, use the `-a` option followed by the strategy names:

```bash
python main.py -a strategy1 strategy2 ... strategyN
```

Use the verbose options for more detailed output:

```bash
# Verbose
python main.py -v

# Very Verbose
python main.py -vv
```

## Contributing

Contributions to the project are welcome! Please feel free to submit a pull request or open an issue for bugs, suggestions, or feature requests.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Inspired by [this YouTube video](https://www.youtube.com/watch?v=mScpHTIi-kM) on the Prisoner's Dilemma.

