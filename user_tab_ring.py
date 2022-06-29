from tkinter import messagebox
from Network import *
import algorithm_minadm
from average_analysis import *
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import draw_network

matplotlib.use('TkAgg')

NUMBER_OF_NODES = 10
NODE_SIZE = 100
count_ring = 0
flag_ring = 0
a_ring = 1
angle_r = 0.2
list_paths_ring = []
max_row = None
net_ring = None

row_left_frame = 0
row_left_frame_radio_btns = 0
canvas_tab_user_ring = None
tab1_drawing_frame = None
frame_for_radio_btns = None
row_for_end_label = 0

'''this script is for visualizing the tab1 in ring topology.
 Here the user can draw his own network by choosing number of nodes and choosing paths.
 '''


#  ############# tab 1 left side


def create_left_user_frame_r(tab):
    global tab1, left_fr_ring, row_left_frame, list_user_paths_ring
    list_user_paths_ring = []
    tab1 = tab  # to make it global
    # global left_fr_ring, frame11_ring
    left_fr_ring = Frame(tab, width=200, height=100, highlightbackground="black", highlightthickness=1)
    left_fr_ring.pack(side=LEFT, fill=Y, expand=False)
    left_fr_ring.grid_propagate(False)
    Label(left_fr_ring, text="Build new graph:", font=("Times", 12)).grid(row=row_left_frame, column=0, pady=10,
                                                                          sticky=W)
    row_left_frame = row_left_frame + 1
    frame11_ring = left_fr_ring
    options_for_num_nodes = [
        "6 nodes", "7 nodes", "8 nodes", "9 nodes", "10 nodes", "11 nodes", "12 nodes", "13 nodes"
    ]
    Label(left_fr_ring, text="Select # of nodes:", font=("Times", 12)).grid(row=row_left_frame, column=0, pady=5,
                                                                            sticky=W)
    row_left_frame = row_left_frame + 1
    # global clicked_ring
    # global clicked_paths_ring
    option_menu_num_nodes = StringVar()
    option_menu_num_nodes.set("# of nodes")  # init value
    global drop_nodes_ring
    drop_nodes_ring = OptionMenu(left_fr_ring, option_menu_num_nodes, *options_for_num_nodes,
                                 command=selected_number_nodes_ring)
    drop_nodes_ring.grid(row=row_left_frame, column=0, pady=5, sticky=W)
    row_left_frame = row_left_frame + 1


def selected_number_nodes_ring(event):
    global tab1_drawing_frame, drop_nodes_ring, row_left_frame, selected_num_nodes, \
        row_left_frame_radio_btns, frame_for_radio_btns
    print("test1")
    if canvas_tab_user_ring:
        canvas_tab_user_ring.get_tk_widget().destroy()
    else:
        tab1_drawing_frame.destroy()
    print("test2")
    tab1_drawing_frame = Frame(tab1, bg="white")
    tab1_drawing_frame.pack(fill=BOTH, expand=True)
    selected_num_nodes = event
    print("str selected - ", str(selected_num_nodes))
    selected_num_nodes = selected_num_nodes.split()
    selected_num_nodes = int(selected_num_nodes[0])
    print("int selected number is - ", str(selected_num_nodes))
    global number_ring
    number_ring = selected_num_nodes
    create_ring_in_tab1_drawing(selected_num_nodes)

    print("test3")

    drop_nodes_ring.configure(state="disabled")
    make_radio_buttons_start_node(left_fr_ring, selected_num_nodes)
    color_user_btn_ring.config(state=DISABLED)
    print("test4")
    create_g_list()
    print("test5")


# ####### tab 1 ring - bottom frame for buttons


def make_bottom_frame(tab):
    global frame_btns_tab1_ring, tab11_ring
    tab11_ring = tab
    frame_btns_tab1_ring = Frame(tab11_ring, height=60)
    frame_btns_tab1_ring.pack(side=BOTTOM, fill='x')
    add_buttons_to_frame(frame_btns_tab1_ring)


