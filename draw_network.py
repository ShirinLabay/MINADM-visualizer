import networkx as nx
import numpy as np
NODE_SIZE = 400

"""
    A file containing all drawing functions
    networkx library is used for drawing.
"""


def get_points(radius, number_of_points):
    radians_between_each_point = 2*np.pi / number_of_points
    list_of_points = []
    for p in range(0, number_of_points):
        list_of_points.append((radius*np.cos(p*radians_between_each_point), radius*np.sin(p*radians_between_each_point)) )
    return list_of_points


def convert_list_to_dict(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst)-1, 1)}
    return res_dct


def distance(x, y):
    if x >= y:
        result = x - y
    else:
        result = y - x
    return result


def transfer_lightpath_to_edge(lightpath):     # gets type Lightpath to [1, 2] format
    edge = [None, None]
    edge[0] = lightpath.start_node.node_id
    edge[1] = lightpath.end_node.node_id
    return edge


def draw_line_graph(number_of_nodes, ax):
    g = nx.path_graph(number_of_nodes, create_using=nx.Graph())
    pos = {}
    for i in range(number_of_nodes):
        pos[i] = [i, 0]
    node_options = {"edgecolors": "black", "node_size": NODE_SIZE, "alpha": 0.9}
    nx.draw_networkx_nodes(g, pos=pos, ax=ax, node_color="white", **node_options)
    nx.draw_networkx_labels(g, pos, ax=ax, font_size=14, font_color="black")
    nx.draw_networkx_edges(g, pos=pos, ax=ax, width=1, edge_color="black")
    fix_graph_scale(ax, pos, NODE_SIZE)
    return g, pos


def draw_circle_graph(number_of_nodes, ax1, user_or_optimal):
    g = nx.cycle_graph(number_of_nodes, create_using=nx.Graph())
    pos_ring = get_points(1, number_of_nodes)
    node_options = {"edgecolors": "black", "node_size": NODE_SIZE, "alpha": 0.9}
    nx.draw_networkx_nodes(g, pos=pos_ring, ax=ax1, node_color="white", **node_options)
    nodes = list()
    for i in range(number_of_nodes):
        nodes.append(i)
    edges_list = list()
    for i in range(number_of_nodes):
        if i == number_of_nodes - 1:
            edges_list.append([nodes[i], nodes[0]])
        else:
            edges_list.append([nodes[i], nodes[i+1]])
    nx.draw_networkx_labels(g, pos_ring, ax=ax1, font_size=14, font_color="black")
    nx.draw_networkx_edges(g, pos=pos_ring, ax=ax1, edgelist=edges_list, arrows=True, edge_color="black", arrowstyle='-',
                           width=1, connectionstyle="arc3,rad=0.2")
    pos_ring_dict = convert_list_to_dict(pos_ring)
    if user_or_optimal == 0:  # its optimal tab
        fix_graph_scale(ax1, pos_ring_dict, NODE_SIZE)
    if user_or_optimal == 1:  # its user tab
        fix_graph_scale_ring(ax1, pos_ring_dict, NODE_SIZE)
    return g, pos_ring


# ############################ building new circles(graphs) with different pos


def get_parts_reverse(edge, number_nodes):  # if number nodes = 5, gets [4,1] returns [[4,5],[5,0],[0,1]]
    list_parts = []
    first_node = edge[0]
    last_node = edge[1]
    list_tmp = []
    print("reverse")
    for i in range(0, number_nodes - first_node):
        list_tmp.append(i + first_node)
    print("tmp: ", list_tmp)
    for i in range(0, last_node + 1):
        list_tmp.append(i)
    print("tmp: ", list_tmp)
    for i, j in zip(list_tmp, list_tmp[1:]):
        list_parts.append([i, j])

    return list_parts


def get_parts(edge):  # gets [0,4] returns [[0,1],[1,2],[2,3],[3,4]]
    list_parts = []
    first_node = edge[0]
    last_node = edge[1]
    list_tmp = []
    for i in range(first_node, last_node + 1):
        list_tmp.append(i)
    for i, j in zip(list_tmp, list_tmp[1:]):
        list_parts.append([i, j])

    return list_parts


def get_g_and_pos_to_use(circle_number, number_nodes):
    g_new = nx.cycle_graph(number_nodes, create_using=nx.Graph())
    r = 1.2 + (circle_number - 1) * 0.2
    pos_new = get_points(r, number_nodes)

    return g_new, pos_new


