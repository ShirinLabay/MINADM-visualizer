from user_tab_ring import *
from tkinter import ttk, messagebox
import algorithm_minadm
from average_analysis import *
from user_tab_ring import *
import matplotlib
import matplotlib.pyplot as plt
import tkinter.font as font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import draw_network
from Network import *

matplotlib.use('TkAgg')

'''
    create all 3 tabs in ring topology
    tab 1 - user can build a custom network and run the algorithm
    tab 2 - example of an optimal solution and solution of the algorithm
    tab 3 - show 3d graph in different angles, also user can add to statistics 
'''


def create_ring_notebook(frame):
    notebook_ring = ttk.Notebook(frame)
    tab1 = Frame(notebook_ring)  # ring topology
    optimal_tab2 = Frame(notebook_ring)  # optimal solution
    average_tab3 = Frame(notebook_ring)  # statistics
    notebook_ring.add(tab1, text="Algorithm Visualization")
    notebook_ring.add(optimal_tab2, text="Optimal Solution")
    notebook_ring.add(average_tab3, text="Average Analysis")
    notebook_ring.pack(expand=True, fill="both")

    create_left_user_frame_r(tab1)
    make_bottom_frame(tab1)
    create_init_tab1_drawing(tab1)

    create_tab2(optimal_tab2)

    create_average_tab(average_tab3, 'ring')


# ############### tab 2 ring


def create_tab2(tab2):      # make two frames
    global tab22, canvas_alg
    tab22 = tab2
    frame_optimal = Frame(tab2)
    frame_optimal.pack(side=LEFT, fill=BOTH, expand=True)

    bottom_frame_empty = Frame(frame_optimal, height=50, bg="white")        # this frame is empty - it is only for
    # getting the same frame size in tab 2 ring
    bottom_frame_empty.pack(side=BOTTOM, fill=BOTH, expand=False)

    frame_alg = Frame(tab2)
    frame_alg.pack(side=RIGHT, fill=BOTH, expand=True)

    can_for_optimal = Canvas(frame_optimal)  # , background="pink")
    can_for_optimal.pack(fill=BOTH, expand=True, padx=3)
    can_for_optimal.pack_propagate(0)

    can_for_alg = Canvas(frame_alg)  # , background="white")

    # frame for visualization buttons
    bottom_frame_btns = Frame(frame_alg, height=50, bg="white")
    bottom_frame_btns.pack(side=BOTTOM, fill=BOTH, expand=False)
    add_tab2_bottom_buttons(bottom_frame_btns)
    bottom_frame_btns.pack_propagate(0)

    can_for_alg.pack(fill=BOTH, expand=True, padx=3)
    can_for_alg.pack_propagate(0)

    making_optimal(can_for_optimal)

    draw_run_algorithm_tab2(can_for_alg)  # tab 2


def add_tab2_bottom_buttons(frame):
    green_btns_frame = Frame(frame, bg="white")
    green_btns_frame.pack()

    exit_but = Button(frame, text="Exit", command=exit_program, bg='#CD5C5C', fg='white')
    exit_but.pack(side=RIGHT, padx=10)

    add_green_btn(green_btns_frame)


def add_green_btn(frame):
    global add_all_btn_ring, add_next_btn_ring, color_path_btn_ring

    restart_btn = tk.Button(frame, text="Restart", command=restart, bg='orange')
    restart_btn.pack(padx=20, side=LEFT)

    add_next_btn_ring = tk.Button(frame, text="Add Next Path", command=button_click_add_path_onebyone, bg='#8FBC8F',
                                 fg='black')
    add_next_btn_ring.pack(padx=20, side=LEFT)

    color_path_btn_ring = tk.Button(frame, text="Color Path", command=color_path, bg='#8FBC8F', fg='black')
    color_path_btn_ring.pack(padx=20, side=LEFT)
    color_path_btn_ring.config(state="disabled")

    add_all_btn_ring = tk.Button(frame, text="Add All", command=button_click_add_all_paths, bg='#8FBC8F', fg='black')
    add_all_btn_ring.pack(padx=20,side=LEFT)


# ######## handle buttons tab2

def button_click_add_path_onebyone():
    add_next_btn_ring.config(state="disabled")
    color_path_btn_ring.config(state="normal")
    index_ring = network_ring.get_index()
    next_path_to_draw = network_ring.get_lightpaths()[index_ring]
    if index_ring < 5:
        draw_network.draw_paths_in_circle(g_ring, ax_ring, 10, canvas_tab22, next_path_to_draw, 1, 2)
    if index_ring > 4:
        draw_network.draw_paths_in_circle(g_ring, ax_ring, 10, canvas_tab22, next_path_to_draw, 2, 2)
    len_list = network_ring.get_len_lightpaths_list()
    if index_ring == len_list:  # disable buttons
        add_next_btn_ring.config(state="disabled")
        add_all_btn_ring.config(state="disabled")


