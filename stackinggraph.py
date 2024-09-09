import networkx as nx
import json
import matplotlib.pyplot as plt
import flor

# Path to the JSON file containing the fake papers
file_path = "./fake_papers.json"

# Load the data from the JSON file
with open(file_path, "r") as file:
    data = json.load(file)  # Use json.load to read from a file object

# Create a directed graph
G = nx.DiGraph()


# Function to extract the primary author from a citation
def extract_primary_author(citation):
    # Assuming the author's name ends with "et al."
    author_part = citation.split(" et al.")[0]
    return author_part.strip()


# Dictionary to keep track of citations for each author
author_citations = {}

# Iterate through each paper in the data
for paper in data:
    paper_title = paper["title"]
    author = paper["Author"]

    # Add nodes for the paper and the author
    G.add_node(paper_title, type="paper")
    G.add_node(author, type="author")

    # Add an edge from the author to their own paper
    G.add_edge(author, paper_title, color="blue")

    # Initialize citation set for the author if not already present
    if author not in author_citations:
        author_citations[author] = set()

    # Iterate through the references of the paper
    for ref in paper["references"]:
        cited_title = ref.split(",")[1].strip()  # Extract the title of the cited paper
        primary_author = extract_primary_author(
            ref
        )  # Extract the primary author of the cited paper

        # Add nodes for the cited paper and the primary author if not already present
        if not G.has_node(cited_title):
            G.add_node(cited_title, type="cited_paper")
        if not G.has_node(primary_author):
            G.add_node(primary_author, type="author")

        # Add an edge from the current paper to the primary author of the cited paper
        G.add_edge(paper_title, primary_author, color="green")

        # Initialize citation set for the primary author if not already present
        if primary_author not in author_citations:
            author_citations[primary_author] = set()
        # Add the primary author to the citation set of the current author
        author_citations[author].add(primary_author)

    # Create bidirectional edges (red) between authors that cite each other
    for author in author_citations:
        for cited_author in author_citations[author]:
            if author in author_citations.get(cited_author, set()):
                G.add_edge(author, cited_author, color="red")
                G.add_edge(cited_author, author, color="red")

# Generate positions for all nodes using spring layout
pos = nx.spring_layout(G)

# Get edges with their attributes
edges = G.edges(data=True)

# Draw nodes with a specific size and color
nx.draw_networkx_nodes(G, pos, node_size=70, node_color="lightblue")

# Draw edges based on their specified colors
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[(u, v) for u, v, d in edges if d["color"] == "green"],
    edge_color="green",
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[(u, v) for u, v, d in edges if d["color"] == "red"],
    edge_color="red",
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[(u, v) for u, v, d in edges if d["color"] == "blue"],
    edge_color="blue",
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[(u, v) for u, v, d in edges if d["color"] == "black"],
    edge_color="blue",
)

# Draw labels for the nodes
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

# Set the title of the plot
plt.title("Enhanced Citation Network Visualization")

# Turn off the axis
plt.axis("off")

# Show the plot
plt.show()
