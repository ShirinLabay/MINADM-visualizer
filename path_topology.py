from user_tab_path import *
from tkinter import ttk, messagebox
from average_analysis import *
from Network import *
import tkinter as tk
import algorithm_minadm
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import draw_network
matplotlib.use('TkAgg')

NUMBER_OF_NODES = 7
NODE_SIZE = 100

'''
    path topology - 
    - alg_visualizing_tab1 is the first tab - visualizing the algorithm with user input
    - optimal_solution_tab2 is the second tab where there is a comparison with the optimal solution and the algorithm 
        on the same network.
    - average_tab3 is the third tab - calls create_average_tab from average_analysis.py
'''

network = None
lightpaths = None
g = None
pos = None
add_all_btn = None
add_next_btn = None
color_path_btn = None
tab11 = None
can_for_alg = None

ax = None
f = None
canvas_tab1 = None


def create_path_notebook(tab):
    notebook_path = ttk.Notebook(tab)
    alg_visualizing_tab1 = Frame(notebook_path)
    optimal_solution_tab2 = Frame(notebook_path)
    average_tab3 = Frame(notebook_path)
    notebook_path.add(alg_visualizing_tab1, text="Algorithm Visualization")
    notebook_path.add(optimal_solution_tab2, text="Optimal Solution")
    notebook_path.add(average_tab3, text="Average Analysis")
    notebook_path.pack(expand=True, fill="both")

    create_left_user_frame_p(alg_visualizing_tab1)
    make_bottom_frame_user_p(alg_visualizing_tab1)
    create_init_tab1_drawing_path(alg_visualizing_tab1)

    create_optimal_solution_tab(optimal_solution_tab2)       # tab 2

    create_average_tab(average_tab3, 'path')


def create_network():
    global network, lightpaths
    global g, pos
    network = Network("path", NUMBER_OF_NODES)
    g, pos = draw_network.draw_line_graph(NUMBER_OF_NODES, ax)
    lightpaths = [[0, 1], [2, 3], [5, 6], [1, 2], [1, 4], [3, 5]]
    network.add_paths_to_network(lightpaths)

# ################################ tab 2 optimal path


def create_optimal_solution_tab(tab2):
    global tab11, can_for_alg
    tab11 = tab2
    # frame for visualization buttons
    frame_for_visualization_btns = Frame(tab2, height=50, bg="white")
    frame_for_visualization_btns.pack(side=BOTTOM, fill=BOTH, expand=False)
    add_visualizing_tab2_buttons(frame_for_visualization_btns)
    frame_for_visualization_btns.pack_propagate(False)

    can_for_optimal = Canvas(tab2, height=250)  # , background="pink")
    can_for_optimal.pack(side=TOP, fill=BOTH, expand=True, pady=5)
    can_for_optimal.pack_propagate(False)

    can_for_alg = Canvas(tab2, height=250)  # , background="white")
    can_for_alg.pack(side=TOP, fill=BOTH, expand=True)
    can_for_alg.pack_propagate(False)

    draw_optimal_solution(can_for_optimal)

    draw_network_to_run_alg(can_for_alg)  # tab 2


def draw_optimal_solution(canvas):
    f = plt.Figure(figsize=(9, 6.5))
    f.suptitle('The Optimal Solution', size=15, font="Maiandra GD")
    ax = f.add_subplot(6, 1, (1, 5))
    ax.set_xlabel("Number of ADMs used : 8", fontsize=13, labelpad=20, font="Times New Roman")

    draw_network.draw_line_graph(NUMBER_OF_NODES, ax)

    canvas = FigureCanvasTkAgg(f, canvas)
    canvas.get_tk_widget().pack(fill='x', expand=False, pady=5)
    canvas.draw()

    draw_paths_colored_path_optimal(ax, canvas)


def draw_paths_colored_path_optimal(ax, canvas_tab2):
    draw_network.color_path_in_opt(ax, canvas_tab2)


def draw_network_to_run_alg(second_canvas):  # create Network instance
    global ax, f, canvas_tab1
    f = plt.Figure(figsize=(9, 6.5))
    f.suptitle('Run The Algorithm', size=15, font="Maiandra GD")
    ax = f.add_subplot(6, 1, (1, 5))
    ax.set_xlabel("Number of ADMs used : ?", fontsize=13, labelpad=20, font="Times New Roman")
    create_network()
    canvas_tab1 = FigureCanvasTkAgg(f, second_canvas)
    canvas_tab1.get_tk_widget().pack(fill="x", expand=False)
    canvas_tab1.draw()


