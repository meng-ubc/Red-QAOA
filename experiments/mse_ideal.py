import argparse
import networkx as nx
import numpy as np
from tqdm import tqdm

import path

from qiskit.circuit import Parameter
from qiskit import Aer
from qiskit_aer import AerSimulator, AerError

from qaoa_util import compute_expectation, create_qaoa_circ
from red_qaoa import red_qaoa_exe
import json


def get_sampled_landscape(circ, backend, graph, thetas, theta_vals, shots, taskname):
    exps = []

    for theta in tqdm(theta_vals, desc=taskname):
        binded_circ = circ.bind_parameters({k: v for k, v in zip(thetas, theta)})

        counts = backend.run(binded_circ, shots=shots).result().get_counts()

        exps.append(compute_expectation(counts, graph))

    return np.array(exps)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph_set", type=str, required=True, help="graph dataset to use"
    )
    parser.add_argument("--p", type=int, required=True, help="QAOA layers")
    parser.add_argument(
        "--num_points",
        type=int,
        default=1024,
        help="number of points sampled for landscape",
    )
    parser.add_argument(
        "--num_graphs", type=int, default=100, help="number of graphs to test"
    )
    parser.add_argument("--shots", type=int, default=8192, help="number of shots")
    parser.add_argument("--use_gpu", action="store_true", help="use GPU backend")

    parser.add_argument(
        "--min_nodes", type=int, default=0, help="minimum number of nodes"
    )
    parser.add_argument(
        "--max_nodes", type=int, default=10, help="maximum number of nodes"
    )

    return parser.parse_args()


def get_graphs(graph_set, num_graphs, min_nodes, max_nodes):
    with open(f"../graph_sets/{graph_set}.json", "r") as f:
        raw_graphs = json.load(f)

        graphs = [nx.Graph(edge_list) for edge_list in raw_graphs]

        filtered_graphs = [
            g
            for g in graphs
            if g.number_of_nodes() >= min_nodes and g.number_of_nodes() <= max_nodes
        ]

        np.random.shuffle(filtered_graphs)

        return filtered_graphs[:num_graphs]


def main():
    # parse arguments
    args = get_args()

    # create testing and red-qaoa graph
    testing_graphs = get_graphs(
        args.graph_set, args.num_graphs, args.min_nodes, args.max_nodes
    )

    # create ideal and noisy circuit simulators
    ideal_backend = Aer.get_backend("qasm_simulator", device="CPU")

    if args.use_gpu:
        try:
            ideal_backend.set_options(device="GPU")
        except AerError as e:
            print(e)

    node_reductions = []
    edge_reductions = []
    mse = []

    theta_vals = np.random.uniform(0, 2 * np.pi, (args.num_points, 2 * args.p))

    for i, graph in enumerate(testing_graphs):
        red_graph = red_qaoa_exe(graph)

        node_reductions.append(
            1 - red_graph.number_of_nodes() / graph.number_of_nodes()
        )
        edge_reductions.append(
            1 - red_graph.number_of_edges() / graph.number_of_edges()
        )

        # create 1-layer qaoa circuits
        theta_names = [f"theta_{i}" for i in range(2 * args.p)]
        thetas = [Parameter(theta_name) for theta_name in theta_names]

        circ = create_qaoa_circ(thetas, graph)
        circ_red_qaoa = create_qaoa_circ(thetas, red_graph)

        baseline_landscape = get_sampled_landscape(
            circ,
            ideal_backend,
            graph,
            thetas,
            theta_vals,
            args.shots,
            f"Ideal Landscape {i+1}",
        )

        red_qaoa_landscape = get_sampled_landscape(
            circ_red_qaoa,
            ideal_backend,
            red_graph,
            thetas,
            theta_vals,
            args.shots,
            f"Red-QAOA Landscape {i+1}",
        )

        baseline_landscape /= baseline_landscape.min()
        red_qaoa_landscape /= red_qaoa_landscape.min()

        mse.append(np.mean((baseline_landscape - red_qaoa_landscape) ** 2))

    print(f"Node Reduction: {np.mean(node_reductions)}")
    print(f"Edge Reduction: {np.mean(edge_reductions)}")
    print(f"MSE: {np.mean(mse)}")

    new_results_key = f"{args.graph_set}_{args.p}"

    if args.graph_set == "imdb":
        if args.max_nodes > 10:
            new_results_key += "_medium"
        else:
            new_results_key += "_small"

    new_results = {
        new_results_key: [
            (np.mean(node_reductions), np.std(node_reductions)),
            (np.mean(edge_reductions), np.std(edge_reductions)),
            (np.mean(mse), np.std(mse)),
        ]
    }

    # Load existing data if available
    try:
        with open("mse_ideal_results.json", "r") as file:
            existing_results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_results = {}

    # Update existing data with new data
    existing_results.update(new_results)

    # Save the updated data back to the file
    with open("mse_ideal_results.json", "w") as file:
        json.dump(existing_results, file)


if __name__ == "__main__":
    main()
