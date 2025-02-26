import json
import numpy as np
from scipy import sparse
import cidre
import matplotlib.pyplot as plt

# Load citations.json
try:
    with open('outputs/citations.json', 'r') as f:
        citations_data = json.load(f)['citations']
except FileNotFoundError:
    print("Error: 'outputs/citations.json' not found. Please check the file path.")
    exit(1)

# Build adjacency matrix
citation_ids = sorted(set(c['id'] for c in citations_data))
id_to_idx = {cid: i for i, cid in enumerate(citation_ids)}
n_nodes = len(citation_ids)

data, row, col = [], [], []
for citation in citations_data:
    source_idx = id_to_idx[citation['id']]  # Define source_idx for the source node
    for target_id in citation['citation_graph']:
        if target_id in id_to_idx:  # Ensure target exists
            target_idx = id_to_idx[target_id]  # Define target_idx for the target node
            # Use 1 for unweighted citations; adjust for weights if available
            data.append(1)  
            row.append(source_idx)
            col.append(target_idx)

# Create sparse matrix (CSR format)
try:
    A = sparse.csr_matrix((data, (row, col)), shape=(n_nodes, n_nodes))
    print(f"Adjacency matrix shape: {A.shape}")
except ValueError as e:
    print(f"Error creating adjacency matrix: {e}")
    exit(1)

# Initialize and run CIDRE
try:
    alg = cidre.Cidre(group_membership=None)  # No pre-existing communities
    groups = alg.detect(A, threshold=0.15)  # Adjust threshold for tighter/smaller groups
except Exception as e:
    print(f"Error running CIDRE: {e}")
    exit(1)

# Map nodes to labels
def map_nodes_to_labels(node_ids, citation_data):
    labels = {}
    for node_id in node_ids:
        citation = next((c for c in citation_data if c['id'] == node_id), None)
        if citation:
            labels[node_id] = citation['title'][:30] + '...'  # Shorten for readability
        else:
            labels[node_id] = f"Unknown (ID: {node_id})"
    return labels

# Print and visualize groups
for i, group in enumerate(groups):
    donor_labels = {id_to_idx[k]: v for k, v in group.donors.items() if k in id_to_idx}
    recipient_labels = {id_to_idx[k]: v for k, v in group.recipients.items() if k in id_to_idx}
    print(f"Group {i + 1}:")
    print(f" - Donors: {donor_labels}")
    print(f" - Recipients: {recipient_labels}")
    print(f" - Size (nodes): {group.size()}")
    print(f" - Within edges: {group.get_within_edges()}")
    
    # Visualization
    try:
        fig, ax = plt.subplots(figsize=(7, 10))
        dc = cidre.DrawGroup()
        node_labels = map_nodes_to_labels(set(group.donors.keys()) | set(group.recipients.keys()), citations_data)
        dc.draw(group, ax=ax, node_labels=node_labels)
        plt.title(f"Group {i + 1} - Anomalous Citation Pattern")
        plt.savefig(f'group_{i+1}_visualization.png')
        plt.close()  # Close to avoid overlap
    except Exception as e:
        print(f"Error visualizing Group {i + 1}: {e}")

print("Visualizations saved as 'group_X_visualization.png' for each group (if successful)")