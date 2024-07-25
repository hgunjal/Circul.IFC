import ifcopenshell.geom
import ifcopenshell.util.shape
from .ifc_element import IfcElement
import numpy as np


class IfcSpace(IfcElement):
    def __init__(self, element):
        super().__init__(element)
        self.LongName = element.LongName if hasattr(element,
                                                    'LongName') else None  # Long name of the space, if it exists

    def get_adjoining_walls_in_space(self):
        boundaries = []
        if hasattr(self.ifc_element, "BoundedBy"):
            for rel_space_boundary in self.ifc_element.BoundedBy:
                element = rel_space_boundary.RelatedBuildingElement
                if element and element.is_a("IfcWall"):
                    wall_info = self.get_ifc_rel_space_boundary_info(rel_space_boundary)
                    if wall_info not in boundaries:  # Avoid appending duplicates
                        boundaries.append(wall_info)
        # If no IfcRelSpaceBoundary relationships are found, append a placeholder message
        if not boundaries:
            boundaries.append("No IfcRelSpaceBoundary relationships.")
        return boundaries

    def get_adjoining_doors_in_space(self):
        boundaries = []
        if hasattr(self.ifc_element, "BoundedBy"):
            for rel_space_boundary in self.ifc_element.BoundedBy:
                element = rel_space_boundary.RelatedBuildingElement
                if element and element.is_a("IfcDoor"):
                    door_info = self.get_ifc_rel_space_boundary_info(rel_space_boundary)
                    if door_info not in boundaries:  # Avoid appending duplicates
                        boundaries.append(door_info)
        # If no IfcRelSpaceBoundary relationships are found, append a placeholder message
        if not boundaries:
            boundaries.append("No IfcRelSpaceBoundary relationships.")
        return boundaries

    def get_adjoining_openings_in_space(self):
        boundaries = []
        if hasattr(self.ifc_element, "BoundedBy"):
            for rel_space_boundary in self.ifc_element.BoundedBy:
                element = rel_space_boundary.RelatedBuildingElement
                if element and element.is_a("IfcOpeningElement"):
                    opening_info = self.get_ifc_rel_space_boundary_info(rel_space_boundary)
                    if opening_info not in boundaries:  # Avoid appending duplicates
                        boundaries.append(opening_info)
        # If no IfcRelSpaceBoundary relationships are found, append a placeholder message
        if not boundaries:
            boundaries.append("No IfcRelSpaceBoundary relationships.")
        return boundaries

    @staticmethod
    def get_ifc_rel_space_boundary_info(rel_space_boundary):
        info = {
            "Element Name": rel_space_boundary.RelatedBuildingElement.Name if rel_space_boundary.RelatedBuildingElement else None,
            "Element GlobalID": rel_space_boundary.RelatedBuildingElement.GlobalId if rel_space_boundary.RelatedBuildingElement else None,
        }
        return info