def add_buttons_to_frame(frame):
    green_btns = Frame(frame)
    add_buttons(green_btns)

    exit_but = Button(frame, text="Exit", command=exit_program, bg='#CD5C5C', fg='white')
    exit_but.pack(side=tk.RIGHT, padx=20, pady=10)

    green_btns.pack()


def add_buttons(frame):
    global add_another_btn_ring, finish_btn_ring, color_user_btn_ring, restart_user_btn_ring

    add_another_btn_ring = tk.Button(frame, text="Add Another Path", command=add_another_path_ring,
                                     bg='#8FBC8F', fg='black')
    add_another_btn_ring.pack(side=LEFT, padx=15, pady=10)
    add_another_btn_ring.config(state=DISABLED)

    color_user_btn_ring = tk.Button(frame, text="Color Path", command=color_path_user_ring,
                                    bg='#8FBC8F', fg='black')
    color_user_btn_ring.pack(side=LEFT, padx=15, pady=10)
    color_user_btn_ring.config(state=DISABLED)

    finish_btn_ring = tk.Button(frame, text="Show ADMs", command=show_num_adms_ring,
                                bg='#8FBC8F', fg='black')

    restart_user_btn_ring = tk.Button(frame, text="Restart", command=restart_tab1_ring,
                                      bg='orange', fg='black')
    restart_user_btn_ring.pack(side=LEFT, padx=25, pady=10)
    restart_user_btn_ring.config(state=NORMAL)


# ##### tab 1 ring - frame for visualization - draw network here


def create_init_tab1_drawing(tab):
    global init_msg_tab1, init_title_tab1
    global tab1_drawing_frame

    tab1_drawing_frame = Frame(tab, bg="white")
    tab1_drawing_frame.pack(fill=BOTH, expand=True)

    init_title_tab1 = Label(tab1_drawing_frame, text="Ring Topology", font=("Maiandra GD", 25), bg="white")
    init_title_tab1.pack(side=TOP, pady=10)
    init_msg_tab1 = Label(tab1_drawing_frame, text="Select number of nodes to start visualization", font=("Times", 15),
                          bg="white")
    init_msg_tab1.pack(pady=50)


def create_ring_in_tab1_drawing(num_nodes):
    global tab1_drawing_frame, ax_tab1_ring, canvas_tab_user_ring, f, tab_new_ring
    f = plt.Figure(figsize=(9, 6.5))
    f.suptitle('Ring Topology', size=25, font="Maiandra GD")
    ax_tab1_ring = f.add_subplot(111)
    ax_tab1_ring.set_xlabel("Number of ADMs used : ?", fontsize=15, labelpad=20, font="Times New Roman")
    canvas_tab_user_ring = FigureCanvasTkAgg(f, tab1_drawing_frame)
    canvas_tab_user_ring.get_tk_widget().pack(fill=BOTH, expand=True)
    canvas_tab_user_ring.draw()
    create_empty_network(num_nodes, canvas_tab_user_ring)


def create_empty_network(num_nodes, canvas_tab_user_ring):
    global net_ring, lightpaths_user_ring
    global g_user_ring, pos_ring
    net_ring = Network("ring", num_nodes)
    g_user_ring, pos_ring = draw_network.draw_circle_graph(num_nodes, ax_tab1_ring, 1)
    canvas_tab_user_ring.draw()


# ###################### user interface tab 1


def create_g_list():  # this list is global and contains all the possible paths and # of row for every path
    global g_list_all_possible_paths, max_row, paths_and_rows_dic
    paths_and_rows_dic = {}
    max_row = 1
    g_list_all_possible_paths = []

    # if num_nodes = 4 then row1 contains paths [0,1], [1, 2], [2, 3] and row2 contains [0, 2], [2, 3]
    row = 1
    for i in range(0, selected_num_nodes):
        c = 0
        for k in range(1, selected_num_nodes):  # the jump
            if i + k < selected_num_nodes:
                if [i, i + k] not in g_list_all_possible_paths:
                    g_list_all_possible_paths.append([i, i + k])
            else:
                if c < i:
                    g_list_all_possible_paths.append([i,c])
                    c = c + 1
    print("g_list with", str(selected_num_nodes), " nodes is -", str(g_list_all_possible_paths))


