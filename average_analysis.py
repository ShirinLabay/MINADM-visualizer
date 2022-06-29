import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import run_files
from AverageList import *
from ToolTip import *


'''
    Average analysis creates the third tab for both topologies
    - Displays 3D graph where X is the number of nodes, Y is the number of paths, and Z is the average ratio.
        Average ratio = average number of ADMs used / number of ADMs used in the optimal solution
        Creates an instance of AverageList to track the results for the graph for both topologies
        Reads results from "p_statistics1.txt" and "r_statistics1.txt"
        
    - Includes buttons to show different angles of the 3d graph. which can also be rotated manually
    
    - The left side of the tab is used for the user to input # of nodes the range of paths
        Example of an input - 
            # nodes = 5 and range of paths 5-7:
            The software will create the following networks
            - 5 nodes and 5 random paths = [[0, 2], [2, 4], [1, 3], [0, 3], [0, 4]]
                create a new network and in each iteration change the order of the paths 
                the order of the paths matter since the algorithm is online
                (changing the order is done 300 times - relevant mainly for bigger networks)
                get the average solution of these 300 networks and write it in statistics txt file 
            - 5 nodes and 6 random paths (same as above)
            - 5 nodes and 7 random paths (same as above)
        - The results are displayed for the user to see. The "add to graph" button adds the results to the 3d graph and 
        clears the results table 
        - The input is validated when generate button is clicked
        - when hovering on "?" sign and input boxs a description of the expected values are shown
'''

list_results = []


def create_average_tab(tab2, topology):
    global list_results
    list_results = AverageList()

    frame_left_side = Frame(tab2, width=300, height=100, highlightbackground="black", highlightthickness=1)
    frame_left_side.pack(side=LEFT, fill=Y)
    frame_left_side.grid_propagate(0)

    frame_for_buttons = Frame(tab2, height=30)
    frame_for_buttons.pack(side=BOTTOM, fill=X, pady=10)

    drawing_3d_canvas, toolbar = create_graph_3d(tab2, topology, azim=2, elev=-45)
    create_buttons_bottom_frame(frame_for_buttons, tab2, drawing_3d_canvas, toolbar, topology, frame_left_side)

    create_left_side(frame_left_side, tab2, topology, drawing_3d_canvas, toolbar, frame_for_buttons)

# ############### 3d graph


def create_graph_3d(tab2, topology, azim, elev):
    fig = Figure(figsize=(9, 6.5))
    drawing_3d_canvas = FigureCanvasTkAgg(fig, tab2)
    drawing_3d_canvas.draw()

    ax = create_ax(fig)
    file = create_file_name(topology)
    try:
        f_read = open(file, 'r')
    except IOError:
        print("Error - Could not open file!")
        return -1

    f_read.readline()
    lines = f_read.readlines()
    list_of_points = []
    for line in lines:
        x, y, z = get_xyz(line)
        point = [x, y, z]
        if point not in list_of_points:
            list_of_points.append(point)
            if topology == 'path':
                if 1 <= z <= 1.05:
                    color = '#FA8072'               # light red
                elif 1.05 < z <= 1.15:
                    color = '#FF0000'           # red
                else:           # 1.15 < z < 1.5
                    color = '#8B0000'           # dark red
            if topology == 'ring':
                if 1 <= z <= 1.2:
                    color = '#FA8072'               # light red
                elif 1.2 < z <= 1.275:
                    color = '#FF0000'           # red
                else:           # 1.275 < z < 1.75
                    color = '#8B0000'           # dark red
            b = ax.scatter(x, y, z, c=color)

    ax.view_init(azim, elev)  # initial view

    toolbar = NavigationToolbar2Tk(drawing_3d_canvas, tab2)
    toolbar.update()
    drawing_3d_canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)

    f_read.close()
    return drawing_3d_canvas, toolbar


def create_ax(fig):
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("Average Analysis", size=25, font="Maiandra GD")
    ax.set_xlabel("(X) Number of nodes", font="Times New Roman")
    ax.set_ylabel("(Y) Number of paths", font="Times New Roman")
    ax.set_zlabel("(Z) Ratio", font="Times New Roman")  # ratio between avg number of ADMs used
    return ax


