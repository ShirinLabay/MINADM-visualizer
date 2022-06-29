# write to network files 300 permutations for each network
from algorithm_minadm import *
import math
import copy
import algorithm_minadm
from Network import *


'''
functions for running larger networks. results are written in "p_statistics1.txt" and "r_statistics1.txt" 
In the statistics files each row represents topology\\num_nodes\\num_paths\\avg_adms\\optimum\\ratio
'''


def write_to_statistics_file(topology, num_nodes, num_paths, optimum, avg_solution):
    if topology == 'path':
        file = 'networks_txt/path/p_statistics1.txt'
    else:
        file = 'networks_txt/ring/r_statistics1.txt'
    try:
        f_write = open(file, 'a')
    except IOError:
        print("Error - Could not open file!")
        return -1
    ratio = (avg_solution / optimum)
    ratio = round(ratio, 2)     # keep only 2 digits after point
    if topology == 'path':
        if ratio > 3/2:
            Exception("ERROR - Ratio is", str(ratio), "but cannot be grater than 3/2")
            return -1
    if topology == 'ring':
        if ratio > 7/4:
            Exception("ERROR - Ratio is", str(ratio), "but cannot be grater than 7/4")
            return -1
    line = "\n" + str(topology) + "\\" + str(num_nodes) + "\\" + str(num_paths) + "\\" + str(avg_solution) \
           + "\\" + str(optimum) + "\\" + str(ratio)
    f_write.write(line)
    return ratio


def color_all_paths(number_nodes, paths):
    network = Network("path", number_nodes)
    network.add_paths_to_network(paths)
    # iterate through lightpaths and color them one by one

    for path in network.get_lightpaths():
        color = algorithm_minadm.color_lightpath(path, nodes=number_nodes, color_not_random=False, network=network)
        print("colored path", path.get_start_node().get_node_id(), ",", path.get_end_node().get_node_id(), "in",
              color.get_color_string(), ". Number of adms so far is - ", len(network.adms_list))
    num_adms = len(network.adms_list)
    print('\ndone network\n\n')
    network.reset_network()

    return num_adms


def run_all_permutations(list_to_shuffle, topology, num_nodes, num_paths, optimum):
    # shuffle the list 300 times
    # run every permutation
    # write avg ADMs in statistics file
    list_result_adms = []

    for i in range(0, 300):
        random.shuffle(list_to_shuffle)
        list_result_adms = []
        num_adms = color_all_paths(num_nodes, list_to_shuffle)
        if num_adms < optimum:
            Exception("Something went wrong! number of ADMs used- ", str(num_adms), "cannot be less than the optimal- ",
                      str(optimum))
            return -1
        list_result_adms.append(num_adms)

    avg_adms = math.ceil(sum(list_result_adms) / len(list_result_adms))
    ratio = write_to_statistics_file(topology, num_nodes, num_paths, optimum, avg_adms)
    return ratio


def write_opt_adms_to_file(file, opt_num):
    str_optimal_num_of_adms = '\n' + "Optimal number of ADMs = " + str(opt_num)
    file.write(str_optimal_num_of_adms)


def write_lightpaths_to_file(file, paths):
    str_ = "\n" + str(len(paths)) + " Lightpaths:"
    file.write(str_)
    for path in paths:
        file.write('\n' + str(path))