def get_row_number(path):  # input is path like [0, 2] and output is row number where to draw it like 2
    global max_row, paths_and_rows_dic
    for row in range(1, max_row + 1):
        if path_can_fit_in_row(path, row):
            if row in paths_and_rows_dic:
                paths_and_rows_dic[row].append(path)
            else:
                paths_and_rows_dic[row] = [path]
            return row
    max_row = max_row + 1
    paths_and_rows_dic[max_row] = [path]
    return max_row


def path_can_fit_in_row(path, row):
    if not paths_and_rows_dic:
        return True
    if not paths_and_rows_dic[row]:
        return True
    for value in paths_and_rows_dic[row]:
        if path_conflict_ring(path, value):
            return False
    return True


def path_conflict_ring(path1, path2):
    list_edges_in_path1 = []
    list_edges1 = []
    list_edges_in_path2 = []
    list_edges2 = []
    if path1[0] > path1[1]:
        for i in range(0, selected_num_nodes - path1[0]):
            list_edges_in_path1.append(i + path1[0])
        for i in range(0, path1[1] + 1):
            list_edges_in_path1.append(i)
        for i, j in zip(list_edges_in_path1, list_edges_in_path1[1:]):
            list_edges1.append([i, j])
    else:
        for i in range(path1[0], path1[1] + 1):
            list_edges_in_path1.append(i)
        for i, j in zip(list_edges_in_path1, list_edges_in_path1[1:]):
            list_edges1.append([i, j])

    if path2[0] > path2[1]:
        for i in range(0, selected_num_nodes - path2[0]):
            list_edges_in_path2.append(i + path2[0])
        for i in range(0, path2[1] + 1):
            list_edges_in_path2.append(i)
        for i, j in zip(list_edges_in_path2, list_edges_in_path2[1:]):
            list_edges2.append([i, j])
    else:
        for i in range(path2[0], path2[1] + 1):
            list_edges_in_path2.append(i)
        for i, j in zip(list_edges_in_path2, list_edges_in_path2[1:]):
            list_edges2.append([i, j])

    # see if there are conflicting paths
    min_len_list = list_edges1
    other_list = list_edges2
    print("list1 ", list_edges1)

    print("list2 ", list_edges2)
    if len(list_edges2) < len(list_edges1):
        min_len_list = list_edges2
        other_list = list_edges1
    for path in min_len_list:
        if path in other_list:
            return True  # conflicting
    return False


def make_radio_buttons_start_node(tab, selected_num_nodes):
    global frame_for_radio_btns, row_left_frame_radio_btns, var_ring, row_left_frame, row_for_end_label
    row_left_frame_radio_btns = 0
    if frame_for_radio_btns:
        frame_for_radio_btns.destroy()
    frame_for_radio_btns = Frame(left_fr_ring)
    frame_for_radio_btns.grid(row=row_left_frame, column=0)
    row_left_frame = row_left_frame + 1

    Label(frame_for_radio_btns, text="Generate new path:", font=("Times", 12)).grid(row=row_left_frame_radio_btns,
                                                                                    column=0, pady=15)
    row_left_frame_radio_btns = row_left_frame_radio_btns + 1
    row_for_end_label = row_left_frame_radio_btns
    Label(frame_for_radio_btns, text="Start node", font=("Times", 12)).grid(row=row_left_frame_radio_btns, column=0,
                                                                            pady=10)
    row_left_frame_radio_btns = row_left_frame_radio_btns + 1

    Label(frame_for_radio_btns, text="End node", font=("Times", 12)).grid(row=row_for_end_label, column=1,
                                                                          pady=10)
    row_for_end_label = row_for_end_label + 1

    var_ring = IntVar()
    var_ring.set(500)
    number = selected_num_nodes
    global radiobutton_start_list_ring
    radiobutton_start_list_ring = []
    for i in range(number):
        if i_is_usable(i):  # i is usable
            radiobutton_start = Radiobutton(frame_for_radio_btns, text=i, variable=var_ring, value=i,
                                            command=selected_start_ring,
                                            cursor="hand2")
            radiobutton_start.grid(row=row_left_frame_radio_btns, column=0)
            row_left_frame_radio_btns = row_left_frame_radio_btns + 1
            radiobutton_start_list_ring.append(radiobutton_start)
    add_another_btn_ring.config(state=DISABLED)


