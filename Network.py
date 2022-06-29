from Node import *
from Lightpath import *

'''
    Network class
    contains all the information needed for running the algorithm in the network
    id for lightpath tracks the number of existing paths, every time a new lightpaths is created the id is incremented
    index path and colored are for tracking which path is already drawn and colored in the visualization tab (tab2)
    colors_list is created for the visualization in tab2 where the algorithm is compared to the optimal solution 
        to make sure that the same colors are used - this enables the user to truly see the difference
    in tab1 where the user draws a network as he wants - the colors of the paths are generated randomly and are saved
        in used_random_colors to make sure the same color is not generated randomly twice
'''


class Network:

    def __init__(self, typeof, number_nodes):
        self.network_edges = []
        self.lightpaths_list = []
        self.id_for_lightpath = 0
        self.adms_list = []
        self.id_for_adm = -1
        self.index_path = 0         # index of path in lightpaths list. incremented after coloring in Algorithm_minadm
        self.colored = False        # True when path in Index is colored. change to true in function
        self.type = typeof          # type can be "path" or "ring"
        self.nodes_list = []
        for i in range(number_nodes):       # if num = 5 then I is from 0 to 4
            n = Node(i)
            self.nodes_list.append(n)
            if typeof == "path":
                if i < number_nodes-1:      # for path connect 0-1, 1-2, 2-3, 3-4
                    self.network_edges.append([i, i+1])
            elif typeof == "ring":
                if i < number_nodes-1:      # for ring connect 0-1, 1-2, 2-3, 3-4, 4-0. 4-0 connected in line 27
                    self.network_edges.append([i, i + 1])
            else:
                print("general network")
        if typeof == "ring":
            self.network_edges.append([number_nodes-1, 0])

        self.colors_list = [
            "#ff0000",  # red
            "#009900",  # green
            "#ff9900",  # orange
            "#33ccff",  # light blue
            "#996633",  # brown
            "#cc66ff",  # light purple
            "#ff3399",  # pink
            "#66ff33",  # light green
            "#0000ff",  # blue
            "#9900ff",  # purple
            "#b32d00",  # dark red
            "#ffff00",  # yellow
        ]
        self.index_in_colors_list = 0
        self.used_random_colors = []

    def get_color_from_list(self):
        if self.index_in_colors_list == len(self.colors_list):
            Exception("add more colors to colors list")
        next_color = self.colors_list[self.index_in_colors_list]
        self.index_in_colors_list = self.index_in_colors_list + 1
        return next_color

    def add_used_random_color(self, color):
        self.used_random_colors.append(color)

    def add_adm_to_list(self, adm):
        self.adms_list.append(adm)

    def get_adm_id_to_use(self):
        self.id_for_adm = self.id_for_adm + 1
        return self.id_for_adm

    def inc_index_in_paths_in_network(self):
        self.index_path = self.index_path + 1
        self.colored = False

    def find_node(self, index):
        for n in self.nodes_list:
            if n.get_node_id() == index:
                return n

    def add_paths_to_network(self, lightpath):     # gets list like [[0, 1], [2, 3], [5, 6], [1, 2], [2, 5], [3, 5]]
        # and adds to list of lightpaths
        for path in lightpath:
            # for [1, 2] find nodes with index 1 and 2 and create new Lightpath with it
            start_node = self.find_node(path[0])
            end_node = self.find_node(path[1])
            if not start_node or not end_node:
                Exception("Node does not exist")
            else:
                new_lightpath = Lightpath(start_node, end_node, self.id_for_lightpath)
                self.id_for_lightpath = self.id_for_lightpath + 1
                self.lightpaths_list.append(new_lightpath)

    def colored_true(self):
        self.colored = True

    def add_node_to_network(self, node):
        self.nodes_list.append(node)

    def get_lightpaths(self):
        return self.lightpaths_list

    def get_index(self):
        return self.index_path

    def get_len_lightpaths_list(self):
        return len(self.lightpaths_list)

    def get_type(self):
        return self.type

    def reset_network(self):
        self.index_in_colors_list = 0
        self.used_random_colors = []
        self.network_edges = []
        self.lightpaths_list = []
        self.id_for_lightpath = 0
        # self.index_ring = 0
        self.index_path = 0  # index of path in lightpaths list. incremented after coloring in Algorithm_minadm
        self.colored = False  # True when path in Index is colored. change to true in function
        self.type = None  # type can be "path" or "ring"
        self.nodes_list = []
        self.adms_list = []
        self.id_for_adm = -1
