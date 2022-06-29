from Adm import *

'''
    Node class with an id, and a list of ADMs that are in this node
    exist_adm_at_node method returns true if there is at least one ADM in this node
    get_adms returns the list of ADMs we have at this node.
'''


class Node:

    def __init__(self, idd):
        self.node_id = idd
        self.node_neighbors = []        # not in use yet
        self.node_adms = []

    def exist_adm_at_node(self):
        if not self.node_adms:
            # no adm at this node
            return False
        else:
            return True

    def get_adms(self):      # returns a list of free adms of this node
        adms = []
        if not self.node_adms:
            #  no adm at all in this node
            return adms
        for adm in self.node_adms:
            if Adm.is_free(adm):
                adms.append(adm)
        return adms

    def add_neighbor(self, neighbor):
        self.node_neighbors.append(neighbor)

    def add_adm(self, adm):
        self.node_adms.append(adm)

    def get_node_id(self):
        return self.node_id