def i_is_usable(i):
    usable = -1
    j = selected_num_nodes - 1
    while usable == -1 and j > -1:
        if [i, j] not in list_paths_ring and not i == j:
            usable = 1
        j = j - 1
    if usable == -1:
        return False
    if usable == 1:
        return True


def selected_start_ring():
    print("event value is - ", var_ring.get())
    global start_node_input_ring
    start_node_input_ring = var_ring.get()
    for i in range(len(radiobutton_start_list_ring)):
        radiobutton_start_list_ring[i].configure(state="disabled")
    make_radio_buttons_end_node(left_fr_ring, start_node_input_ring)


def make_radio_buttons_end_node(tab, start_node_input):
    global var2_ring, row_left_frame, frame_for_radio_btns, row_left_frame_radio_btns, row_for_end_label
    global list_ring
    global radiobutton_end_list_ring
    radiobutton_end_list_ring = []
    list_ring = []
    var2_ring = IntVar()
    var2_ring.set(500)
    number_ring = selected_num_nodes
    for i in range(number_ring):
        if i != start_node_input:
            list_ring.append(i)

    for i in range(selected_num_nodes):
        if not i == var_ring.get():
            if [var_ring.get(), i] not in list_paths_ring and [i, var_ring.get()] not in list_paths_ring:
                radiobutton_end = Radiobutton(frame_for_radio_btns, text=i, variable=var2_ring, value=i,
                                              command=selected_end_ring)
                radiobutton_end.grid(row=row_for_end_label, column=1)
                row_for_end_label = row_for_end_label + 1
                radiobutton_end_list_ring.append(radiobutton_end)


def selected_end_ring():  # var_ring is start node. var_ring2 is end node - now draw path
    global list_user_paths_ring
    global end_node_input_ring, color_user_btn_ring
    global net_ring
    global a_ring, angle_r, row_to_draw_ring
    count_ring = 0
    wait_flag = 0
    l1 = []
    for i in range(len(radiobutton_end_list_ring)):
        radiobutton_end_list_ring[i].configure(state="disabled")
    end_node_input_ring = var2_ring.get()
    new_edge = [start_node_input_ring, end_node_input_ring]
    list_paths_ring.append(new_edge)
    l1.append(new_edge)
    print(list_paths_ring)
    # check if the selected path is already has been selected
    # if it has been selected, then select again another path
    for i in range(len(list_paths_ring)):
        if new_edge == list_paths_ring[i]:
            count_ring = count_ring + 1
            # ##select again
    if count_ring > 1:
        tk.messagebox.showerror(title='ERROR',
                                message='Choose another path. This path is already in the network.')
        restart_sub_frame_of_radio_btns()
        list_paths_ring.remove(new_edge)
        l1.remove(new_edge)
        print("list ", list_paths_ring)
        print("l1 ", l1)
        wait_flag = 1
        return
    count_how_many = 0
    # ##Draw the path
    if wait_flag == 0:
        net_ring.add_paths_to_network(l1)
        new_net_tmp = Network("ring", int(number_ring))
        new_net_tmp.add_paths_to_network(l1)
        a1 = new_net_tmp.get_lightpaths()
        print("a1", a1[0])
        b1 = net_ring.get_lightpaths()
        print("b1", b1)
        # for i in range(len(list_paths_ring)):
        #     if b1[i] is not None:
        #         # if algorithm_minadm.is_conflicting(a1[0], b1[i]):
        #             # flag_found = 1 # found a path that conflicts
        #             count_how_many = count_how_many + 1
        #             if count_how_many == 2:
        #                 print("conflicting")
        #                 a_ring = a_ring + 1
        #                 angle_r = angle_r + 0.2
        #                 print("a=", a_ring)
        count_how_many = 0
        # delete the canvas and remake it.
        row_to_draw_ring = get_row_number(new_edge)
        draw_network.draw_paths_in_circle_user(g_user_ring, ax_tab1_ring, int(number_ring), canvas_tab_user_ring,
                                               new_edge, row_to_draw_ring)
        color_user_btn_ring.config(state=NORMAL)


