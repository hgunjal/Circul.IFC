import ifcopenshell
import json
import os

# Load the IFC file
file_path = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\models\AC20-FZK-Haus.ifc'
model = ifcopenshell.open(file_path)

# Output path
output_dir = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\output'
model_name = os.path.splitext(os.path.basename(file_path))[0]
output_file = os.path.join(output_dir, f"{model_name}_space_boundaries.json")
output_file_new = os.path.join(output_dir, f"{model_name}_space_name_mapping.json")

# Function to get IfcRelSpaceBoundary info as a dictionary
def get_ifc_rel_space_boundary_info(rel_space_boundary):
    info = {
        "Related_Building_Element_Name": rel_space_boundary.RelatedBuildingElement.Name if rel_space_boundary.RelatedBuildingElement else None,
        "Related_Building_Element_GlobalID": rel_space_boundary.RelatedBuildingElement.GlobalId if rel_space_boundary.RelatedBuildingElement else None,
        "Related_Building_Element_IFC_Type": rel_space_boundary.RelatedBuildingElement.is_a() if rel_space_boundary.RelatedBuildingElement else None,
    }
    # Add LongName only if it exists
    if rel_space_boundary.RelatedBuildingElement and hasattr(rel_space_boundary.RelatedBuildingElement, 'LongName'):
        info["Related_Building_Element_LongName"] = rel_space_boundary.RelatedBuildingElement.LongName
    return info

# Function to create a dictionary mapping space.Name to space.LongName
def get_space_name_to_long_name_dict(spaces):
    name_longname_dict = {}
    for space in spaces:
        name_longname_dict[space.Name] = space.LongName if hasattr(space, 'LongName') else None
    return name_longname_dict

# Create a dictionary to store the information
spaces_info = {}

spaces = model.by_type("IfcSpace")

# Iterate through each space and collect its IfcRelSpaceBoundary relationships
for space in spaces:
    space_key = space.Name
    spaces_info[space_key] = []
    if hasattr(space, "BoundedBy"):
        for rel_space_boundary in space.BoundedBy:
            element = rel_space_boundary.RelatedBuildingElement
            if element and element.is_a("IfcDoor"):
                spaces_info[space_key].append(get_ifc_rel_space_boundary_info(rel_space_boundary))
        # If no IfcRelSpaceBoundary relationships are found, append a placeholder message
        if not spaces_info[space_key]:
            spaces_info[space_key].append("No IfcRelSpaceBoundary relationships.")

space_name_mapping = get_space_name_to_long_name_dict(spaces)
print(space_name_mapping)

# Save the dictionary as a JSON file
with open(output_file_new, 'w') as json_file:
    json.dump(space_name_mapping, json_file, indent=4)

# # Save the dictionary as a JSON file
# with open(output_file, 'w') as json_file:
#     json.dump(spaces_info, json_file, indent=4)
#
# print(f"Space boundary information has been saved to {output_file}")