def generate_lightpaths_ring(file, num_nodes, num_of_paths):    # also allow paths like 5 to 1
    if not num_of_paths or not num_nodes:
        return
    list_lightpaths = []
    # generate random length of each path
    index_start = 0
    start_of_circle = 0
    try_again = 0
    optimal_num_adms = 0
    completed_circle = False
    paths_count = copy.copy(num_of_paths)
    count_errors = 0

    while paths_count and count_errors < 1000:
        if completed_circle or try_again > 4:
            try_again = 0
            start_of_circle = start_of_circle + 1
            if start_of_circle == num_nodes:
                start_of_circle = 0
            index_start = start_of_circle

        if index_start > start_of_circle:
            r = num_nodes - index_start + start_of_circle
        elif index_start < start_of_circle:
            r = start_of_circle - index_start
        else:
            r = num_nodes - 1

        len_path = random.randint(1, r)       # if num nodes = 5 then max length is 4

        if len_path:
            index_end = index_start + len_path
            if index_end > num_nodes - 1:
                rest = index_end - num_nodes
                index_end = rest
                if index_start < start_of_circle:
                    if index_end > start_of_circle:
                        index_end = start_of_circle

            if [index_start, index_end] not in list_lightpaths:      # check if this path already exists
                try_again = 0
                list_lightpaths.append([index_start, index_end])
                paths_count = paths_count - 1
                if index_start == start_of_circle:
                    optimal_num_adms = optimal_num_adms + 1
                if not index_end == start_of_circle:
                    optimal_num_adms = optimal_num_adms + 1
                    completed_circle = False
                    index_start = index_end
                else:
                    completed_circle = True

            else:
                try_again = try_again + 1        # path already exists. pick other end index.
                completed_circle = False
                count_errors = count_errors + 1
                # count how many times we try again.

    print("ring - num of paths is - ", str(num_of_paths), ". paths are ", list_lightpaths,
          "optimal adms is - ", str(optimal_num_adms))

    write_opt_adms_to_file(file, optimal_num_adms)
    write_lightpaths_to_file(file, list_lightpaths)

    return optimal_num_adms, list_lightpaths


def generate_lightpaths_path(file, num_nodes, num_of_paths):
    if not num_of_paths or not num_nodes:
        return
    list_lightpaths = []
    # generate random length for each path
    optimal_num_adms = 0
    index_start = 0
    index_end = 0
    try_again = 0

    paths_count = copy.copy(num_of_paths)
    count_errors = 0

    while paths_count and count_errors < 1000:
        if try_again > 4:
            index_start = 0
            try_again = 0
        if index_end == num_nodes - 1:        # try 5 times. if fail then initialize index start
            index_start = 0
            index_end = 0
        r = num_nodes - index_start - 1
        len_path = random.randint(1, r)
        if len_path:
            index_end = index_start + len_path
            if [index_start, index_end] not in list_lightpaths:      # check if this path already exists
                try_again = 0
                if index_end > num_nodes-1:      # check that end_node exists
                    Exception("error - node does not exist")
                    return -1
                list_lightpaths.append([index_start, index_end])
                if index_start == 0:
                    optimal_num_adms = optimal_num_adms + 2
                else:
                    optimal_num_adms = optimal_num_adms + 1

                paths_count = paths_count - 1
                index_start = index_end
            else:
                try_again = try_again + 1        # path already exists. pick other end index.
                count_errors = count_errors + 1
                # count how many times we try again.

    print("num of paths is - ", str(num_of_paths), ". paths are ", list_lightpaths,
          "optimal adms is - ", str(optimal_num_adms))

    write_opt_adms_to_file(file, optimal_num_adms)
    write_lightpaths_to_file(file, list_lightpaths)

    return optimal_num_adms, list_lightpaths


def generate_lightpaths(file, num_nodes, topology, num_of_paths):
    if topology == 'path':
        return generate_lightpaths_path(file, num_nodes, num_of_paths)
    elif topology == 'ring':
        return generate_lightpaths_ring(file, num_nodes, num_of_paths)
    else:
        Exception("ERROR - Topology does not exist")
        return -1


def build_and_run_network(num_nodes, file_name, topology, num_of_paths):
    try:
        f_w = open(file_name, 'a')
    except IOError:
        print("Error - Could not open file!")
        return -1
    str_topology = f'Topology = {topology}'
    f_w.write(str_topology)
    str_nodes = '\nNumber of nodes = ' + str(num_nodes)
    f_w.write(str_nodes)        # write num of nodes to file

    optimum, list_lightpaths = generate_lightpaths(f_w, num_nodes, topology, num_of_paths)

    # run each permutation and write final result of avg ADMs in statistics file
    ratio_result = run_all_permutations(list_lightpaths, topology, num_nodes, num_of_paths, optimum)

    f_w.close()

    return ratio_result
