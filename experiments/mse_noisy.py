import argparse
import networkx as nx
import numpy as np
from tqdm import tqdm

import path

from qiskit.circuit import Parameter
from qiskit import Aer, transpile
from qiskit.providers.fake_provider import FakeToronto
from qiskit_aer import AerSimulator, AerError

from qaoa_util import compute_expectation, create_qaoa_circ
from red_qaoa import red_qaoa_exe


def grid_search(circ, backend, graph, thetas, shots, width, taskname):
    # Create a grid of search points in range [0, pi]
    beta_vals = np.linspace(0, np.pi, width)
    gamma_vals = np.linspace(0, 2 * np.pi, width)

    exps = []

    for x in tqdm(gamma_vals, desc=taskname):
        sub_exps = []

        for y in tqdm(beta_vals, leave=False):
            params = [x, y]

            binded_circ = circ.bind_parameters({k: v for k, v in zip(thetas, params)})

            counts = backend.run(binded_circ, shots=shots).result().get_counts()

            sub_exps.append(compute_expectation(counts, graph))

        exps.append(sub_exps)

    return np.array(exps)


def get_args():
    parser = argparse.ArgumentParser(description="Create a random graph")
    parser.add_argument(
        "-n", type=int, required=True, help="number of nodes in the graph"
    )
    parser.add_argument("--width", type=int, default=32, help="width of search grid")
    parser.add_argument("--shots", type=int, default=8192, help="number of shots")
    parser.add_argument("--use_gpu", action="store_true", help="use GPU backend")

    return parser.parse_args()


def transpile_circuit(circ, backend):
    min_depth = 100000
    min_circ = None

    for _ in range(100):
        temp_circ = transpile(circ, backend=backend, routing_method="sabre")
        if temp_circ.depth() < min_depth:
            min_depth = temp_circ.depth()
            min_circ = temp_circ
    return min_circ


def main():
    # parse arguments
    args = get_args()

    # create testing and red-qaoa graph
    graph = nx.gnp_random_graph(args.n, 0.5)
    red_graph = red_qaoa_exe(graph)

    # create ideal and noisy circuit simulators
    ideal_backend = Aer.get_backend("qasm_simulator", device="CPU")

    device_backend = FakeToronto()
    noisy_backend = AerSimulator.from_backend(device_backend, method="density_matrix")

    if args.use_gpu:
        try:
            noisy_backend.set_options(device="GPU")
        except AerError as e:
            print(e)

    # create 1-layer qaoa circuits
    theta_names = [f"theta_{i}" for i in range(2)]
    thetas = [Parameter(theta_name) for theta_name in theta_names]
    circ = create_qaoa_circ(thetas, graph)
    circ = transpile_circuit(circ, noisy_backend)

    circ_red_qaoa = create_qaoa_circ(thetas, red_graph)
    circ_red_qaoa = transpile_circuit(circ_red_qaoa, noisy_backend)

    ideal_landscape = grid_search(
        circ, ideal_backend, graph, thetas, args.shots, args.width, "Ideal Landscape"
    )

    noisy_landscape = grid_search(
        circ, noisy_backend, graph, thetas, args.shots, args.width, "Noisy Landscape"
    )

    red_qaoa_landscape = grid_search(
        circ_red_qaoa,
        noisy_backend,
        red_graph,
        thetas,
        args.shots,
        args.width,
        "Red-QAOA Landscape",
    )

    ideal_landscape /= ideal_landscape.min()
    noisy_landscape /= noisy_landscape.min()
    red_qaoa_landscape /= red_qaoa_landscape.min()

    baseline_mse = np.mean((ideal_landscape - noisy_landscape) ** 2)
    red_qaoa_mse = np.mean((ideal_landscape - red_qaoa_landscape) ** 2)

    print("Mean Square Error:", baseline_mse)
    print("Mean Square Error red:", red_qaoa_mse)


if __name__ == "__main__":
    main()
