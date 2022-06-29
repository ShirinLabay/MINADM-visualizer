import large_networks
import os.path
'''
make networks -
nodes = 10: paths = 5, 10, 15, 20
nodes = 20, paths = 10, 15, 20, 25, 30, 35, 40
nodes = 30, paths = 15, 20, 25, 30, 35, 40, 45, 50, 55, 60
nodes = 40, paths = 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80
nodes = 50, paths = 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100
nodes = 60, paths = 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120
nodes = 70, paths = 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140
nodes = 80, paths = 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160
nodes = 90, paths = 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180
nodes = 100, paths = 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200
'''

'''
    This file generates all the networks above, for each network the algorithm runs 300 permutations and writes the 
    average result in statistics files to later display in 3d graph in the third tabs
    also generates new files where a files named "networks_txt/ring/network20_35.txt" represents a ring network
    with 20 nodes and 35 paths as input. these files contain the topology, # nodes, the optimal # of ADMs and the list
    of the lightpaths
'''


def add_and_run(num_nodes, num_paths, topology):
    # for example gets 10 and 15 - creates network and run it, final results in statistics
    # and adds to list the path 'networks_txt/ring/network_10_15.txt'

    file_name = "networks_txt/" + str(topology) + "/network_" + str(num_nodes) + "_" + str(num_paths) + ".txt"
    print("file name is - ", file_name)
    return large_networks.build_and_run_network(num_nodes, file_name, topology, num_paths)


'''i = 10
while i < 101:          # make 10 networks
    j = int(i / 2)
    while j < (2 * i) + 1:      # for every network make 10
        if not j == 5:
            add_and_run(i, j, 'path')
            add_and_run(i, j, 'ring')

        j = j + 5
    i = i + 10'''


def build_and_run_range(num_nodes, paths_from, paths_to, topology):  # gets number of nodes and range of number of paths
    if not num_nodes or not paths_from or not paths_to:
        return
    list_results = []
    num_nodes = int(num_nodes)
    paths_from = int(paths_from)
    paths_to = int(paths_to)
    for i in range(int(paths_from), int(paths_to)+1, 1):
        file_name = "networks_txt/" + str(topology) + "/network_" + str(num_nodes) + "_" + str(i) + ".txt"
        if os.path.isfile(file_name) and os.path.getsize(file_name) > 0:     # check if file already exists
            # already_exists_in_statistics_file = True
            f = 'networks_txt/' + str(topology) + '/' + str(topology[0]) + '_statistics1.txt'
            try:
                f_statistics = open(f, 'r')
            except IOError:
                print("Error - Could not open statistics file!")
                return -1
            ratio_result = find_ratio_result(f_statistics, num_nodes, i)
            if not ratio_result == "not found in statistics file":
                list_results.append([num_nodes, i, ratio_result])       # [num nodes, num paths, result(ratio)
            else:
                os.remove(file_name)
                list_results.append([num_nodes, i, add_and_run(num_nodes, i, topology)])
        else:           # run the algorithm in this network and add result to statistics file
            result = add_and_run(num_nodes, i, topology)
            list_results.append([num_nodes, i, result])       # [num nodes, num paths, result(ratio)
    return list_results


def find_ratio_result(file, n_nodes, n_paths):
    file.readline()
    lines = file.readlines()
    for line in lines:
        splitt = str(line.replace("\\", " "))
        splitt = splitt.replace("\n", " ")
        splitt = splitt.split(" ")
        if int(splitt[1]) == n_nodes and int(splitt[2]) == n_paths:
            return float(splitt[5])
    return "not found in statistics file"

