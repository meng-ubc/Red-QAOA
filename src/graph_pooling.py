import numpy as np
import networkx as nx


import torch
from torch_geometric.utils import from_networkx, to_networkx
from torch_geometric.nn import TopKPooling, SAGPooling, ASAPooling
from torch_geometric.data import Data


def calculate_node_features(G):
    # Compute node features
    degrees = np.array([G.degree(n) for n in G.nodes()])
    clustering_coeffs = np.array(list(nx.clustering(G).values()))
    betweenness_centralities = np.array(
        list(nx.betweenness_centrality(G).values()))
    closeness_centralities = np.array(
        list(nx.closeness_centrality(G).values()))
    eigenvector_centralities = np.array(
        list(nx.eigenvector_centrality(G).values()))

    # Normalize features
    features = np.stack([degrees, clustering_coeffs, betweenness_centralities,
                        closeness_centralities, eigenvector_centralities], axis=-1)
    normalized_features = np.array(
        features - features.mean(axis=0)) / features.std(axis=0)

    # a = a[np.isfinite(a)] a[:, np.all(np.isfinite(a), axis=0)]
    return normalized_features[:, np.all(np.isfinite(normalized_features), axis=0)]


def reset_node_indices(G):
    mapping = {node: i for i, node in enumerate(G.nodes())}
    return nx.relabel_nodes(G, mapping)

def get_pooled_graph(graph, ratio, pool_method):
    # Convert the networkx graph to a PyTorch Geometric graph
    data = from_networkx(graph)

    # Add node features to the graph
    data.x = torch.Tensor(calculate_node_features(graph))
    in_channels = data.x.shape[1]

    # Select pooling method
    if pool_method == 'topk':
        pool = TopKPooling(in_channels=in_channels, ratio=ratio)
    elif pool_method == 'sag':
        pool = SAGPooling(in_channels=in_channels, ratio=ratio)
    elif pool_method == 'asa':
        pool = ASAPooling(in_channels=in_channels, ratio=ratio)
    else:
        raise RuntimeError('Unrecognized pooling method')

    # Apply the pooling layer to the graph
    pooled_data = pool(x=data.x, edge_index=data.edge_index)
    
    nx_graph = nx.from_edgelist(list(to_networkx(
        Data(x=pooled_data[0], edge_index=pooled_data[1])).to_undirected().edges()))
    return reset_node_indices(nx_graph)
