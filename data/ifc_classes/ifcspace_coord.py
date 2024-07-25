import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.placement
import ifcopenshell.util.shape
import numpy as np
import pandas as pd

# Load the IFC file
file_path = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\AC20-FZK-Haus.ifc'
model = ifcopenshell.open(file_path)

# Function to get vertices of a space and transform to global coordinates
def get_space_global_vertices(space):
    # Get the local placement of the space
    local_placement = ifcopenshell.util.placement.get_local_placement(space.ObjectPlacement)

    # Get the vertices of the space
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, space)
    geometry = shape.geometry
    vertices = ifcopenshell.util.shape.get_vertices(geometry)

    # Transform the vertices to the global coordinate system
    global_vertices = []
    for vertex in vertices:
        local_vertex = np.append(vertex, 1)  # Make it a homogenous coordinate for transformation
        global_vertex = local_placement @ local_vertex  # Apply the transformation
        global_vertices.append(global_vertex[:3])  # Extract the x, y, z coordinates

    return np.array(global_vertices)

# Get all spaces in the model
spaces = model.by_type("IfcSpace")

# Initialize lists to store all coordinates
all_coords = []

# Loop through all spaces and get their global vertices
for space in spaces:
    global_vertices = get_space_global_vertices(space)
    for vertex in global_vertices:
        all_coords.append({
            'SpaceName': space.Name,
            'X': vertex[0],
            'Y': vertex[1],
            'Z': vertex[2]
        })

# Convert the coordinates to a DataFrame
df = pd.DataFrame(all_coords)

# Export to CSV
output_csv_path = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\output\AC20-FZK-Haus_space_coordinates.csv'
df.to_csv(output_csv_path, index=False)

print(f"Coordinates exported to {output_csv_path}")
