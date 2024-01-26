import argparse
import networkx as nx
import numpy as np
from tqdm import tqdm
from scipy.optimize import minimize
import json

import path

from qiskit.circuit import Parameter
from qiskit import Aer
from qiskit_aer import AerError

from qaoa_util import compute_expectation, create_qaoa_circ
from red_qaoa import red_qaoa_exe


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--num_graphs", type=int, required=True, help="number of graphs to test"
    )
    parser.add_argument("--p", type=int, required=True, help="QAOA layers")

    parser.add_argument(
        "--num_nodes", type=int, default=30, help="number of nodes in the graph"
    )
    parser.add_argument("--shots", type=int, default=8192, help="number of shots")
    parser.add_argument("--use_gpu", action="store_true", help="use GPU backend")

    return parser.parse_args()


def get_expectation(
    G,
    p,
    shots,
    gpu,
):
    parameters = [Parameter("theta" + str(i)) for i in range(2 * p)]

    circuit = create_qaoa_circ(parameters, G)

    backend = Aer.get_backend("qasm_simulator")

    if gpu:
        try:
            backend.set_options(device="GPU")
        except AerError as e:
            print(e)

    def execute_circ(theta):
        theta = np.array(theta)

        counts = (
            backend.run(
                circuit.bind_parameters(
                    {parameters[i]: theta[i] for i in range(2 * p)}
                ),
                shots=shots,
            )
            .result()
            .get_counts()
        )

        return compute_expectation(counts, G)

    return execute_circ


def perform_optimization(args, graph, red_graph):
    get_exps = get_expectation(graph, args.p, args.shots, args.use_gpu)
    get_exps_red = get_expectation(red_graph, args.p, args.shots, args.use_gpu)

    # Define the initial guess for the minimum
    x0 = np.random.rand(args.p * 2) * np.pi
    # Minimize the function
    baseline_result = minimize(get_exps, x0, method="COBYLA")
    red_qaoa_result = minimize(get_exps_red, x0, method="COBYLA")

    baseline_fun = baseline_result.fun
    red_qaoa_fun = get_exps(red_qaoa_result.x)

    return baseline_fun, red_qaoa_fun


def main():
    # parse arguments
    args = get_args()

    restarts = 20 if args.p == 1 else 50 if args.p == 2 else 100

    # create testing and red-qaoa graph
    testing_graphs = [
        nx.gnp_random_graph(args.num_nodes, 0.5) for _ in range(args.num_graphs)
    ]

    ratio_average = []
    ratio_optimal = []

    for graph in tqdm(testing_graphs, desc="Testing graphs"):
        red_graph = red_qaoa_exe(graph)

        baseline_funs = []
        red_qaoa_funs = []
        for _ in tqdm(range(restarts), leave=False, desc="restarts"):
            baseline_fun, red_qaoa_fun = perform_optimization(args, graph, red_graph)

            baseline_funs.append(baseline_fun)
            red_qaoa_funs.append(red_qaoa_fun)

        ratio_average.append(np.mean(red_qaoa_funs) / np.mean(baseline_funs))
        ratio_optimal.append(np.min(red_qaoa_funs) / np.min(baseline_funs))

    print(f"Optimal ratio: {np.mean(ratio_optimal)}")
    print(f"Average ratio: {np.mean(ratio_average)}")

    new_results = {
        args.p: [
            (np.mean(ratio_optimal), np.std(ratio_optimal)),
            (np.mean(ratio_average), np.std(ratio_average)),
        ]
    }

    # Load existing data if available
    try:
        with open("end_to_end_results.json", "r") as file:
            existing_results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_results = {}

    # Update existing data with new data
    existing_results.update(new_results)

    # Save the updated data back to the file
    with open("end_to_end_results.json", "w") as file:
        json.dump(existing_results, file)


if __name__ == "__main__":
    main()