def create_file_name(topology):
    if topology == 'path':
        file = 'networks_txt/path/p_statistics1.txt'
    elif topology == 'ring':
        file = 'networks_txt/ring/r_statistics1.txt'
    else:
        Exception("topology does not exist")
        return -1
    return file


def get_xyz(line):
    splitt = str(line.replace("\\", " "))
    splitt = splitt.replace("\n", " ")
    splitt = splitt.split(" ")
    x_num_nodes = int(splitt[1])
    y_num_paths = int(splitt[2])
    z_ratio = float(splitt[5])
    return x_num_nodes, y_num_paths, z_ratio

# ################ bottom frame for view buttons


def create_buttons_bottom_frame(frame_for_buttons, tab2, drawing_3d_canvas, toolbar, topology, frame_left_side):
    blue_btns_frame = Frame(frame_for_buttons)

    blue_btns(blue_btns_frame, tab2, drawing_3d_canvas, toolbar, topology, frame_for_buttons, frame_left_side)

    exit_btn = Button(frame_for_buttons, text="Exit", bg="#CD5C5C", fg='white', command=lambda: exit_program())
    exit_btn.pack(side=tk.RIGHT, padx=20)
    blue_btns_frame.pack()


def blue_btns(blue_btns_frame, tab2, drawing_3d_canvas, toolbar, topology, frame_for_buttons, frame_left_side):
    Button(blue_btns_frame, text="Show X-Y-Z", bg='light blue',
           command=lambda: reset_(drawing_3d_canvas, toolbar, tab2, topology, frame_for_buttons, frame_left_side
                                  , 2, -45)).pack(side=LEFT, padx=10)
    Button(blue_btns_frame, text="Show X-Y", bg='light blue',
           command=lambda: reset_( drawing_3d_canvas, toolbar, tab2, topology, frame_for_buttons, frame_left_side
                                   , 88, -90)).pack(side=LEFT, padx=10)
    Button(blue_btns_frame, text="Show X-Z", bg='light blue',
           command=lambda: reset_(drawing_3d_canvas, toolbar, tab2, topology, frame_for_buttons, frame_left_side
                                  , 0, 92)).pack(side=LEFT, padx=10)
    Button(blue_btns_frame, text="Show Y-Z", bg='light blue',
           command=lambda: reset_(drawing_3d_canvas, toolbar, tab2, topology, frame_for_buttons, frame_left_side
                                  , 0, 1)).pack(side=LEFT, padx=10)


def reset_(drawing_3d_canvas, toolbar, tab, topology, frame_for_buttons, frame_left_side, azim, elev):
    frame_for_buttons.destroy()
    drawing_3d_canvas.get_tk_widget().destroy()
    toolbar.destroy()

    frame_for_buttons = Frame(tab, height=30)
    frame_for_buttons.pack(side=BOTTOM, fill=X, pady=10)
    fig, toolbar = create_graph_3d(tab, topology, azim, elev)
    create_buttons_bottom_frame(frame_for_buttons, tab, fig, toolbar, topology, frame_for_buttons)

# ################ left frame for user input