def color_path_ring(g, ax, number_nodes, canvas, lightpath, edge, color1, circle_num):      # color1 is type Color
    if lightpath:   # not None
        edge = transfer_lightpath_to_edge(lightpath)
    color = color1
    g_to_use, pos_to_use = get_g_and_pos_to_use(circle_num, number_nodes)
    if edge[0] > edge[1]:
        list_parts_of_edges = get_parts_reverse(edge, number_nodes)
    else:
        list_parts_of_edges = get_parts(edge)
    g_to_use.add_edges_from(list_parts_of_edges)
    nodes_g = list()
    for i in range(len(list_parts_of_edges)):
        nodes_g.append(list_parts_of_edges[i][0])
        nodes_g.append(list_parts_of_edges[i][1])
    nodes_g.pop(0)
    nodes_g.pop()
    node_options = {"edgecolors": color, "node_size": 100, "alpha": 0.1}
    nx.draw_networkx_nodes(g_to_use, pos=pos_to_use, nodelist=nodes_g, ax=ax, node_color=color, **node_options)
    nx.draw_networkx(g_to_use, pos_to_use)
    nx.draw_networkx_edges(g_to_use, pos=pos_to_use, ax=ax, edgelist=list_parts_of_edges, arrows=True,
                           edge_color=color,
                           arrowstyle='-',
                           arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")
    canvas.draw()


def draw_paths_in_circle_user(g, ax, number_nodes, canvas, lightpath, circle_num):
    edge = lightpath
    g.add_edges_from([edge])
    gnew = nx.cycle_graph(number_nodes, create_using=nx.Graph())
    pos_ring = get_points(1, number_nodes)
    g_to_use, pos_to_use = get_g_and_pos_to_use(circle_num, number_nodes)

    if edge[0] > edge[1]:
        list_parts_of_edges = get_parts_reverse(edge, number_nodes)
    else:
        list_parts_of_edges = get_parts(edge)
    g_to_use.add_edges_from(list_parts_of_edges)

    nodes_g = list()
    for i in range(len(list_parts_of_edges)):
        nodes_g.append(list_parts_of_edges[i][0])
        nodes_g.append(list_parts_of_edges[i][1])
    nodes_g.pop(0)
    nodes_g.pop()
    node_options = {"edgecolors": "black", "node_size": 100, "alpha": 0.1}
    nx.draw_networkx_nodes(g_to_use, pos=pos_to_use, nodelist=nodes_g, ax=ax, node_color="black", **node_options)
    nx.draw_networkx(g_to_use, pos_to_use)
    nx.draw_networkx_edges(g_to_use, pos=pos_to_use, ax=ax, edgelist=list_parts_of_edges, arrows=True,
                           edge_color="black",
                           arrowstyle='-',
                           arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")
    pos_ring_dict = convert_list_to_dict(pos_ring)
    print("pos_ring_dict", pos_ring_dict)
    canvas.draw()


def color_paths_in_circle_optimal(ax):       # , canvas):
    gnew = nx.cycle_graph(10, create_using=nx.Graph())
    pos_ring = []
    pos_ring = get_points(1, 10)
    new_p = get_points(1.2, 10)
    new_p_2 = get_points(1.4, 10)
    edge_list = [[0, 1], [5, 6], [1, 2], [7, 8], [3, 4], [8, 9], [4, 6], [9, 0]]

    nx.draw_networkx_edges(gnew, pos=new_p, ax=ax, edgelist=[edge_list[0]], arrows=True, edge_color="#ff0000",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")

    nx.draw_networkx_edges(gnew, pos=new_p, ax=ax, edgelist=[edge_list[1]], arrows=True, edge_color="#009900",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")

    nx.draw_networkx_edges(gnew, pos=new_p, ax=ax, edgelist=[edge_list[2]], arrows=True, edge_color="#ff0000",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")

    nx.draw_networkx_edges(gnew, pos=new_p, ax=ax, edgelist=[edge_list[3]], arrows=True, edge_color="#ff0000",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")

    nx.draw_networkx_edges(gnew, pos=new_p, ax=ax, edgelist=[edge_list[4]], arrows=True, edge_color="#33ccff",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")

    nx.draw_networkx_edges(gnew, pos=new_p_2, ax=ax, edgelist=[edge_list[5]], arrows=True, edge_color="#ff0000",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")

    nodes_g = list()
    nodes_g.append(5)
    node_options = {"edgecolors": "#33ccff", "node_size": 100, "alpha": 0.1}
    nx.draw_networkx_nodes(gnew, pos=new_p_2, nodelist=nodes_g, ax=ax, node_color="#33ccff", **node_options)
    nodes_g.clear()
    nx.draw_networkx_edges(gnew, pos=new_p_2, ax=ax, edgelist=[[4, 5]], arrows=True, edge_color="#33ccff",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")
    nx.draw_networkx_edges(gnew, pos=new_p_2, ax=ax, edgelist=[[5, 6]], arrows=True, edge_color="#33ccff",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")

    nx.draw_networkx_edges(gnew, pos=new_p_2, ax=ax, edgelist=[edge_list[7]], arrows=True, edge_color="#ff0000",
                           arrowstyle='-', arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")
    # canvas.draw()


def draw_paths_in_circle(g, ax, number_nodes, canvas, lightpath, circlenumber, tab_num):
    if tab_num == 1:  # user
        edge = lightpath
    if tab_num == 2:  # optimal
        edge = transfer_lightpath_to_edge(lightpath)

    g.add_edges_from([edge])
    pos_ring = get_points(1, number_nodes)
    g_to_use, pos_to_use = get_g_and_pos_to_use(circlenumber, number_nodes)
    if edge[0] > edge[1]:
        list_parts_of_edges = get_parts_reverse(edge, number_nodes)
    else:
        list_parts_of_edges = get_parts(edge)
    g_to_use.add_edges_from(list_parts_of_edges)

    nodes_g = list()
    for i in range(len(list_parts_of_edges)):
        nodes_g.append(list_parts_of_edges[i][0])
        nodes_g.append(list_parts_of_edges[i][1])
    nodes_g.pop(0)
    nodes_g.pop()
    node_options = {"edgecolors": "black", "node_size": 100, "alpha": 0.1}
    nx.draw_networkx_nodes(g_to_use, pos=pos_to_use, nodelist=nodes_g, ax=ax, node_color="black", **node_options)
    nx.draw_networkx(g_to_use, pos_to_use)
    nx.draw_networkx_edges(g_to_use, pos=pos_to_use, ax=ax, edgelist=list_parts_of_edges, arrows=True,
                           edge_color="black",
                           arrowstyle='-',
                           arrowsize=30, width=2, connectionstyle="arc3,rad=0.2")
    pos_ring_dict = convert_list_to_dict(pos_ring)
    print("pos_ring_dict", pos_ring_dict)
    canvas.draw()


# ############################ building lines of paths for path topology


def draw_paths_above_in_path(g, ax, num, canvas, lightpath, path_num, tab_num):
    edge = []
    if tab_num == 1:
        edge = lightpath
    if tab_num == 2:
        edge = transfer_lightpath_to_edge(lightpath)

    g.add_edges_from([edge])
    gnew = nx.path_graph(num, create_using=nx.Graph())
    pos = {}
    pos_2 = {}
    pos_3 = {}
    pos_4 = {}
    pos_5 = {}
    pos_6 = {}
    pos_7 = {}
    pos_8 = {}
    pos_9 = {}
    pos_10 = {}
    pos_11 = {}
    pos_12 = {}
    pos_13 = {}
    pos_14 = {}
    for i in range(14):
        if tab_num == 1:
            pos[i] = [i, 0.05]
            pos_2[i] = [i, 0.1]
            pos_3[i] = [i, 0.15]
            pos_4[i] = [i, 0.2]
            pos_5[i] = [i, 0.25]
            pos_6[i] = [i, 0.3]
            pos_7[i] = [i, 0.35]
            pos_8[i] = [i, 0.4]
            pos_9[i] = [i, 0.45]
            pos_10[i] = [i, 0.5]
            pos_11[i] = [i, 0.55]
            pos_12[i] = [i, 0.6]
            pos_13[i] = [i, 0.65]
            pos_14[i] = [i, 0.7]
        else:       # tab2
            pos[i] = [i, 0.2]
            pos_2[i] = [i, 0.3]
            pos_3[i] = [i, 0.4]
            # the rest are not in use in tab2 in path. if they are then change it accordingly
            pos_4[i] = [i, 0.5]
            pos_5[i] = [i, 0.6]
            pos_6[i] = [i, 0.7]
            pos_7[i] = [i, 0.75]
            pos_8[i] = [i, 0.8]
            pos_9[i] = [i, 0.85]
            pos_10[i] = [i, 0.9]
            pos_11[i] = [i, 0.95]
            pos_12[i] = [i, 0.95]
            pos_13[i] = [i, 0.95]
            pos_14[i] = [i, 0.95]

    nx.draw_networkx(gnew, pos)
    if path_num == 1:
        pos_to_use = pos
    if path_num == 2:
        pos_to_use = pos_2
    if path_num == 3:
        pos_to_use = pos_3
    if path_num == 4:
        pos_to_use = pos_4
    if path_num == 5:
        pos_to_use = pos_5
    if path_num == 6:
        pos_to_use = pos_6
    if path_num == 7:
        pos_to_use = pos_7
    if path_num == 8:
        pos_to_use = pos_8
    if path_num == 9:
        pos_to_use = pos_9
    if path_num == 10:
        pos_to_use = pos_10
    if path_num == 11:
        pos_to_use = pos_11
    if path_num == 12:
        pos_to_use = pos_12
    if path_num == 13:
        pos_to_use = pos_13
    nx.draw_networkx_edges(gnew, pos=pos_to_use, ax=ax, edgelist=[edge], arrows=True, edge_color="black",
                           arrowstyle='-', arrowsize=30, width=2)
    # fix_graph_scale(ax, pos_to_use, NODE_SIZE)

    canvas.draw()


def color_paths_above(g, ax, canvas, lightpath, edge, color1, path_num):      # color1 is type Color
    if lightpath:   # not None
        edge = transfer_lightpath_to_edge(lightpath)
    # color = color1.get_color_string()
    color = color1
    pos = {}
    pos_2 = {}
    pos_3 = {}
    pos_4 = {}
    pos_5 = {}
    pos_6 = {}
    pos_7 = {}
    pos_8 = {}
    pos_9 = {}
    pos_10 = {}
    pos_11 = {}
    pos_12 = {}
    pos_13 = {}
    pos_14 = {}
    for i in range(14):
        pos[i] = [i, 0.05]
        pos_2[i] = [i, 0.1]
        pos_3[i] = [i, 0.15]
        pos_4[i] = [i, 0.2]
        pos_5[i] = [i, 0.25]
        pos_6[i] = [i, 0.3]
        pos_7[i] = [i, 0.35]
        pos_8[i] = [i, 0.4]
        pos_9[i] = [i, 0.45]
        pos_10[i] = [i, 0.5]
        pos_11[i] = [i, 0.55]
        pos_12[i] = [i, 0.6]
        pos_13[i] = [i, 0.65]
        pos_14[i] = [i, 0.7]

    if path_num == 1:
        pos_use = pos
    if path_num == 2:
        pos_use = pos_2
    if path_num == 3:
        pos_use = pos_3
    if path_num == 4:
        pos_use = pos_4
    if path_num == 5:
        pos_use = pos_5
    if path_num == 6:
        pos_use = pos_6
    if path_num == 7:
        pos_use = pos_7
    if path_num == 8:
        pos_use = pos_8
    if path_num == 9:
        pos_use = pos_9
    if path_num == 10:
        pos_use = pos_10
    if path_num == 11:
        pos_use = pos_11
    if path_num == 12:
        pos_use = pos_12
    if path_num == 13:
        pos_use = pos_13
    if path_num == 14:
        pos_use = pos_14
    nx.draw_networkx_edges(g, pos=pos_use, ax=ax, edgelist=[edge], arrows=True, edge_color=color,
                           arrowstyle='-', arrowsize=30, width=2)
    canvas.draw()


def color_paths_above_tab2(g, ax, canvas, lightpath, edge, color1, path_num):      # color1 is type Color
    if lightpath:   # not None
        edge = transfer_lightpath_to_edge(lightpath)
    # color = color1.get_color_string()
    color = color1
    pos = {}
    pos_2 = {}
    pos_3 = {}
    for i in range(10):
        pos[i] = [i, 0.2]
        pos_2[i] = [i, 0.3]
        pos_3[i] = [i, 0.4]

    if path_num == 1:
        pos_use = pos
    if path_num == 2:
        pos_use = pos_2
    if path_num == 3:
        pos_use = pos_3
    nx.draw_networkx_edges(g, pos=pos_use, ax=ax, edgelist=[edge], arrows=True, edge_color=color,
                           arrowstyle='-', arrowsize=30, width=2)
    canvas.draw()


def color_path_in_opt(ax, canvas):      # color1 is type Color
    gnew = nx.cycle_graph(10, create_using=nx.Graph())
    pos = {}
    pos_2 = {}
    pos_3 = {}
    for i in range(10):
        pos[i] = [i, 0.2]
        pos_2[i] = [i, 0.3]
        pos_3[i] = [i, 0.4]
    paths = [[0, 1], [2, 3], [5, 6], [1, 2], [1, 4], [3, 5]]
    red = "#ff0000"
    green = "#009900"
    nx.draw_networkx_edges(gnew, pos=pos, ax=ax, edgelist=[paths[0]], arrows=True, edge_color=red,
                           arrowstyle='-', arrowsize=30, width=2)
    nx.draw_networkx_edges(gnew, pos=pos, ax=ax, edgelist=[paths[1]], arrows=True, edge_color=red,
                           arrowstyle='-', arrowsize=30, width=2)
    nx.draw_networkx_edges(gnew, pos=pos, ax=ax, edgelist=[paths[2]], arrows=True, edge_color=red,
                           arrowstyle='-', arrowsize=30, width=2)
    nx.draw_networkx_edges(gnew, pos=pos, ax=ax, edgelist=[paths[3]], arrows=True, edge_color=red,
                           arrowstyle='-', arrowsize=30, width=2)
    nx.draw_networkx_edges(gnew, pos=pos_2, ax=ax, edgelist=[paths[4]], arrows=True, edge_color=green,
                           arrowstyle='-', arrowsize=30, width=2)
    nx.draw_networkx_edges(gnew, pos=pos_3, ax=ax, edgelist=[paths[5]], arrows=True, edge_color=red,
                           arrowstyle='-', arrowsize=30, width=2)
    canvas.draw()

# ############################


def get_ax_size_ring(a):  # used in fix_graph_scale
    bbox = a.get_window_extent().transformed(a.figure.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= 4.5
    height *= 15
    return width, height


def get_ax_size(a):  # used in fix_graph_scale
    bbox = a.get_window_extent().transformed(a.figure.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= 60
    height *= 60
    return width, height


def fix_graph_scale_ring(a, poss, node_size):  # to fit graph in the center of figure
    node_radius = (node_size / 3.14159265359) ** 0.5
    min_x = min(i_pos[0] for i_pos in poss.values())
    max_x = max(i_pos[0] for i_pos in poss.values())
    min_y = min(i_pos[1] for i_pos in poss.values())
    max_y = max(i_pos[1] for i_pos in poss.values())

    ax_size_x, ax_size_y = get_ax_size_ring(a)
    points_to_x_axis = (max_x - min_x) / (ax_size_x - node_radius * 2)
    points_to_y_axis = (max_y - min_y) / (ax_size_y - node_radius * 2)
    node_radius_in_x_axis = node_radius * points_to_x_axis
    node_radius_in_y_axis = node_radius * points_to_y_axis

    ax_min_x = min_x - node_radius_in_x_axis
    ax_max_x = max_x + node_radius_in_x_axis
    ax_min_y = min_y - node_radius_in_y_axis
    ax_max_y = max_y + node_radius_in_y_axis

    a.set_xlim([ax_min_x, ax_max_x])
    a.set_ylim([ax_min_y - 0.5, ax_max_y + 0.5])


def fix_graph_scale(a, poss, node_size):  # to fit graph in the center of figure
    node_radius = (node_size / 3.14159265359) ** 0.5
    min_x = min(i_pos[0] for i_pos in poss.values())
    max_x = max(i_pos[0] for i_pos in poss.values())
    min_y = min(i_pos[1] for i_pos in poss.values())
    max_y = max(i_pos[1] for i_pos in poss.values())

    ax_size_x, ax_size_y = get_ax_size(a)
    points_to_x_axis = (max_x - min_x) / (ax_size_x - node_radius * 2)
    points_to_y_axis = (max_y - min_y) / (ax_size_y - node_radius * 2)
    node_radius_in_x_axis = node_radius * points_to_x_axis
    node_radius_in_y_axis = node_radius * points_to_y_axis

    ax_min_x = min_x - node_radius_in_x_axis
    ax_max_x = max_x + node_radius_in_x_axis
    ax_min_y = min_y - node_radius_in_y_axis
    ax_max_y = max_y + node_radius_in_y_axis

    a.set_xlim([ax_min_x, ax_max_x])
    a.set_ylim([ax_min_y - 0.5, ax_max_y + 0.5])
