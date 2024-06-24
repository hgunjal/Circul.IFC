from ifc_element import IfcElement

class IfcDoor(IfcElement):
    def __init__(self, ifc_element):
        super().__init__(ifc_element)
        self.location = self._get_location()

    def _get_location(self):
        # Method to find the location of the door
        pass