def add_visualizing_tab2_buttons(frame_btns):
    green_btns_frame = Frame(frame_btns, bg="white")
    green_btns_frame.pack()

    restart_btn = tk.Button(frame_btns, text="Restart", command=restart_btn_clicked, bg='orange')
    restart_btn.pack(side=LEFT, padx=20)

    exit_but = Button(frame_btns, text="Exit", command=exit_program, bg='#CD5C5C', fg='white')
    exit_but.pack(side=RIGHT, padx=20)

    add_green_btn(green_btns_frame)


def add_green_btn(frame):
    global add_all_btn, add_next_btn, color_path_btn
    add_next_btn = tk.Button(frame, text="Add Next Path", command=add_next_path_btn_clicked, bg='#8FBC8F',
                             fg='black')
    add_next_btn.pack(side=LEFT)

    color_path_btn = tk.Button(frame, text="Color Path", command=color_path_btn_clicked, bg='#8FBC8F', fg='black')
    color_path_btn.pack(padx=50, side=LEFT)
    color_path_btn.config(state="disabled")

    add_all_btn = tk.Button(frame, text="Add All", command=add_all_btn_clicked, bg='#8FBC8F', fg='black')
    add_all_btn.pack(side=LEFT)


def create_exit_button(tab):
    exit_but = Button(tab, text="Exit", command=exit_program, bg='#CD5C5C', fg='white')
    exit_but.pack(side=tk.RIGHT, padx=20)

# ############################ buttons tab2


def restart_btn_clicked():
    global canvas_tab1, network
    if not messagebox.askokcancel(title="Restart", message="Are you sure?"):
        return
    canvas_tab1.get_tk_widget().destroy()  # destroy and remake the tab

    network.reset_network()

    for path in lightpaths:  # remove all paths
        g.remove_edges_from([path])

    draw_network_to_run_alg(can_for_alg)

    add_next_btn.config(state="normal")
    add_all_btn.config(state="normal")
    color_path_btn.config(state=DISABLED)
    print("restart done")


def add_all_btn_clicked():
    if not network.colored:     # need to color this path first
        color_path_btn_clicked()
    while network.get_index() < len(network.lightpaths_list):
        add_next_path_btn_clicked()
        color_path_btn_clicked()
    print("all paths with colors")
    add_next_btn.config(state="disabled")
    add_all_btn.config(state="disabled")
    color_path_btn.config(state="disabled")
    ax.set_xlabel(f"Number of ADMs used : {len(network.adms_list)}", fontsize=13, labelpad=20, font="Times New Roman")
    canvas_tab1.draw()


def add_next_path_btn_clicked():
    add_next_btn.config(state="disabled")
    color_path_btn.config(state="normal")
    index_path = network.get_index()
    next_path_to_draw = network.get_lightpaths()[index_path]
    print(next_path_to_draw)
    if index_path < 4:
        draw_network.draw_paths_above_in_path(g, ax, NUMBER_OF_NODES, canvas_tab1, next_path_to_draw, 1, 2)  # in Draw file
    if index_path == 4:
        draw_network.draw_paths_above_in_path(g, ax, NUMBER_OF_NODES, canvas_tab1, next_path_to_draw, 2, 2)
    if index_path == 5:
        draw_network.draw_paths_above_in_path(g, ax, NUMBER_OF_NODES, canvas_tab1, next_path_to_draw, 3, 2)
    len_list = network.get_len_lightpaths_list()
    if index_path == len_list:  # disable buttons
        add_next_btn.config(state="disabled")
        add_all_btn.config(state="disabled")


def color_path_btn_clicked():
    if network.colored:  # if colored is true there is an error. should be false
        Exception("colored must be false")
    index_path = network.get_index()
    lightpath_to_color = network.get_lightpaths()[index_path]
    chosen_color = algorithm_minadm.color_lightpath(lightpath_to_color, nodes=NUMBER_OF_NODES, color_not_random=True, network=network)
    if index_path < 4:
        draw_network.color_paths_above_tab2(g, ax, canvas_tab1, lightpath_to_color, None, chosen_color, 1)  # in Draw file
    if index_path == 4:
        draw_network.color_paths_above_tab2(g, ax, canvas_tab1, lightpath_to_color, None, chosen_color, 2)
    if index_path == 5:
        draw_network.color_paths_above_tab2(g, ax, canvas_tab1, lightpath_to_color, None, chosen_color, 3)

    network.inc_index_in_paths_in_network()
    network.colored_true()
    print("colored lightpath", lightpath_to_color.start_node.node_id, ",", lightpath_to_color.end_node.node_id,
          "with color", chosen_color)
    color_path_btn.config(state="disabled")
    if network.get_index() < len(network.lightpaths_list):
        add_next_btn.config(state="normal")
    else:
        add_all_btn.config(state="disabled")
        ax.set_xlabel(f"Number of ADMs used : {len(network.adms_list)}", fontsize=13, labelpad=20,
                      font="Times New Roman")
        canvas_tab1.draw()
