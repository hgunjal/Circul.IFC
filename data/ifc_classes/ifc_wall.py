from ifc_element import IfcElement

class IfcWall(IfcElement):
    def __init__(self, ifc_element):
        super().__init__(ifc_element)
        self.start_point = self._get_start_point()

    def _get_start_point(self):
        # Method to find the start point of the wall
        pass
