# Artifact Evaluation Figure Reproduce Guide

This document aims to provide a comprehensive guide to reproduce and verify the results and figures presented in the paper.

In this repository, you will find a series of scripts and detailed instructions designed to facilitate the replication of our key experiments and the generation of the exact figures as shown in the paper.

## Getting Started

Before proceeding, ensure that you have the required packages installed. The packages can be installed using the following command:

   ```bash
   pip install -r requirements.txt
   ```

Now, you are ready to reproduce the experiments and generate figures.


## Reproducing Experiments

In this section, we guide you through the process of generating the results for the figures with the experiment scripts included in this repository. The scripts are in the "experiments" directory and have been specifically designed for ease of execution and accurate replication of our research findings. Once these scripts are run, the results of the experiments will be automatically saved, thus ensuring a straightforward and efficient replication process.

**Note**: It is crucial to be in the 'experiments' directory before executing the scripts. This directory contains all the necessary code and data files required for the experiments.

## Generating Figures

### Figure 10

1. **Preparation**: Execute the following commands in the 'experiments' directory to generate the data for Figure 10:

   ```bash
   python mse_noisy.py -n 7
   python mse_noisy.py -n 8
   python mse_noisy.py -n 9
   python mse_noisy.py -n 10
   python mse_noisy.py -n 11
   python mse_noisy.py -n 12
   python mse_noisy.py -n 13
   python mse_noisy.py -n 14
   ```


2. **Generating the Figure**: Once the data is prepared, navigate to the 'plot_figures' directory and run the following command to generate Figure 10:

   ```bash
   python fig10.py
   ```

#### Approximate Execution Time
- Note that running the scripts with n > 12 on a CPU can be very time-consuming, potentially taking several hours. It is highly recommended to use a GPU-accelerated platform for these cases (add the --use_gpu flag for GPU acceleration).
- The plot script does not require all 'n' values to generate the plot. Results for n=13 and n=14 can be omitted if needed to save time.


### Figures 13 & 14

1. **Preparation**: Execute the following commands in the 'experiments' directory to generate the data for Figure 13 & 14:

   ```bash
   python mse_ideal.py --graph_set aids --p 1
   python mse_ideal.py --graph_set aids --p 2
   python mse_ideal.py --graph_set aids --p 3
   python mse_ideal.py --graph_set linux --p 1
   python mse_ideal.py --graph_set linux --p 2
   python mse_ideal.py --graph_set linux --p 3
   python mse_ideal.py --graph_set imdb --p 1
   python mse_ideal.py --graph_set imdb --p 2
   python mse_ideal.py --graph_set imdb --p 3
   ```


2. **Generating the Figure**: Once the data is prepared, navigate to the 'plot_figures' directory and run the following command to generate Figure 13 & 14:

   ```bash
   python fig13.py
   python fig14.py
   ```

#### Approximate Execution Time

- The execution time for generating this figure can vary significantly based on the `--num_points` and `--num_graphs` parameters. By default, `--num_points` is set to 1024 and `--num_graphs` to 100, which offers a comprehensive result but may require a substantial amount of time to process, especially on less powerful hardware.

- To reduce the execution time, you can decrease these parameters. We recommend maintaining `--num_points` greater than 100 and `--num_graphs` more than 10 to ensure a balance between time efficiency and the quality of results. 

### Figures 15 & 16

1. **Preparation**: To generate the data for Figures 15 & 16, execute the following commands in the 'experiments' directory. These are in addition to the commands used for Figures 13 & 14:

   ```bash
   python mse_ideal.py --min_nodes 10 --max_nodes 20 --graph_set imdb --p 1
   python mse_ideal.py --min_nodes 10 --max_nodes 20 --graph_set imdb --p 2
   python mse_ideal.py --min_nodes 10 --max_nodes 20 --graph_set imdb --p 3
   ```

2. **Generating the Figure**: Once the data is prepared, navigate to the 'plot_figures' directory and run the following command to generate Figure 15 & 16:

   ```bash
   python fig15.py
   python fig16.py
   ```

#### Approximate Execution Time
- Similar to the previous figures, the --num_points and --num_graphs parameters can be adjusted based on available resources. Reducing these values will decrease execution time but may also affect the granularity of the results.

### Figures 17
1. **Preparation**: Execute the following commands in the 'experiments' directory to generate the data for Figure 17:

   ```bash
   python end_to_end.py --num_graphs 100 --num_nodes 10 --p 1
   python end_to_end.py --num_graphs 100 --num_nodes 10 --p 2
   python end_to_end.py --num_graphs 100 --num_nodes 10 --p 3
   ```


2. **Generating the Figure**: Once the data is prepared, navigate to the 'plot_figures' directory and run the following command to generate Figure 17:

   ```bash
   python fig17.py
   ```

#### Approximate Execution Time
- The --num_graphs parameter can be reduced to expedite the data generation process. While the default is set to 100, a lower value can be used to save time. We suggest keeping --num_graphs greater than 10 to maintain a representative sample size for accurate analysis.