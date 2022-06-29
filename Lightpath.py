"""
    Lightpath class
    properties - start and end node of the lightpath (a simple path in the network)
               - id
               - color
               - first and last ADM that the lightpath is connected to
"""


class Lightpath:

    def __init__(self, start_node, end_node, idd):
        self.start_node = start_node
        self.end_node = end_node
        self.lightpath_id = idd
        self.lightpath_color = "black"
        self.first_adm = None
        self.last_adm = None

    def get_start_node(self):
        return self.start_node

    def get_end_node(self):
        return self.end_node

    def get_color(self):
        if self.lightpath_color == "black":
            return "black - not colored yet"
        return self.lightpath_color.get_color_string()

    def set_color_path(self, color):
        self.lightpath_color = color

    def set_first_adm(self, first_adm):
        self.first_adm = first_adm

    def set_last_adm(self, last_adm):
        self.last_adm = last_adm
