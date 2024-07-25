import ifcopenshell.util.shape
import ifcopenshell.util.placement
import ifcopenshell.util.element
import numpy as np
class IfcElement:
    def __init__(self, ifc_element):
        self.ifc_element = ifc_element
        self.id = ifc_element.id()
        self.Name = ifc_element.Name
        self.GlobalId = ifc_element.GlobalId

    def get_vertices(self, geometry):
        return ifcopenshell.util.shape.get_vertices(geometry)

    def get_bbox(self, vertices):
        vertices = np.array(vertices)
        min_coords = np.min(vertices, axis=0)
        max_coords = np.max(vertices, axis=0)
        return min_coords, max_coords

    def get_local_placement(self):
        return ifcopenshell.util.placement.get_local_placement(self.ifc_element.ObjectPlacement)

    def get_storey_elevation(self):
        container = ifcopenshell.util.element.get_container(self.ifc_element)
        while container:
            if container.is_a('IfcBuildingStorey'):
                return container.Elevation
            container = ifcopenshell.util.element.get_container(container)
        return None

    def get_container_name(self):
        container = ifcopenshell.util.element.get_container(self.ifc_element)
        return container.Name if container else 'Unknown'
