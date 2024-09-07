import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Set a dark background for the entire Streamlit app
page_bg = """
    <style>
    body {
        background-color: #1E1E1E;
        color: white;
    }
    </style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Load the pre-saved graph from the .graphml file
graph_path = 'NetworkXUNR/Data/ResearchNetwork.graphml'
G = nx.read_graphml(graph_path)

# List of topics for user selection
topics_list = [
    "Full Graph",
    "Low-Dimensional Topology",
    "Probability Theory",
    "Mathematical Statistics",
    "Stochastic Network Models",
    "Algebraic Topology"
]

# Streamlit App
st.title("Research Network Visualization")

# Dropdown for selecting either the full graph or a specific topic
selected_option = st.selectbox("Choose a topic to visualize:", topics_list)

# Adjust matplotlib parameters for a dark background
rcParams['figure.facecolor'] = '#1E1E1E'
rcParams['axes.facecolor'] = '#1E1E1E'
rcParams['savefig.facecolor'] = '#1E1E1E'
rcParams['text.color'] = 'white'
rcParams['axes.labelcolor'] = 'white'
rcParams['xtick.color'] = 'white'
rcParams['ytick.color'] = 'white'

def plot_two_hop_neighborhood(graph, node):
    """Plots a subgraph consisting of the two-hop neighborhood of the given node."""
    # Get the two-hop neighborhood
    neighbors = set(nx.single_source_shortest_path_length(graph, node, cutoff=2).keys())
    subgraph = graph.subgraph(neighbors)
    
    # Set up the layout for the nodes (Kamada-Kawai layout for nice spacing)
    pos = nx.kamada_kawai_layout(subgraph)

    # Define node colors: Researchers in cyan, Topics in yellow
    node_colors = []
    for node in subgraph.nodes():
        node_type = graph.nodes[node].get('type', 'Unknown')
        if node_type == 'Researcher':
            node_colors.append('#5D3FD3')  # Cyan for researchers
        elif node_type == 'Topic':
            node_colors.append('#FFA500')  # Yellow for topics

    # Define edge colors and styles based on relation types
    edge_colors = []
    edge_styles = []
    for edge in subgraph.edges(data=True):
        relation = edge[2].get('relation', 'Unknown')
        if relation == 'Works_On':
            edge_colors.append('#FF4500')  # Bright orange for "Works_On"
            edge_styles.append('solid')
        elif relation == 'Related_To':
            edge_colors.append('#32CD32')  # Lime green for "Related_To"
            edge_styles.append('dashed')
        else:
            edge_colors.append('#A9A9A9')  # Gray for unknown relations

    # Create the plot
    plt.figure(figsize=(15, 15))
    nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=500)
    nx.draw_networkx_labels(subgraph, pos, font_size=10, font_color='white')
    nx.draw_networkx_edges(subgraph, pos, edge_color=edge_colors, style=edge_styles, width=2)

    # Show the plot in Streamlit
    st.pyplot(plt.gcf())

# If "Full Graph" is selected, plot the full graph
if selected_option == "Full Graph":
    plt.figure(figsize=(15, 15))
    pos = nx.kamada_kawai_layout(G)

    # Define node colors: Researchers in cyan, Topics in yellow
    node_colors = []
    for node in G.nodes():
        node_type = G.nodes[node].get('type', 'Unknown')
        if node_type == 'Researcher':
            node_colors.append('#5D3FD3')  # Cyan for researchers
        elif node_type == 'Topic':
            node_colors.append('#FFA500')  # Yellow for topics

    # Define edge colors and styles based on relation types
    edge_colors = []
    edge_styles = []
    for edge in G.edges(data=True):
        relation = edge[2].get('relation', 'Unknown')
        if relation == 'Works_On':
            edge_colors.append('#FF4500')  # Bright orange for "Works_On"
            edge_styles.append('solid')
        elif relation == 'Related_To':
            edge_colors.append('#32CD32')  # Lime green for "Related_To"
            edge_styles.append('dashed')
        else:
            edge_colors.append('#A9A9A9')  # Gray for unknown relations

    # Draw the full graph
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='white')
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, style=edge_styles, width=2)

    st.pyplot(plt.gcf())

# If a specific topic is selected, plot the two-hop neighborhood
else:
    # Plot two-hop neighborhood for the selected topic
    if selected_option in G.nodes:
        plot_two_hop_neighborhood(G, selected_option)
    else:
        st.write("The selected topic is not in the graph.")
