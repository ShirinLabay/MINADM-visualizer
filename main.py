import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from PIL import Image
from PIL.ImageTk import PhotoImage
from average_analysis import exit_program
import path_topology
import ring_topology

'''
    The main file - make a Tk window for gui and opens the welcome tab
    3 tabs - welcome, path topology and ring topology
'''


def clicked_path(e):
    print("clicked path")
    tabControl.select(tab_path)


def clicked_ring(e):
    print("clicked ring")
    tabControl.select(tab_ring)


window = tk.Tk()
window.geometry("1190x720")
window.title("ONLINE-MINADM Algorithm Visualizer")
window.iconphoto(True, tk.PhotoImage(file='logo.png'))
window.resizable(True, True)

s = ttk.Style()
s.configure('TNotebook', tabposition='n')

style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='nw')

tabControl = ttk.Notebook(window, style='lefttab.TNotebook')

s = ttk.Style()
s.configure('new.TFrame', background='white')

tab_welcome = ttk.Frame(tabControl, style='new.TFrame')
tab_path = ttk.Frame(tabControl)
tab_ring = ttk.Frame(tabControl)

tabControl.add(tab_welcome, text="Welcome")
tabControl.add(tab_path, text="Path Topology")
tabControl.add(tab_ring, text="Ring Topology")
tabControl.pack(expand=1, fill="both")


# welcome to tab
im_temp = Image.open("logo.png")
im_temp = im_temp.resize((70, 70), Image.ANTIALIAS)
img = PhotoImage(image=im_temp)
ttk.Label(tab_welcome, image=img, background="white").pack(pady=30)
ttk.Label(tab_welcome, text="Welcome!", font=('Tempus Sans ITC', 30), background="white").pack(pady=20)
ttk.Label(tab_welcome, text="ONLINE-MINADM Algorithm Visualizer", font=("Maiandra GD", 20), background="white")\
    .pack(pady=50)
ttk.Label(tab_welcome, text="Select Topology To Start Visualization", font=("Times", 15), background="white")\
    .pack(pady=20)

labels_style = ttk.Style()
labels_style.configure("new.TLabel", font=("Times", 15, "underline"), background="white")


l1 = ttk.Label(tab_welcome, text="Path Topology", style="new.TLabel", cursor="hand2")
l2 = ttk.Label(tab_welcome, text="Ring Topology", style="new.TLabel", cursor="hand2")
l1.bind('<Button-1>', clicked_path)
l2.bind('<Button-1>', clicked_ring)
l1.pack()
l2.pack()

myFont = font.Font(family='Times', size=15)
exit_button = tk.Button(tab_welcome, text="Exit", command=exit_program, bg='#CD5C5C', fg='white')
exit_button['font'] = myFont
exit_button.pack(side=tk.BOTTOM, pady=50)

path_topology.create_path_notebook(tab_path)
ring_topology.create_ring_notebook(tab_ring)


window.mainloop()
