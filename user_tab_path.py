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

NUMBER_OF_NODES = 7
NODE_SIZE = 100
count3 = 0
flag = 0
a = 1
list_paths = []

canvas_tab_user_path = None
tab1_drawing_frame_p = None
frame_for_radio_btns_p = None
net = None
max_row = None

row_left_frame_p = 0
row_left_frame_radio_btns_p = 0
row_of_end_node_string = 0

'''
    this script is for visualizing the tab1 in path topology.
    Here the user can draw his own network by choosing number of nodes and choosing paths.
'''


def create_left_user_frame_p(tab):
    global tab1, left_fr, frame11, row_left_frame_p, list_paths
    tab1 = tab
    list_paths = []
    left_fr = Frame(tab, width=200, height=100, highlightbackground="black", highlightthickness=1)
    left_fr.pack(side=LEFT, fill=Y, expand=False)
    left_fr.grid_propagate(False)
    Label(left_fr, text="Build new graph  ", font=("Times", 12)).grid(row=row_left_frame_p, column=0, pady=10, sticky=W)
    row_left_frame_p = row_left_frame_p + 1
    # frame11 = left_fr
    options_nodes = [
        "3 nodes", "4 nodes", "5 nodes", "6 nodes", "7 nodes", "8 nodes", "9 nodes", "10 nodes", "11 nodes", "12 nodes",
    ]
    select_lbl = Label(left_fr, text="Select # of nodes:", font=("Times", 12))
    select_lbl.grid(row=row_left_frame_p, column=0, pady=5, sticky=W)
    select_lbl.grid_propagate(True)
    row_left_frame_p = row_left_frame_p + 1
    # global clicked_menu_path
    # global clicked_paths
    clicked_menu_path = StringVar()
    clicked_menu_path.set("# of nodes")
    global drop_nodes
    drop_nodes = OptionMenu(left_fr, clicked_menu_path, *options_nodes,
                            command=selected_number_nodes)
    drop_nodes.grid(row=row_left_frame_p, column=0, pady=5, sticky=W)
    row_left_frame_p = row_left_frame_p + 1


def selected_number_nodes(event):
    global tab1_drawing_frame_p, drop_nodes, row_left_frame_p, selected_num_nodes_p, \
        row_left_frame_radio_btns_p, frame_for_radio_btns_p
    if canvas_tab_user_path:
        canvas_tab_user_path.get_tk_widget().destroy()
    else:
        tab1_drawing_frame_p.destroy()
    tab1_drawing_frame_p = Frame(tab1, bg="white")
    tab1_drawing_frame_p.pack(fill=BOTH, expand=True)
    selected_num_nodes_p = event
    print("str selected - ", str(selected_num_nodes_p))
    selected_num_nodes_p = selected_num_nodes_p.split()
    selected_num_nodes_p = int(selected_num_nodes_p[0])
    print("int selected number is - ", str(selected_num_nodes_p))
    global number_path
    number_path = selected_num_nodes_p
    create_tab1_empty_path_net(selected_num_nodes_p)

    drop_nodes.configure(state="disabled")
    color_user_btn.configure(state="disabled")
    make_radio_buttons_start_node(left_fr, selected_num_nodes_p)

    create_g_list()


def create_g_list():            # this list is global and contains all the possible paths and # of row for every path
    global g_list_all_possible_paths, max_row, paths_and_rows_dic
    paths_and_rows_dic = {}
    max_row = 1
    g_list_all_possible_paths = []
    # if num_nodes = 4 then row1 contains paths [0,1], [1, 2], [2, 3] and row2 contains [0, 2], [2, 3]
    row = 1
    for i in range(0, selected_num_nodes_p):
        for k in range(1, selected_num_nodes_p):        # the jump
            if i+k < selected_num_nodes_p:
                if [i, i+k] not in g_list_all_possible_paths:
                    g_list_all_possible_paths.append([i, i+k])
    print("g_list with", str(selected_num_nodes_p), " nodes is -", str(g_list_all_possible_paths))


def get_row_number(path):           # input is path like [0, 2] and output is row number where to draw it like 2
    global max_row, paths_and_rows_dic
    for row in range(1, max_row+1):
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
        if path_conflict(path, value):
            return False
    return True