def button_click_add_all_paths():
    if not network_ring.colored:     # need to color this path first
        color_path()
    while network_ring.get_index() < len(network_ring.lightpaths_list):
        button_click_add_path_onebyone()
        color_path()
    print("all paths with colors")
    add_next_btn_ring.config(state="disabled")
    color_path_btn_ring.config(state="disabled")
    add_all_btn_ring.config(state="disabled")
    ax_ring.set_xlabel(f"Number of ADMs used : {len(network_ring.adms_list)}", fontsize=13, labelpad=20)
    canvas_tab22.draw()


def restart():
    global canvas_tab22, network_ring
    if not messagebox.askokcancel(title="Restart", message="Are you sure?"):
        return
    canvas_tab22.get_tk_widget().destroy()  # destroy and remake the tab
    network_ring.reset_network()

    for path in lightpaths_ring:  # remove all paths
        g_ring.remove_edges_from([path])

    draw_run_algorithm_tab2(tab_new)

    add_next_btn_ring.config(state="normal")
    color_path_btn_ring.config(state=DISABLED)
    add_all_btn_ring.config(state=NORMAL)
    print("restart done")


def color_path():
    if network_ring.colored:  # if colored is true there is an error. should be false
        Exception("colored must be false")
    index_ring = network_ring.get_index()
    lightpath_to_color = network_ring.get_lightpaths()[index_ring]
    chosen_color = algorithm_minadm.color_lightpath(lightpath_to_color, nodes=NUMBER_OF_NODES,
                                                    color_not_random=True, network=network_ring)
    if index_ring < 5:
        draw_network.color_path_ring(g_ring, ax_ring, NUMBER_OF_NODES, canvas_tab22, lightpath_to_color,
                                     None, chosen_color, 1)  # in colored path
    if index_ring > 4:
        draw_network.color_path_ring(g_ring, ax_ring, NUMBER_OF_NODES, canvas_tab22, lightpath_to_color,
                                     None, chosen_color, 2)  # in colored path

    network_ring.inc_index_in_paths_in_network()
    network_ring.colored_true()
    print("colored lightpath", lightpath_to_color.start_node.node_id, ",", lightpath_to_color.end_node.node_id,
          "with color", chosen_color)
    # add_all_btn_ring.config(state="disabled")
    if network_ring.get_index() < len(network_ring.lightpaths_list):
        add_next_btn_ring.config(state="normal")
    else:
        color_path_btn_ring.config(state="disabled")
        ax_ring.set_xlabel(f"Number of ADMs used : {len(network_ring.adms_list)}", fontsize=13, labelpad=20)
        canvas_tab22.draw()

# ####### algorithm tab 2


def draw_run_algorithm_tab2(tab2):
    global ax_ring, f_ring, tab_new, canvas_tab22
    tab_new = tab2
    num1 = NUMBER_OF_NODES
    f_ring = plt.Figure(figsize=(1, num1))
    f_ring.suptitle('Run The Algorithm', size=15, font="Maiandra GD")
    ax_ring = f_ring.add_subplot(6, 1, (1, 5))
    ax_ring.set_xlabel("Number of ADMs used : ?", fontsize=13, labelpad=20)
    create_network_ring()
    canvas_tab22 = FigureCanvasTkAgg(f_ring, tab2)
    canvas_tab22.get_tk_widget().pack(fill="both", expand=True)
    canvas_tab22.draw()


def create_network_ring():
    global network_ring, lightpaths_ring
    global g_ring, pos_ring
    network_ring = Network("ring", NUMBER_OF_NODES)
    g_ring, pos_ring = draw_network.draw_circle_graph(NUMBER_OF_NODES, ax_ring,0)
    lightpaths_ring = [[0, 1], [5, 6], [1, 2], [7, 8], [3, 4], [8, 9], [4, 6], [9, 0]]
    network_ring.add_paths_to_network(lightpaths_ring)


# ############### tab 2 optimall


def making_optimal(can6):
    global ax6
    num1 = NUMBER_OF_NODES
    f6 = plt.Figure(figsize=(1, num1))
    f6.suptitle('The Optimal Solution', size=15, font="Maiandra GD")
    ax6 = f6.add_subplot(6, 1, (1, 5))
    ax6.set_xlabel("Number of ADMs used : 11", fontsize=13, labelpad=20)

    g6, pos_ring6 = draw_network.draw_circle_graph(NUMBER_OF_NODES, ax6, 0)

    canvas_tab2 = FigureCanvasTkAgg(f6, can6)
    canvas_tab2.get_tk_widget().pack(fill=BOTH, expand=True)
    canvas_tab2.draw()
    draw_network.color_paths_in_circle_optimal(ax6)
    canvas_tab2.draw()