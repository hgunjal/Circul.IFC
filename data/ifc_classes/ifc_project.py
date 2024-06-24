import ifcopenshell


class IfcProject:
    def __init__(self, file_path):
        self.ifc_file = ifcopenshell.open(file_path)
        self.schema = self.ifc_file.schema
        self.by_id = self.ifc_file.by_id
        self.by_guid = self.by_guid
        self.walls = self._get_elements_by_type("IfcWall")
        self.doors = self._get_elements_by_type("IfcDoor")

    def _get_elements_by_type(self, ifc_type):
        return self.ifc_file.by_type(ifc_type)
