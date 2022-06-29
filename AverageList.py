"""
    This class is used in average_analysis file to track the results that were generated in tab 3
    and to track the average ratio in both topologies
"""


class AverageList:

    def __init__(self):
        self.l_path = []
        self.l_ring = []
        self.avg_ratio_path = 0         # to display as label in tab 3
        self.avg__ratio_ring = 0

    def add_to_list(self, element, topology):
        if topology == 'path':
            list_r = self.l_path
        else:
            list_r = self.l_ring
        if element not in list_r:
            list_r.append(element)

    def set_avg_ratio(self, topology, avg_ratio):
        if topology == "path":
            self.avg_ratio_path = avg_ratio
        else:
            self.avg__ratio_ring = avg_ratio

    def get_avg_ratio(self, topology):
        if topology == "path":
            return self.avg_ratio_path
        else:
            return self.avg__ratio_ring

    def get_list(self, topology):
        if topology == 'path':
            return self.l_path
        else:
            return self.l_ring

    def get_len(self, topology):
        if topology == 'path':
            return len(self.l_path)
        else:
            return len(self.l_ring)

    def reset_list(self, topology):
        if topology == 'path':
            self.l_path = []
            self.avg_path = 0
        else:
            self.l_ring = []
            self.avg_ring = 0