def create_left_side(frame_left_side, tab2, topology, drawing_3d_canvas, toolbar, frame_for_buttons):
    Label(frame_left_side, text="Generate new network", font=("Times", 12)).grid(row=0, column=0, pady=10)
    label_q = Label(frame_left_side, text="?", font=('Times', 15))
    label_q.grid(row=0, column=3, padx=5, pady=5)
    if topology == 'path':
        create_tooltip(label_q, text='Generate new network for every # of paths in range'
                                     '\nThe ratio in results table is between the average solution '
                                     'and the optimal solution'
                                     '\n\nNote: The competitive ratio in path topology is 1.5')
    if topology == 'ring':
        create_tooltip(label_q, text='Generate new network for every # of paths in range'
                                     '\nThe ratio in results table is between the average solution '
                                     'and the optimal solution'
                                     '\n\nNote: The competitive ratio in ring topology is 1.75')
    Label(frame_left_side, text="Number of nodes: ", font=("Times", 12)).grid(row=1, column=0, padx=5)
    num_nodes_lbl = Entry(frame_left_side, width=10)
    num_nodes_lbl.grid(row=1, column=1, columnspan=2)
    create_tooltip(num_nodes_lbl, text='Should be a number grater than 3'
                                       '\n Please note that the grater is it the longer it might take to get results')

    Label(frame_left_side, text="Number of paths: ", font=("Times", 12)).grid(row=2, column=0)
    paths_from_lbl = Entry(frame_left_side, width=5)
    paths_from_lbl.grid(row=2, column=1, padx=5)
    create_tooltip(paths_from_lbl, text='Should be a number grater than 0')

    Label(frame_left_side, text="to", font=("Times", 12)).grid(row=2, column=2)
    paths_to_lbl = Entry(frame_left_side, width=5)
    paths_to_lbl.grid(row=2, column=3, padx=5)
    create_tooltip(paths_to_lbl, text='Should be a number grater than the start of range'
                                      '\nPlease note that the bigger the range is the longer '
                                      'it might take to get results')

    Label(frame_left_side, text="Results table", font=("Times", 12)).grid(row=4, column=0, columnspan=4, pady=10)

    sub_frame = Frame(frame_left_side, bd=5, bg="white", width=200, height=350, borderwidth=1, border=True)

    add_to_3d_btn = Button(frame_left_side, text="Add to graph", bg="light pink", command=lambda: add_to_3d_clicked(tab2, topology))
    add_to_3d_btn.grid(row=36, column=1, columnspan=2, pady=10)
    add_to_3d_btn.config(state=DISABLED)

    Button(frame_left_side, text="Clear", bg="light pink", command=lambda: clear_btn_clicked(topology, sub_frame, add_to_3d_btn)) \
        .grid(row=36, column=0, columnspan=2, pady=10)

    sub_frame.grid(row=5, column=0, columnspan=4, rowspan=30, pady=5, padx=50)
    sub_frame.grid_propagate(0)
    Label(sub_frame, text="  # of nodes  | ", bg="white").grid(row=0, column=0)
    Label(sub_frame, text="# of paths  | ", bg="white").grid(row=0, column=1)
    Label(sub_frame, text="Ratio ", bg="white").grid(row=0, column=2)

    Button(frame_left_side, text="Generate", bg="light pink", command=lambda: generate_btn_clicked(
        sub_frame, num_nodes_lbl, paths_from_lbl, paths_to_lbl,
        topology, drawing_3d_canvas, toolbar, tab2, frame_for_buttons, frame_left_side, add_to_3d_btn)).grid(row=3, column=0, columnspan=4, pady=20)

    generate_avg(topology)

    Label(frame_left_side, text=f"The average ratio is {list_results.get_avg_ratio(topology)}", font=("Ariel", 10, "bold")).grid(row=37, column=0, pady=10)
    avg_ratio_explanation = Label(frame_left_side, text="?", font=('Times', 12, "bold"))
    avg_ratio_explanation.grid(row=37, column=3, padx=5, pady=5)
    create_tooltip(avg_ratio_explanation, text='The average ratio is the ratio between the average solution and the '
                                               'optimal solution')


def generate_avg(topology):
    global list_results
    statistics_file = create_file_name(topology)
    read_file = open(statistics_file, 'r')
    read_file.readline()        # the first line
    lines = read_file.readlines()
    count_results = len(lines)
    print(f"number of lines in statistics file in {topology} is {count_results}")

    sum = 0
    for line in lines:
        x, y, z = get_xyz(line)
        sum = sum + z

    print(f"sum of results statistics file in {topology} is {sum}")
    average = sum / count_results
    average = round(average, 2)
    print(f"the average in {topology} is {average}")
    list_results.set_avg_ratio(topology, average)

    read_file.close()


def add_to_3d_clicked(tab2, topology):
    if tk.messagebox.askokcancel(title='WARNING', message='\nAdding results to 3d graph will also clear results table'
                                                          '\nClick OK to continue'):
        print("clicked")
        for widget in tab2.winfo_children():
            widget.destroy()
        create_average_tab(tab2, topology)


