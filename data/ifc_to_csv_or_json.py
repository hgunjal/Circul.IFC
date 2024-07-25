import csv
import os
import json
import numpy as np
import pandas as pd
from ifc_classes.ifc_project import IfcProject
from ifc_classes.ifc_wall import IfcWall
from ifc_classes.ifc_opening import IfcOpeningElement
from ifc_classes.ifc_space import IfcSpace
from ifc_classes.adj_space import IfcGeometry

def wall_prop_to_csv(file_path, output_csv_path):
    """
        Extracts wall properties from an IFC file and writes them to a CSV file.

        Args:
            ifc_file_path (str): Path to the IFC file.
            output_csv_path (str): Path to the output CSV file.
        """
    model = IfcProject(file_path)

    # Extract model name from the file path
    model_name, _ = os.path.splitext(os.path.basename(ifc_file_path))

    # Construct output CSV path with model name
    output_csv_path = os.path.join(output_dir, f"{model_name}_wall_info.csv")

    # Get all walls
    walls = model.walls
    wall_data = []

    for w in walls:
        ifc_wall = IfcWall(w)
        wall_prop = ifc_wall.get_bounding_box_data()
        wall_data.append(wall_prop)

    # Check if wall data is not empty to avoid creating an empty DataFrame
    if wall_data:
        # Create a pandas DataFrame from the list of wall properties
        df = pd.DataFrame(wall_data)

        # Optionally, save the DataFrame to a CSV file (modified to avoid hardcoded filename)
        df.to_csv(output_csv_path, index=False)

        print(f"Successfully exported wall data to {output_csv_path}")
    else:
        print("No walls found in the IFC file. Skipping CSV generation.")

def opening_prop_to_csv(ifc_file_path, output_csv_path):
    # Initialize the project with the IFC file path
    project = IfcProject(ifc_file_path)

    # Extract model name from the file path
    model_name, _ = os.path.splitext(os.path.basename(ifc_file_path))

    # Construct output CSV path with model name
    output_csv_path = os.path.join(output_dir, f"{model_name}_opening_info.csv")

    # Collect data for all openings
    openings_data_list = []

    for wall in project.walls:
        wall_element = IfcWall(wall)
        wall_data = wall_element.get_bounding_box_data()

        print(f"Checking wall: {wall.Name} (GlobalId: {wall.GlobalId})")

        # Find related openings using IfcRelVoidsElement relationships
        voids_elements = project._get_elements_by_type("IfcRelVoidsElement")
        openings_in_wall = [rel.RelatedOpeningElement for rel in voids_elements if rel.RelatingBuildingElement == wall]

        # Check if any openings are found
        if openings_in_wall:
            print(f" - Found openings: ")
            for opening in openings_in_wall:
                print(f"  - Opening Element: {opening.Name} {opening.GlobalId}")
                opening_processor = IfcOpeningElement(opening)
                opening_bounding_box_data = opening_processor.get_bounding_box_data()
                print(opening_bounding_box_data)
                # Combine wall data and opening data
                opening_data = {
                    'WallName': wall.Name,
                    'WallGlobalId': wall.GlobalId,
                    **opening_bounding_box_data
                }
                print(opening_data)
                openings_data_list.append(opening_data)
        else:
            print(f" - No openings found for this wall.")

        # Check if wall data is not empty to avoid creating an empty DataFrame
        if openings_data_list:
            # Create a pandas DataFrame from the list of wall properties
            df = pd.DataFrame(openings_data_list)

            # Optionally, save the DataFrame to a CSV file (modified to avoid hardcoded filename)
            df.to_csv(output_csv_path, index=False)

            print(f"Successfully exported wall data to {output_csv_path}")
        else:
            print("No openings found in the IFC file. Skipping CSV generation.")

def get_space_wall_relations(file_path, output_dir):
    model = IfcProject(file_path)
    # Extract model name from the IFC file path
    model_name, _ = os.path.splitext(os.path.basename(file_path))
    # Construct the output JSON file path
    output_json_path = os.path.join(output_dir, f"{model_name}_space_wall_relation.json")
    spaces = model.ifc_file.by_type("IfcSpace")
    individual_instances_of_space_list = [IfcSpace(s) for s in spaces]
    space_wall_mapping = {}
    for s in individual_instances_of_space_list:
        walls_in_space = s.get_adjoining_walls_in_space()
        if walls_in_space:
            space_wall_mapping[s.GlobalId] = [wall for wall in walls_in_space if wall not in space_wall_mapping.get(s.Name, [])]
    # Write the space_wall_mapping dictionary to a JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(space_wall_mapping, json_file, indent=4)

    print(f"Successfully exported space-wall relations to {output_json_path}")