def path_conflict(path1, path2):
    list_edges_in_path1 = []
    list_edges_in_path2 = []
    for i in range(path1[0], path1[1]):
        list_edges_in_path1.append([i, i+1])
    for i in range(path2[0], path2[1]):
        list_edges_in_path2.append([i, i+1])

    # see if there are conflicting paths
    min_len_list = list_edges_in_path1
    other_list = list_edges_in_path2
    if len(list_edges_in_path2) < len(list_edges_in_path1):
        min_len_list = list_edges_in_path2
        other_list = list_edges_in_path1
    for path in min_len_list:
        if path in other_list:
            return True     # conflicting
    return False


def create_init_tab1_drawing_path(tab):
    global init_msg_tab1_path, init_title_tab1_path
    global tab1_drawing_frame_p

    tab1_drawing_frame_p = Frame(tab, bg="white")
    tab1_drawing_frame_p.pack(fill=BOTH, expand=True)

    init_title_tab1_path = Label(tab1_drawing_frame_p, text="Path Topology", font=("Maiandra GD", 25), bg="white")
    init_title_tab1_path.pack(side=TOP, pady=10)
    init_msg_tab1_path = Label(tab1_drawing_frame_p, text="Select number of nodes to start visualization",  font=("Times", 15), bg="white")
    init_msg_tab1_path.pack(pady=50)


def create_tab1_empty_path_net(num_nodes):
    global ax_tab1, f_p, canvas_tab_user, tab_new, tab1_drawing_frame_p
    f_p = plt.Figure(figsize=(9, 6.5))
    f_p.suptitle('Path Topology', size=25, font="Maiandra GD")
    ax_tab1 = f_p.add_subplot(111)
    ax_tab1.set_xlabel("Number of ADMs used : ?", fontsize=15, labelpad=20, font="Times New Roman")

    canvas_tab_user = FigureCanvasTkAgg(f_p, tab1_drawing_frame_p)
    canvas_tab_user.get_tk_widget().pack(fill="both", expand=True)
    canvas_tab_user.draw()
    create_empty_network(num_nodes, canvas_tab_user)


def create_empty_network(num_nodes, canvas_tab_user):
    global net, lightpaths_user
    global g_user, pos_path
    net = Network("path", num_nodes)
    g_user, pos_path = draw_network.draw_line_graph(num_nodes, ax_tab1)
    canvas_tab_user.draw()


def make_bottom_frame_user_p(tab):
    global frame_for_user_btns, tab11_p
    tab11_p = tab
    frame_for_user_btns = Frame(tab11_p, height=60)
    frame_for_user_btns.pack(side=BOTTOM, fill='x')
    add_buttons_to_frame(frame_for_user_btns)


def add_buttons_to_frame(frame_user):
    green_btns = Frame(frame_user)
    add_buttonss(green_btns)

    exit_but = Button(frame_user, text="Exit", command=exit_program, bg='#CD5C5C', fg='white')
    exit_but.pack(side=RIGHT, padx=20, pady=5)

    green_btns.pack()


def add_buttonss(frame):
    global add_another_btn, finish_btn, color_user_btn, restart_user_btn

    add_another_btn = tk.Button(frame, text="Add Another Path", command=add_another_path,
                                bg='#8FBC8F', fg='black')
    add_another_btn.pack(side=LEFT, padx=15, pady=10)
    add_another_btn.config(state=DISABLED)

    color_user_btn = tk.Button(frame, text="Color Path", command=color_path_user,
                               bg='#8FBC8F', fg='black')
    color_user_btn.pack(side=LEFT, padx=15, pady=10)
    color_user_btn.config(state=DISABLED)

    finish_btn = tk.Button(frame, text="Show ADMs", command=show_num_adms,
                           bg='#8FBC8F', fg='black')

    restart_user_btn = tk.Button(frame, text="Restart", command=restart_tab1_path,
                                 bg='orange', fg='black')
    restart_user_btn.pack(side=LEFT, padx=25, pady=10)
    restart_user_btn.config(state=NORMAL)


