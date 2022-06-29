import Color
from Node import *
import random
from Color import *

'''
    list_edges gets 0,4 and returns [[0,1], [1,2], [2,3], [3,4]].
    is_conflicting checks if path1 and path2 share an edge.
    conflicting_paths returns list of conflicting paths to a given path in a given network.
    generate_new_color generates new color.
    is_adm_available_at_other_endpoint checks if we have a free ADM at other endpoint.
    get_usable_adms returns list of usable adms for path.
    color_lightpath returns the color that was used. this is the algorithm minADM.
'''


def list_edges(path, nodes):   # gets 0,4 and returns [[0,1], [1,2], [2,3], [3,4]]
    path_edges = []
    first_node = path.get_start_node().get_node_id()
    last_node = path.get_end_node().get_node_id()
    list_tmp = []
    if first_node < last_node:
        for i in range(first_node, last_node + 1):
            list_tmp.append(i)
        for i, j in zip(list_tmp, list_tmp[1:]):
            path_edges.append([i, j])

    if first_node > last_node:
        for i in range(0, nodes - first_node):
            list_tmp.append(i + first_node)
        print("tmp: ", list_tmp)
        for i in range(0, last_node + 1):
            list_tmp.append(i)
        print("tmp: ", list_tmp)
        for i, j in zip(list_tmp, list_tmp[1:]):
            path_edges.append([i, j])

    return path_edges


def is_conflicting(path1, path2, nodes):  # check if path1 and path2 share an edge
    le1 = list_edges(path1, nodes)
    le2 = list_edges(path2, nodes)
    for x in le1:
        for y in le2:
            if x == y:
                return True
    return False


def conflicting_paths(path, network, nodes):
    all_paths = network.lightpaths_list.copy()
    all_paths.remove(path)  # remove this lightpath from all paths list
    list_conflicting = []
    for p in all_paths:
        if is_conflicting(path, p, nodes):
            list_conflicting.append(p)
    return list_conflicting


def generate_new_color(from_colors_list, network):   # returns a color that was never used
    color = None
    if from_colors_list:    # if true then return the next color in colors list
        return network.get_color_from_list()        # not random
    else:   # false = generate random color. used when optimal solution not shown
        change = True
        while change:
            r_dec = random.randint(0, 16777215)
            rgb_hex = str(hex(r_dec))
            rgb_hex = '#'+rgb_hex[2:]
            color = Color(rgb_hex)
            if color in network.used_random_colors:     # this random color is already in use
                change = True
            else:
                change = False
        network.add_used_random_color(color)
    return color


def is_adm_available_at_other_endpoint(adms_at_endpoint, color):  # true if adm at endpoint this color is usable
    for a in adms_at_endpoint:
        if a.get_color() == color:
            return a
    return None


def delete_conflicting_colors(adms, lightpath, network, nodes):
    list1 = adms.copy()
    final_list = []
    flag = 0
    list_conflicting = conflicting_paths(lightpath, network, nodes)
    for adm in list1:
        flag = 0
        color_of_adm = adm.get_color()
        for p in list_conflicting:
            if p.lightpath_color == color_of_adm:
                flag = 1
        if flag == 0:
            final_list.append(adm)
    return final_list


def get_usable_adms(adms, path, network, nodes):      # returns list of usable adms for path
    if adms:
        adms = delete_conflicting_colors(adms, path, network, nodes)
    return adms


def use_adm(node, adm, lightpath, first_or_last, new_adm, network):
    node.add_adm(adm)
    if first_or_last == "f":
        lightpath.set_first_adm(adm)
    else:
        lightpath.set_last_adm(adm)
    if not new_adm:
        # not new adm, inc its connected paths
        adm.inc_connected()
    else:
        network.add_adm_to_list(adm)


def color_lightpath(lightpath, nodes, color_not_random, network):        # returns the color that was used
    # if color_not_random is true then use the color array in Color. if false then use the generator
    first = lightpath.get_start_node()
    last = lightpath.get_end_node()
    adms_at_endpoint1 = Node.get_adms(first)
    adms_at_endpoint2 = Node.get_adms(last)

    usable_adms_endpoint1 = get_usable_adms(adms_at_endpoint1, lightpath, network, nodes)
    usable_adms_endpoint2 = get_usable_adms(adms_at_endpoint2, lightpath, network, nodes)

    if not usable_adms_endpoint1 and not usable_adms_endpoint2:
        new_color = generate_new_color(color_not_random, network)
        lightpath.set_color_path(new_color)
        # add adm with this color at each endpoint of path
        adm1 = Adm(new_color, first, network.get_adm_id_to_use())
        use_adm(first, adm1, lightpath, "f", True, network)
        adm2 = Adm(new_color, last, network.get_adm_id_to_use())
        use_adm(last, adm2, lightpath, "l", True, network)
        # draw path again with new color in path_topology_tab1 file
        return new_color

    if usable_adms_endpoint1:
        # there is at least one usable adm at endpoint1
        a = usable_adms_endpoint1[0]    # adm to use at endpoint1
        color = a.get_color()
        lightpath.set_color_path(color)
        use_adm(first, a, lightpath, "f", False, network)

        # check if there is an adm at endpoint2 with same color
        if usable_adms_endpoint2:
            # there is at least one usable adm at endpoint2. check if it has the same color
            for adm in usable_adms_endpoint2:
                if adm.get_color() == color:
                    # same color -> use this adm
                    use_adm(last, adm, lightpath, "l", False, network)
                    return color
        # if it got here - no usable adms at endpoint2 -> need to make new adm
        new_adm = Adm(color, last, network.get_adm_id_to_use())
        use_adm(last, new_adm, lightpath, "l", True, network)
        return color

    if usable_adms_endpoint2:
        a = usable_adms_endpoint2[0]  # adm to use at endpoint2
        color = a.get_color()
        lightpath.set_color_path(color)
        use_adm(last, a, lightpath, "l", False, network)

        if usable_adms_endpoint1:
            for adm in usable_adms_endpoint1:
                if adm.get_color() == color:
                    # use this adm
                    use_adm(first, adm, lightpath, "f", False, network)
                    return color
        new_adm = Adm(color, first, network.get_adm_id_to_use())
        use_adm(first, new_adm, lightpath, "f", True, network)
        return color