import json
import networkx as nx
import matplotlib.pyplot as plt

# Define the functions provided
def process_adjacency_json(adjacency_json):
    adjacency_connections = {}
    for space, adjacent_spaces in adjacency_json.items():
        adjacency_connections[space] = set(adjacent_spaces)
    return adjacency_connections

def process_door_json(door_json):
    door_connections = {}
    for space, doors in door_json.items():
        if space not in door_connections:
            door_connections[space] = set()
        for door in doors:
            if isinstance(door, dict) and door["Related_Building_Element_IFC_Type"] == "IfcDoor":
                door_connections[space].add(door["Related_Building_Element_Name"])  # Use "Name" instead of "GlobalID"
    return door_connections

def process_stairs_json(stairs_json):
    stairs_connections = {}
    for space, stairs in stairs_json.items():
        if space not in stairs_connections:
            stairs_connections[space] = set()
        for stair in stairs:
            if isinstance(stair, dict) and stair["Related_Building_Element_IFC_Type"] == "IfcStair":
                stairs_connections[space].add(stair["Related_Building_Element_Name"])  # Use "Name" instead of "GlobalID"
    return stairs_connections

def build_spaces_dict(adjacency_connections, door_connections, stairs_connections):
    spaces = {}
    for space, adjacent_spaces in adjacency_connections.items():
        if space not in spaces:
            spaces[space] = {}
        for adj_space in adjacent_spaces:
            if adj_space != "Outside":
                spaces[space][adj_space] = "adjacency"
    for space, door_spaces in door_connections.items():
        if space not in spaces:
            spaces[space] = {}
        for door_space in door_spaces:
            if door_space != space:
                spaces[space][door_space] = "door"
    for space, stair_spaces in stairs_connections.items():
        if space not in spaces:
            spaces[space] = {}
        for stair_space in stair_spaces:
            if stair_space != space:
                spaces[space][stair_space] = "stair"
    return spaces

def build_connections_dict(spaces):
    connections = {"adjacency": set(), "door": set(), "stair": set()}
    for space, connections_dict in spaces.items():
        for connected_space, connection_type in connections_dict.items():
            connections[connection_type].add((space, connected_space))
    return connections

# Load JSON files
adjacency_json_file = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\output\AC20-FZK-Haus_adjacent_spaces.json'
door_json_file = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\output\AC20-FZK-Haus_space_boundaries.json'
stairs_json_file = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\output\AC20-FZK-Haus_space_stairs.json'

with open(adjacency_json_file, 'r') as file:
    adjacency_json = json.load(file)

with open(door_json_file, 'r') as file:
    door_json = json.load(file)

with open(stairs_json_file, 'r') as file:
    stairs_json = json.load(file)

# Process JSON files
adjacency_connections = process_adjacency_json(adjacency_json)
door_connections = process_door_json(door_json)
stairs_connections = process_stairs_json(stairs_json)

# Build spaces and connections dictionaries
spaces = build_spaces_dict(adjacency_connections, door_connections, stairs_connections)
connections = build_connections_dict(spaces)
print(spaces)
print(connections)

# Load labels for spaces
labels_json = {
    "4": "Schlafzimmer",
    "3": "Bad",
    "2": "Buero",
    "5": "Wohnen",
    "1": "Flur",
    "6": "K\u00fcche",
    "7": "Galerie"
}

# Create a graph
G = nx.Graph()

# Add nodes for spaces, doors, and stairs
for space in spaces:
    G.add_node(space, color='blue', node_type='space', label=labels_json.get(space, space))
for door in set(door for door_list in door_connections.values() for door in door_list):
    G.add_node(door, color='green', node_type='door', label=door)
for stair in set(stair for stair_list in stairs_connections.values() for stair in stair_list):
    G.add_node(stair, color='orange', node_type='stair', label=stair)  # Use orange color for stairs

# Add edges based on connections
for conn_type, edges in connections.items():
    G.add_edges_from(edges)

# Extract node colors and labels
node_colors = [G.nodes[node]['color'] for node in G.nodes]
node_labels = {node: G.nodes[node]['label'] for node in G.nodes}

# Draw the graph
pos = nx.spring_layout(G)  # You can choose different layouts
nx.draw(G, pos, with_labels=True, labels=node_labels, node_color=node_colors, edge_color='gray', node_size=1000, font_size=10, font_color='black', font_weight='bold')

# Create a legend
legend_labels = {'space': 'blue', 'door': 'green', 'stair': 'orange'}
for label, color in legend_labels.items():
    plt.scatter([], [], c=color, label=label)
plt.legend(loc='best', title='Node Types')

plt.title('Accessibility Network Graph')
plt.show()
