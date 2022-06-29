"""
    A class for representing an ADM object
    properties - id, color of ADM, number of paths that are connected to this ADM, and the node where the ADM is
    is_free gives us an update if the ADM is free, i.e. if it does not have more than 2 connections.
    get_color returns the color of the ADM.
    inc_connected adds 1 to the number of connected paths
    get_adm_index returns the id of the ADM
    get_number_of_adms_used returns the number of ADMs
"""


class Adm:

    def __init__(self, color, node, idd):
        self.adm_id = idd
        self.adm_color = color
        self.connected_paths = 1
        self.node = node

    def is_free(self):
        if self.connected_paths == 2:
            return False
        else:
            return True

    def get_color(self):
        return self.adm_color

    def inc_connected(self):
        self.connected_paths = self.connected_paths + 1

    def get_adm_index(self):
        return self.adm_id

    def get_number_of_adms_used(self):
        return self.index_adms + 1