def generate_btn_clicked(sub_frame, num_nodes_lbl, paths_from_lbl, paths_to_lbl, topology, drawing_3d_canvas, toolbar, tab2, frame_for_buttons, frame_left_side, add_to_3d_btn):  # gets strings
    add_to_3d_btn.config(state=NORMAL)
    num_nodes_str = num_nodes_lbl.get()
    paths_from_str = paths_from_lbl.get()
    paths_to_str = paths_to_lbl.get()
    if num_nodes_str == "":
        tk.messagebox.showerror(title='ERROR', message='Number of nodes can not be empty')
        return -1
    if not paths_from_str or not paths_to_str:
        tk.messagebox.showerror(title='ERROR', message='Number of paths range can not be empty')
        return -1
    if not num_nodes_str.isdigit() or not paths_from_str.isdigit() or not paths_to_str.isdigit():
        tk.messagebox.showerror(title='ERROR', message='Values must be numbers')
        return -1
    if not valid_numbers(int(num_nodes_str), int(paths_from_str), int(paths_to_str)):
        return -1
    if int(num_nodes_str) > 200:
        if not tk.messagebox.askokcancel(title='WARNING', message='Network size is big. Results may take a lone time'
                                                                  '\nAre you sure you want to continue?'):
            return
    print("clicked add", str(num_nodes_str), str(paths_from_str), str(paths_to_str))
    # build and run network, display results in sub frame
    l_temp = run_files.build_and_run_range(num_nodes_str, paths_from_str, paths_to_str, topology)
    for l in l_temp:
        list_results.add_to_list(l, topology)
    display_sub_frame(sub_frame, topology)
    empty_entry(num_nodes_lbl)
    empty_entry(paths_from_lbl)
    empty_entry(paths_to_lbl)
    # reset_(drawing_3d_canvas, toolbar, tab2, topology, frame_for_buttons, frame_left_side, 2, -45)


def empty_entry(e):
    e.delete(0, END)
    e.insert(0, "")


def display_sub_frame(frame, topology):
    list1 = list_results.get_list(topology)
    for i in range(len(list1)):
        Label(frame, text=list1[i][0], bg="white").grid(row=i + 1, column=0)  # num nodes
        Label(frame, text=list1[i][1], bg="white").grid(row=i + 1, column=1)  # num paths
        Label(frame, text=list1[i][2], bg="white").grid(row=i + 1, column=2)  # ratio


def valid_numbers(num_node, paths_from, paths_to):  # gets ints
    if paths_from == 0 or paths_to == 0:
        tk.messagebox.showerror(title='ERROR', message='Number of paths should be grater than 0')
        return False
    if paths_to < paths_from:
        tk.messagebox.showerror(title='ERROR', message='End of range should be grater than start value')
        return False
    if num_node < 3:
        tk.messagebox.showerror(title='ERROR', message='Number of nodes should be grater than 3')
        return False
    if paths_to - paths_from > 10:
        if not tk.messagebox.askokcancel(title='WARNING',
                                         message='Paths range is over 10. Results may take a lone time'
                                                 '\nAre you sure you want to continue?'):
            return False
    if paths_to == paths_from:
        if not tk.messagebox.askokcancel(title='WARNING',
                                         message='Range size is 1'
                                                 '\nAre you sure you want to continue?'):
            return False
    return True


def clear_btn_clicked(topology, sub_frame, add_to_3d_btn):
    if not tk.messagebox.askokcancel(title='WARNING', message='\nAre you sure you want to clear all results?'):
        return
    add_to_3d_btn.config(state=DISABLED)
    list_results.reset_list(topology)
    for widget in sub_frame.winfo_children():
        widget.destroy()
    Label(sub_frame, text="  # of nodes  | ", bg="white").grid(row=0, column=0)
    Label(sub_frame, text="# of paths  | ", bg="white").grid(row=0, column=1)
    Label(sub_frame, text="Ratio ", bg="white").grid(row=0, column=2)

# ############ exit is used in main, path and ring topology


def exit_program():
    if tk.messagebox.askokcancel(title='Exit', message='Are you sure ?'):
        quit()
    else:
        return