def get_space_door_relations(file_path, output_dir):
    model = IfcProject(file_path)
    # Extract model name from the IFC file path
    model_name, _ = os.path.splitext(os.path.basename(file_path))
    # Construct the output JSON file path
    output_json_path = os.path.join(output_dir, f"{model_name}_space_door_relation.json")
    spaces = model.ifc_file.by_type("IfcSpace")
    individual_instances_of_space_list = [IfcSpace(s) for s in spaces]
    space_door_mapping = {}
    for s in individual_instances_of_space_list:
        doors_in_space = s.get_adjoining_doors_in_space()
        if doors_in_space:
            space_door_mapping[s.GlobalId] = [door for door in doors_in_space if door not in space_door_mapping.get(s.Name, [])]
    # Write the space_door_mapping dictionary to a JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(space_door_mapping, json_file, indent=4)

    print(f"Successfully exported space-door relations to {output_json_path}")

def get_space_opening_relations(file_path, output_dir):
    model = IfcProject(file_path)
    # Extract model name from the IFC file path
    model_name, _ = os.path.splitext(os.path.basename(file_path))
    # Construct the output JSON file path
    output_json_path = os.path.join(output_dir, f"{model_name}_space_opening_relation.json")
    spaces = model.ifc_file.by_type("IfcSpace")
    individual_instances_of_space_list = [IfcSpace(s) for s in spaces]
    space_opening_mapping = {}
    for s in individual_instances_of_space_list:
        openings_in_space = s.get_adjoining_openings_in_space()
        if openings_in_space:
            space_opening_mapping[s.GlobalId] = [opening for opening in openings_in_space if opening not in space_opening_mapping.get(s.Name, [])]
    # Write the space_opening_mapping dictionary to a JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(space_opening_mapping, json_file, indent=4)

    print(f"Successfully exported space-opening relations to {output_json_path}")

def filter_by_storey(dict1, dict2):
    dict3 = {}
    for key, adjacents in dict1.items():
        storey = dict2[key]
        filtered_adjacents = [adj for adj in adjacents if dict2[adj] == storey]
        if filtered_adjacents:  # Only add the key if there are filtered adjacents
            dict3[key] = filtered_adjacents
    return dict3

def get_space_to_space_relations(file_path, output_dir):
    model = IfcProject(file_path)
    # Extract model name from the IFC file path
    model_name, _ = os.path.splitext(os.path.basename(file_path))
    # Construct the output JSON file path
    output_json_path = os.path.join(output_dir, f"{model_name}_adjacent_space_relation.json")
    project_name = "test"
    ifc_geometry = IfcGeometry(file_path, project_name, force_init=False)
    adjacent_spaces_dict = ifc_geometry.get_adjacent_spaces_dict()
    space_storey_dict = ifc_geometry.get_space_storey_dict()
    space_adj_dict = filter_by_storey(adjacent_spaces_dict, space_storey_dict)
    # Write the space_opening_mapping dictionary to a JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(space_adj_dict, json_file, indent=4)
    print(f"Successfully exported space-opening relations to {output_json_path}")


if __name__ == "__main__":
    # Replace these paths with your actual file paths
    ifc_file_path = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\models\AC20-FZK-Haus.ifc'
    ifc_file_path = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\models\TUM_Gebaude N6_IFC4.ifc'
    output_dir = r'C:\Users\harsh\Documents\Master Thesis\ifc_processing\Circul.IFC\output'

    # wall_prop_to_csv(ifc_file_path, output_dir) #shift all these variables to main file
    # opening_prop_to_csv(ifc_file_path, output_dir)

    get_space_door_relations(ifc_file_path, output_dir)
    get_space_wall_relations(ifc_file_path, output_dir)
    get_space_opening_relations(ifc_file_path, output_dir)
    get_space_to_space_relations(ifc_file_path, output_dir)