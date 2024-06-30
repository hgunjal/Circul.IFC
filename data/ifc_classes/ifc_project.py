import ifcopenshell


class IfcProject:
    def __init__(self, file_path):
        self.ifc_file = ifcopenshell.open(file_path)
        self.schema = self.ifc_file.schema
        self.by_id = self.ifc_file.by_id
        #self.by_guid = self.by_guid
        self.walls = self._get_elements_by_type("IfcWall")
        self.doors = self._get_elements_by_type("IfcDoor")

    def _get_elements_by_type(self, ifc_type):
        return self.ifc_file.by_type(ifc_type)

    def get_all_walls(self):
        return self.ifc_file.by_type("IfcWall")

    def get_all_doors(self):
        return self.ifc_file.by_type("IfcDoor")

    def get_connects_path_elements(self):
        return self.ifc_file.by_type("IfcRelConnectsPathElements")

    def get_fills_elements(self):
        return self.ifc_file.by_type("IfcRelFillsElement")

    def get_voids_elements(self):
        return self.ifc_file.by_type("IfcRelVoidsElement")