def make_radio_buttons_start_node(tab, num_nodes_selected):
    global frame_for_radio_btns_p, row_left_frame_radio_btns_p, row_left_frame_p, var, row_of_end_node_string
    row_left_frame_radio_btns_p = 0
    if frame_for_radio_btns_p:
        frame_for_radio_btns_p.destroy()
    frame_for_radio_btns_p = Frame(left_fr)
    frame_for_radio_btns_p.grid(row=row_left_frame_p, column=0)
    row_left_frame_p = row_left_frame_p + 1

    Label(frame_for_radio_btns_p, text="Generate new path:", font=("Times", 12)).grid(row=row_left_frame_radio_btns_p,
                                                                                      column=0, pady=15)
    row_left_frame_radio_btns_p = row_left_frame_radio_btns_p + 1
    Label(frame_for_radio_btns_p, text="Start node", font=("Times", 12)).grid(row=row_left_frame_radio_btns_p,
                                                                              column=0, pady=5)
    row_of_end_node_string = row_left_frame_radio_btns_p
    row_left_frame_radio_btns_p = row_left_frame_radio_btns_p + 1

    Label(frame_for_radio_btns_p, text="End node", font=("Times", 12)).grid(row=row_of_end_node_string,
                                                                            column=1, pady=10)
    row_of_end_node_string = row_of_end_node_string + 1

    var = IntVar()
    var.set(500)
    number_path = selected_num_nodes_p
    global radiobutton_start_list
    radiobutton_start_list = []
    for i in range(number_path-1):
        if i_is_usable(i):      # i is usable
            radiobutton_start = Radiobutton(frame_for_radio_btns_p, text=i, variable=var, value=i, command=selected_start)
            radiobutton_start.grid(row=row_left_frame_radio_btns_p, column=0)
            row_left_frame_radio_btns_p = row_left_frame_radio_btns_p + 1
            radiobutton_start_list.append(radiobutton_start)
    add_another_btn.config(state=DISABLED)


def i_is_usable(i):
    usable = -1
    j = selected_num_nodes_p - 1
    while usable == -1 and j > -1 and j > i:
        if [i, j] not in list_paths and not i == j:
            usable = 1
        j = j - 1
    if usable == -1:
        return False
    if usable == 1:
        return True


def make_radio_buttons_end_node(tab, start_node_input):
    global var2, list1, radiobutton_end_list, list_paths
    global row_of_end_node_string, row_left_frame_p, frame_for_radio_btns_p
    radiobutton_end_list = []
    list1 = []
    var2 = IntVar()
    var2.set(500)
    number_path = selected_num_nodes_p
    for i in range(number_path):
        if i > start_node_input:
            list1.append(i)

    for i in range(number_path):
        if i > var.get():
            if [var.get(), i] not in list_paths:
                radiobutton_end = Radiobutton(frame_for_radio_btns_p, text=i, variable=var2, value=i,
                                              command=selected_end)
                radiobutton_end.grid(row=row_of_end_node_string, column=1)
                row_of_end_node_string = row_of_end_node_string + 1
                radiobutton_end_list.append(radiobutton_end)


def selected_start():
    global start_node_input, var
    start_node_input = var.get()
    for i in range(len(radiobutton_start_list)):
        radiobutton_start_list[i].configure(state="disabled")
    make_radio_buttons_end_node(left_fr, start_node_input)


def selected_end():
    global end_node_input, list_paths, a, net, radiobutton_end_list, new_edge
    global row_to_draw
    print("selected path is - ", str(var.get()), ", ", str(var2.get()))
    for i in range(len(radiobutton_end_list)):
        radiobutton_end_list[i].configure(state="disabled")
    count2 = 0
    wait_flag = 0
    l1 = []
    end_node_input = var2.get()
    new_edge = [start_node_input, end_node_input]
    list_paths.append(new_edge)
    l1.append(new_edge)
    # ##check if the selected path is already has been selected
    # ##if it has been selected, then select again another path
    for i in range(len(list_paths)):
        if new_edge == list_paths[i]:
            count2 = count2 + 1
            # ##select again
    if count2 > 1:
        tk.messagebox.showerror(title='ERROR',
                                 message='Choose another path. This path is already in the network.')
        restart_sub_frame_of_radio_btns_p()
        list_paths.remove(new_edge)
        l1.remove(new_edge)
        wait_flag = 1
        # add_another_btn.config(state=NORMAL)
    count_how_many = 0
    # ##Draw the path
    if wait_flag == 0:
        net.add_paths_to_network(l1)
        new_net_tmp = Network("path", int(number_path))
        new_net_tmp.add_paths_to_network(l1)
        a1 = new_net_tmp.get_lightpaths()
        b1 = net.get_lightpaths()
        new_net_tmp.reset_network()
        # for i in range(len(list_paths)):
        #     # if algorithm_minadm.is_conflicting(a1[0], b1[i]):
        #         # flag_found = 1 # found a path that conflicts
        #         count_how_many = count_how_many + 1
        #         if count_how_many == 2:
        #             a = a + 1
        count_how_many = 0
        # if a == 5:
        #     tk.messagebox.showerror(title='Oops', message='The path you added is not visible')
        # draw_network.draw_paths_above_in_path(g_user, ax_tab1, int(number_path), canvas_tab_user, new_edge, a, 1)
        row_to_draw = get_row_number(new_edge)
        draw_network.draw_paths_above_in_path(g_user, ax_tab1, int(number_path), canvas_tab_user, new_edge,
                                              row_to_draw, 1)
        color_user_btn.config(state=NORMAL)


