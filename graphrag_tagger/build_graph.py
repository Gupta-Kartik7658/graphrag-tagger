import os
import json
import numpy as np
from glob import glob
from tqdm import tqdm
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def load_raw_files(input_folder: str, pattern: str="*.json"):
    files = sorted(glob(os.path.join(input_folder, pattern)))
    print(f"Found {len(files)} files in {input_folder}.")
    raws = [json.load(open(f)) for f in files]
    print(f"Loaded {len(raws)} raw documents.")
    return raws

def compute_scores(raws):
    # Count topic rankings
    counter: dict[str, dict] = {}
    for raw in raws:
        for i, topic in enumerate(raw["classification"], start=1):
            if topic not in counter:
                counter[topic] = {}
            counter[topic][i] = counter[topic].get(i, 0) + 1
    # Compute scores
    df = pd.DataFrame(counter).T
    df.fillna(0, inplace=True)
    scores = df.apply(lambda x: sum(i * j for i, j in x.items()), axis=1)
    totals = scores.sum()
    scores = scores.apply(lambda x: np.log(totals / x))
    scores_map = scores.to_dict()
    return scores_map

def build_graph(raws, scores_map):
    chunks = raws
    G = nx.Graph()
    for idx, chunk in enumerate(chunks):
        G.add_node(idx, chunk_text=chunk["chunk"], source=chunk["source_file"], classifications=chunk["classification"])
    
    def compute_contribution(rank1: int, rank2: int, topic: str) -> float:
        return 1.0/(rank1+1) + 1.0/(rank2+1) + scores_map[topic]
    
    for i in range(len(chunks)):
        for j in range(i+1, len(chunks)):
            common_details = []
            total_weight = 0.0
            classifications_i = chunks[i]["classification"]
            classifications_j = chunks[j]["classification"]
            topics = set(classifications_i).intersection(classifications_j)
            for topic in topics:
                rank_i = classifications_i.index(topic)
                rank_j = classifications_j.index(topic)
                contribution = compute_contribution(rank_i, rank_j, topic)
                common_details.append({"topic": topic, "rank_i": rank_i, "rank_j": rank_j, "contribution": contribution})
                total_weight += contribution
            if common_details:
                G.add_edge(i, j, weight=total_weight, common=common_details)
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())
    return G

def prune_graph(G, threshold_percentile: float):
    edge_weights = [data.get('weight', 0) for _, _, data in G.edges(data=True)]
    print("Min weight:", min(edge_weights))
    print("Max weight:", max(edge_weights))
    print("Mean weight:", np.mean(edge_weights))
    print("Median weight:", np.median(edge_weights))
    threshold = np.percentile(edge_weights, threshold_percentile)
    print(f"Pruning threshold ({threshold_percentile}th percentile):", threshold)
    G_pruned = G.copy()
    edges_to_remove = [(u, v) for u, v, data in G_pruned.edges(data=True) if data.get('weight', 0) < threshold]
    print(f"Removing {len(edges_to_remove)} edges out of {G_pruned.number_of_edges()}...")
    G_pruned.remove_edges_from(edges_to_remove)
    print("Pruned graph - Number of nodes:", G_pruned.number_of_nodes())
    print("Pruned graph - Number of edges:", G_pruned.number_of_edges())
    return G_pruned

def update_graph_components(G):
    components = list(nx.connected_components(G))
    print("Number of connected components:", len(components))
    component_map = {}
    for comp_id, comp_nodes in enumerate(components):
        for node in comp_nodes:
            component_map[node] = comp_id
    nx.set_node_attributes(G, component_map, 'component_id')
    component_sizes = [len(comp) for comp in components]
    print("Component sizes (min, max, mean):", np.min(component_sizes), np.max(component_sizes), np.mean(component_sizes))
    return component_map

def process_graph(input_folder: str, output_folder: str, pattern: str="*.json", threshold_percentile: float=97.5):
    """
    Process JSON files from input_folder, build and prune a graph,
    and save connected components to output_folder.
    """
    if threshold_percentile < 1:
        threshold_percentile *= 100
    os.makedirs(output_folder, exist_ok=True)
    raws = load_raw_files(input_folder, pattern)
    scores_map = compute_scores(raws)
    G = build_graph(raws, scores_map)
    G_pruned = prune_graph(G, threshold_percentile)
    component_map = update_graph_components(G_pruned)
    output_file = os.path.join(output_folder, "connected_components.json")
    with open(output_file, "w") as f:
        json.dump(component_map, f)
    print(f"Connected components map saved to {output_file}")
    return G_pruned

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process graph from JSON files.")
    parser.add_argument("--input_folder", type=str, default="data/test/results", help="Folder with input JSON files.")
    parser.add_argument("--output_folder", type=str, default="data/test", help="Folder to save output JSON.")
    parser.add_argument("--threshold_percentile", type=float, default=97.5, help="Percentile threshold for pruning edges.")
    args = parser.parse_args()
    
    process_graph(args.input_folder, args.output_folder, threshold_percentile=args.threshold_percentile)