def add_another_path_ring():
    global count_ring, flag_ring
    count_ring = count_ring + 1

    restart_sub_frame_of_radio_btns()
    finish_btn_ring.config(state=DISABLED)


def restart_sub_frame_of_radio_btns():
    global frame_for_radio_btns, row_left_frame, row_left_frame_radio_btns, list_paths_ring
    # list_paths_ring = []
    row_left_frame = row_left_frame - 1
    row_left_frame_radio_btns = 0
    frame_for_radio_btns.destroy()
    # frame_for_radio_btns = None
    make_radio_buttons_start_node(tab1, selected_num_nodes)


def show_num_adms_ring():
    ax_tab1_ring.set_xlabel(f"Number of ADMs used : {len(net_ring.adms_list)}", fontsize=15, labelpad=20,
                            font="Times New Roman")
    canvas_tab_user_ring.draw()
    print("number of adms: ", len(net_ring.adms_list))


def color_path_user_ring():
    print("color path")
    if net_ring.colored:  # if colored is true there is an error. should be false
        Exception("colored must be false")
    index_path = net_ring.get_index()
    lightpath_to_color = net_ring.get_lightpaths()[index_path]
    chosen_color = algorithm_minadm.color_lightpath(lightpath_to_color, nodes=selected_num_nodes, color_not_random=True, network=net_ring)
    print("color = ", chosen_color)
    draw_network.color_path_ring(g_user_ring, ax_tab1_ring, int(number_ring), canvas_tab_user_ring, lightpath_to_color,
                                 None, chosen_color, row_to_draw_ring)  # in Draw file
    net_ring.inc_index_in_paths_in_network()
    net_ring.colored_true()
    print("colored lightpath", lightpath_to_color.start_node.node_id, ",", lightpath_to_color.end_node.node_id,
          "with color", chosen_color)
    print("lightpath of the net :", net_ring.get_lightpaths())
    color_user_btn_ring.config(state=DISABLED)
    if len(g_list_all_possible_paths) == len(list_paths_ring):
        print("cannot add more paths")
        add_another_btn_ring.config(state=DISABLED)
    else:
        add_another_btn_ring.config(state=NORMAL)
    finish_btn_ring.config(state=NORMAL)
    show_num_adms_ring()


def restart_tab1_ring():
    global a_ring, count_ring
    if not messagebox.askokcancel(title="Restart", message="Are you sure?"):
        return
    global left_fr_ring, tab1_drawing_frame, canvas_tab_user_ring, frame_btns_tab1_ring, g_list_all_possible_paths
    global max_row, paths_and_rows_dic

    g_list_all_possible_paths = []
    max_row = 1
    paths_and_rows_dic = {}
    print("reset g_list = ", str(g_list_all_possible_paths))
    left_fr_ring.destroy()
    left_fr_ring = None
    frame_btns_tab1_ring.destroy()
    frame_btns_tab1_ring = None
    if canvas_tab_user_ring:
        canvas_tab_user_ring.get_tk_widget().destroy()
        canvas_tab_user_ring = None
    if tab1_drawing_frame:
        tab1_drawing_frame.destroy()
        tab1_drawing_frame = None
    if net_ring:
        net_ring.reset_network()
    for path in list_paths_ring:  # remove all paths
        g_user_ring.remove_edges_from([path])
    list_paths_ring.clear()
    # a_ring = 1
    count_ring = 0
    create_left_user_frame_r(tab1)
    make_bottom_frame(tab1)
    create_init_tab1_drawing(tab1)
    print("reset done")


def get_number_of_nodes_selected_in_ring():
    return selected_num_nodes
