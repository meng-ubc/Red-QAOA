# Red-QAOA Repository

This repository contains the source code and experimental scripts for the "Red-QAOA" (Quantum Approximate Optimization Algorithm) variant, as well as the relevant graph datasets used in our study.

## Directory Structure

- `src/`: Contains the source files of the Red-QAOA implementation.
- `experiments/`: Houses the scripts for conducting various experiments as described in the paper.
- `graph_sets/`: Includes the graph datasets (Linux, AIDS, IMDb) used in our experiments.
- `additional_experiments/`: Houses the scripts for conducting additional experiments in the paper.

## Installation

### Prerequisites

- Python 3.11

### Steps

1. **Install Required Packages:**
   Ensure Python 3.11 is installed on your system. Then, run the following command to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

2. **Optional GPU Support:**
    For users with CUDA-enabled systems, the qiskit-aer-gpu package can be installed separately for GPU acceleration:
```bash
pip install qiskit-aer-gpu
```

## Running Experiments

Each experiment script in the `experiments/` folder corresponds to different evaluations of the Red-QAOA. Below are the key experiments:

1. **MSE Analysis in Noisy and Ideal Conditions:** 
- Script: `mse_noisy.py` and `mse_ideal.py`
- Required and optional arguments are detailed within each script.

2. **End-to-End Performance Evaluation:**
- Script: `end_to_end.py`
- The script's arguments allow for customization and detailed performance analysis.

Refer to the individual script documentation for detailed usage instructions.

## Additional Experiments

Additional experiments and their guides are available in the repository. These supplement the key experiments and provide further insights into Red-QAOA's capabilities.

## Experiment Customization

Experiment parameters such as the number of QAOA layers are set as required arguments for consistency with the study. Optional arguments are available for more in-depth and varied testing.

## Hardware and Software Dependencies

- Optional: CUDA-enabled NVidia GPUs for enhanced performance.
- Required software: Qiskit, Networkx, Scipy.
- Optional software: torch-geometric for comparing Red-QAOA with GNN-based methods.

## Data Sets

The `graph_sets/` folder includes the following datasets:
- Linux
- AIDS
- IMDb

These are used across various experiments to evaluate the Red-QAOA's performance.