def add_another_path():
    global count3, flag
    count3 = count3 + 1
    print("count ", count3)
    # if count3 == 5:
    #     tk.messagebox.showerror(title='ERROR', message='Sorry, you can only add 5 paths')
    #     add_another_btn.config(state=DISABLED)
    #     a = 1
    #     return
    restart_sub_frame_of_radio_btns_p()
    finish_btn.config(state=DISABLED)


def restart_sub_frame_of_radio_btns_p():
    global frame_for_radio_btns_p, row_left_frame_radio_btns_p, row_left_frame_p, list_paths
    # list_user_paths_path = []
    row_left_frame_p = row_left_frame_p - 1
    row_left_frame_radio_btns_p = 0
    frame_for_radio_btns_p.destroy()
    # frame_for_radio_btns_p = None
    make_radio_buttons_start_node(tab1, selected_num_nodes_p)


def show_num_adms():
    ax_tab1.set_xlabel(f"Number of ADMs used : {len(net.adms_list)}", fontsize=15, labelpad=20, font="Times New Roman")
    canvas_tab_user.draw()
    print("number of adms: ", len(net.adms_list))


def color_path_user():
    print("color path")
    if net.colored:  # if colored is true there is an error. should be false
        Exception("colored must be false")
    index_path = net.get_index()
    lightpath_to_color = net.get_lightpaths()[index_path]
    chosen_color = algorithm_minadm.color_lightpath(lightpath_to_color, nodes=selected_num_nodes_p,
                                                    color_not_random=True, network=net)

    draw_network.color_paths_above(g_user, ax_tab1, canvas_tab_user, lightpath_to_color, None, chosen_color,
                                   row_to_draw)  # in Draw file
    net.inc_index_in_paths_in_network()
    net.colored_true()
    print("colored lightpath", lightpath_to_color.start_node.node_id, ",", lightpath_to_color.end_node.node_id,
          "with color", chosen_color)
    print("lightpath of the net :", net.get_lightpaths())
    color_user_btn.config(state=DISABLED)
    if len(g_list_all_possible_paths) == len(list_paths):
        print("cannot add more paths")
        add_another_btn.config(state=DISABLED)
    else:
        add_another_btn.config(state=NORMAL)
    finish_btn.config(state=NORMAL)
    show_num_adms()


def restart_tab1_path():
    global count3, a, g_list_all_possible_paths, max_row, paths_and_rows_dic
    if not messagebox.askokcancel(title="Restart", message="Are you sure?"):
        return
    global left_fr, tab1_drawing_frame_p, canvas_tab_user_path, frame_for_user_btns
    g_list_all_possible_paths = []
    max_row = 1
    paths_and_rows_dic = {}
    print("reset g_list = ", str(g_list_all_possible_paths))
    left_fr.destroy()
    # left_fr = None
    frame_for_user_btns.destroy()
    # frame_for_user_btns = None
    if canvas_tab_user_path:
        canvas_tab_user_path.get_tk_widget().destroy()
        # canvas_tab_user_path = None
    if tab1_drawing_frame_p:
        tab1_drawing_frame_p.destroy()
        # tab1_drawing_frame_p = None

    if net:
        net.reset_network()
    for path in list_paths:  # remove all paths
        g_user.remove_edges_from([path])
    list_paths.clear()
    # a = 1
    # count3 = 0
    create_left_user_frame_p(tab1)
    make_bottom_frame_user_p(tab1)
    create_init_tab1_drawing_path(tab1)
    # print("count 3 ", count3)
