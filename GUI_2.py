from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from functools import partial
from pluscoolquecool import main_function
import SMWdrawer


###############
# GUI CLASSES #
###############
class MiniWindow(Frame):
    def __init__(self, title):
        Frame.__init__(self, root)
        self.config(highlightbackground="black", highlightthickness=3, background=aseprite_blue)
        self.bind("<Button-1>", self.drag_start)
        self.bind("<B1-Motion>", self.drag_motion)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        self.title_label = ttk.Label(self, text="   " + title, background=aseprite_blue, foreground="white",
                                     font=main_font_medium)
        self.title_label.grid(row=0, column=0, sticky="W")
        self.quit_button = ttk.Button(self, text="x", command=self.destroy)
        self.quit_button.grid(row=0, column=1, padx=7, pady=7)
        self.main_label = Frame(self, borderwidth=2, padx=10, pady=10, background=aseprite_ecru)
        self.main_label.grid(row=1, column=0, columnspan=2)

    def drag_start(self, e):
        widget = e.widget
        widget.startX = e.x
        widget.startY = e.y

    def drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget.startX + event.x
        y = widget.winfo_y() - widget.startY + event.y
        widget.place(anchor="nw", x=x, y=y)


#############
# UI FUNCTIONS #
#############

def new():
    global show

    def get_file():
        new_file = askopenfilename(parent=main_frame, filetype=[("wav file", "*.wav")], title="Choose a file")
        if new_file != "":
            filevar.set(new_file)
            ok_button["state"] = "enabled"
        else:
            ok_button["state"] = "disabled"

    def ok():
        go(filevar.get(), int(fs.get()), int(hs.get()), title_entry.get(), NUM.get(), DEN.get())
        filevar.set("")
        main_frame.destroy()

    def hideorshow():
        global show
        show = not show
        if show:
            advanced_lab1.grid(row=const_row_pos + 1, column=0, columnspan=column_number, sticky="W")
            advanced_lab2.grid(row=const_row_pos + 2, column=0)
            advanced_lab3.grid(row=const_row_pos + 2, column=2)
            advanced_fs.grid(row=const_row_pos + 3, column=0)
            advanced_hs.grid(row=const_row_pos + 3, column=2)
        else:
            advanced_lab1.grid_remove()
            advanced_lab2.grid_remove()
            advanced_lab3.grid_remove()
            advanced_fs.grid_remove()
            advanced_hs.grid_remove()

    main_frame = MiniWindow("New Sheet Music")

    ######################
    # MAIN FRAME CONTENT #
    ######################
    column_number = 3
    row_number = 16
    for k in range(column_number):
        main_frame.main_label.columnconfigure(k, weight=1)
    for k in range(row_number):
        main_frame.main_label.rowconfigure(k, weight=1)

    # FILE CHOICE
    row_pos = 0
    file_lab1 = Label(main_frame.main_label, height=1, wraplength=250,
                      text=".wav File",
                      background=aseprite_ecru, foreground=aseprite_darkblue, font=main_font_medium)
    file_lab1.grid(row=row_pos + 0, column=0, columnspan=column_number, sticky="W")
    file_button = ttk.Button(main_frame.main_label, text="Browse", command=get_file)
    file_button.grid(row=row_pos + 1, column=0, columnspan=column_number)
    file_lab2 = Label(main_frame.main_label, textvariable=filevar, width=35, height=2, wraplength=250,
                      background=aseprite_ecru,
                      relief="ridge")
    file_lab2.grid(row=row_pos + 2, column=0, columnspan=column_number)
    void1 = Label(main_frame.main_label, background=aseprite_ecru, height=1)
    void1.grid(row=row_pos + 3)

    # TITLE CHOICE
    row_pos = 4
    title_lab1 = Label(main_frame.main_label, height=1, wraplength=250,
                       text="Title",
                       background=aseprite_ecru, foreground=aseprite_darkblue, font=main_font_medium)
    title_lab1.grid(row=row_pos + 0, column=0, columnspan=column_number, sticky="W")
    title_entry = ttk.Entry(main_frame.main_label, width=35, justify=CENTER, font=main_font_medium)
    title_entry.grid(row=row_pos + 1, column=0, columnspan=column_number)
    void2 = Label(main_frame.main_label, background=aseprite_ecru, height=1)
    void2.grid(row=row_pos + 2)

    # METER CHOICE
    row_pos = 7
    NUM = IntVar()
    DEN = IntVar()
    NUM.set(4)
    DEN.set(4)
    NUM_options = list(range(1, 17))
    DEN_options = [2, 4, 8, 16]
    meter_lab1 = Label(main_frame.main_label, height=1, wraplength=250,
                       text="Meter",
                       background=aseprite_ecru, foreground=aseprite_darkblue, font=main_font_medium)
    meter_lab1.grid(row=row_pos + 0, column=0, columnspan=column_number, sticky="W")
    meter_choice1 = OptionMenu(main_frame.main_label, NUM, *NUM_options)
    meter_choice1.grid(row=row_pos + 1, column=0)
    meter_lab2 = Label(main_frame.main_label, text="/", background=aseprite_ecru, foreground="black",
                       font=main_font_big)
    meter_lab2.grid(row=row_pos + 1, column=1)
    meter_choice2 = OptionMenu(main_frame.main_label, DEN, *DEN_options)
    meter_choice2.grid(row=row_pos + 1, column=2)
    void3 = Label(main_frame.main_label, background=aseprite_ecru, height=1)
    void3.grid(row=row_pos + 2)

    # ADVANCED OPTIONS
    const_row_pos = 10
    advanced_check = Checkbutton(main_frame.main_label, text="Advanced Options", font=main_font_medium,
                                 background=aseprite_ecru,
                                 command=hideorshow)
    advanced_check.grid(row=const_row_pos + 0, column=0, columnspan=column_number, sticky="W")

    advanced_lab1 = Label(main_frame.main_label, height=1, wraplength=250,
                          text="Fourier Transform",
                          background=aseprite_ecru, foreground=aseprite_darkblue, font=main_font_medium)
    advanced_lab2 = ttk.Label(main_frame.main_label, text="Frame Size", background=aseprite_ecru, foreground="black")
    advanced_lab3 = ttk.Label(main_frame.main_label, text="Hop Size", background=aseprite_ecru, foreground="black")

    frame_sizes = [1024, 2048, 4096]
    fs = StringVar(root)
    fs.set(frame_sizes[0])
    advanced_fs = OptionMenu(main_frame.main_label, fs, *frame_sizes)

    hop_sizes = [128, 256, 512]
    hs = StringVar(root)
    hs.set(hop_sizes[0])
    advanced_hs = OptionMenu(main_frame.main_label, hs, *hop_sizes)

    # OK AND CANCEL BUTTONS
    row_pos = 14
    void4 = Label(main_frame.main_label, background=aseprite_ecru, height=1)
    void4.grid(row=row_pos + 0)
    ok_button = ttk.Button(main_frame.main_label, text="OK", command=ok, state=DISABLED)
    ok_button.grid(row=row_pos + 1, column=0)
    cancel_button = ttk.Button(main_frame.main_label, text="Cancel", command=main_frame.destroy)
    cancel_button.grid(row=row_pos + 1, column=2)

    # START MAIN FRAME
    main_frame.place(x=(root.winfo_width() / 2) - 192,
                     y=(root.winfo_height() / 2) - 300)


def go(file, frame_size, hop_size, title, num, den):
    liste = main_function(file, frame_size, hop_size)
    open_tab(file, liste, title, num, den)


def open_file():
    file = askopenfilename(parent=root, filetype=[("text_file", "*.txt")], title="Choose a file")
    if file != "": open_tab(file, file)


def open_tab(filename, note_list=None, chosen_title=None, num=None, den=None):
    tab = ttk.Frame(nb, padding=30)
    ##################
    # OPEN TEXT FILE #
    ##################
    if filename[filename.rfind(".") + 1:] == "txt":
        def myfunction(event):
            can.configure(scrollregion=can.bbox("all"), width=200, height=200)

        text_file = open(filename)
        data = text_file.read()
        text_file.close()

        can = Canvas(tab, background=aseprite_ecru)
        fr = Frame(can, background=aseprite_ecru)
        myscrollbar = Scrollbar(tab, orient="vertical", command=can.yview)
        can.configure(yscrollcommand=myscrollbar.set)

        while data.find("\n/separator\n") != -1:
            text_lab = ttk.Label(fr, text=data[:data.find("\n/separator\n")], anchor="nw", wraplength=1750)
            text_lab.pack(fill=X, side=TOP)
            sep = ttk.Separator(fr, orient="horizontal")
            sep.pack(fill=X, side=TOP)
            data = data[data.find("\n/separator\n") + 12:]

        text_lab = ttk.Label(fr, text=data, anchor="nw", wraplength=1750)
        text_lab.pack(fill=X, side=TOP)

        fr.pack(expand=True, fill=BOTH)
        myscrollbar.pack(expand=False, fill=Y, side=RIGHT)
        can.pack(side="left", expand=True, fill=BOTH)
        can.create_window((0, 0), window=fr, anchor='nw')
        fr.bind("<Configure>", myfunction)

        title = filename[filename.rfind("/") + 1:filename.rfind(".")]

    ###################
    # NEW SHEET MUSIC #
    ###################
    elif filename[filename.rfind(".") + 1:] == "wav":
        if chosen_title == "":
            title = filename[filename.rfind("/") + 1:filename.rfind(".")]
        else:
            title = chosen_title
        SMWdrawer.start(note_list, num, den, tab, title)

    ##############################
    # FILE EXTENSION NOT MANAGED #
    ##############################
    else:
        return
    nb.add(tab, text=title)
    nb.select(tab)


def about():
    About = MiniWindow("About SMW5")
    msg = "Sheet Music Writer 5000 - alpha version/separatorSheet Music editor & generator from audio files"

    while msg.find("/separator") != -1:
        text_lab = ttk.Label(About.main_label, text=msg[:msg.find("/separator")], justify=LEFT,
                             background=aseprite_ecru, font=main_font_medium)
        text_lab.pack(side=TOP, fill="x")
        msg = msg[msg.find("/separator") + 10:]
        sep = ttk.Separator(About.main_label, orient="horizontal")
        sep.pack(fill="x")

    text_lab = ttk.Label(About.main_label, text=msg[:msg.find("/separator")], justify=LEFT, background=aseprite_ecru,
                         font=main_font_medium)
    text_lab.pack(side=TOP, fill="x")

    About.place(anchor=CENTER, x=(root.winfo_width() / 2) - (About.winfo_x() / 2),
                y=(root.winfo_height() / 2) - (About.winfo_y() / 2))


###################
# GUI MAIN WINDOW #
###################

root = Tk()
root.title("Sheet Music Writer 5000")
root.geometry("1250x600")

filevar = StringVar()
show = False

root.rowconfigure(0, weight=0)
root.columnconfigure(0, weight=0)
for i in range(1, 50):
    root.rowconfigure(i, weight=1)
    root.columnconfigure(i, weight=1)

nb = ttk.Notebook(root)
nb.grid(row=0, column=0, rowspan=50, columnspan=50, sticky="NESW")


#########
# STYLE #
#########
def color_config(widget, color, event):
    widget.configure(background=color)


style = ttk.Style()

main_font_small = ("Comic Sans MS", "11")
main_font_medium = ("Comic Sans MS", "13")
main_font_big = ("Comic Sans MS", "17")

aseprite_blue = "#7c8f9b"
aseprite_darkblue = "#354c8e"
aseprite_ecru = "#d1cabd"
aseprite_darkecru = "#938074"
aseprite_yellow = "#fdebb6"
aseprite_grey = "#c4c4c4"

style.theme_create("My Theme", parent="classic", settings={
    "TLabel": {
        "configure": {"font": main_font_medium, "background": aseprite_ecru}},
    "TFrame": {
        "configure": {"background": aseprite_blue}},
    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": aseprite_ecru, "borderwidth": 0}},
    "TNotebook.Tab": {
        "configure": {"padding": [5, 1], "background": aseprite_grey, "foreground": "black", "font": main_font_medium},
        "map": {"background": [("selected", aseprite_blue)],
                "foreground": [("selected", "white")],
                "expand": [("selected", [1, 1, 1, 0])]}},
    "TButton": {"configure": {"highlightthickness": 2},
                "map": {"highlightcolor": [("disabled", "lightgrey"), ('focus', 'black'), ('!focus', 'black')],
                        "background": [("disabled", "lightgrey"), ("pressed", aseprite_blue), ("active", "white"),
                                       ("!active", aseprite_ecru)],
                        "foreground": [("disabled", "grey"), ("pressed", "white"), ("active", "black"),
                                       ("!active", "black")]}},
    "TCheckbutton": {"configure": {"font": main_font_medium}, }})

style.theme_use("My Theme")

####################
# MAIN WINDOW MENU #
####################

menu = Menu(root)

menu_file = Menu(menu, tearoff=False)
menu_file.add_command(label="New", command=new)
menu_file.add_command(label="Open", command=open_file)
menu_file.add_separator()
menu_file.add_command(label="Save")
menu_file.add_command(label="Save as")
menu_file.add_command(label="Export")
menu_file.add_command(label="Close")
menu_file.add_command(label="Close All")
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.destroy)
menu.add_cascade(label="File", menu=menu_file)

menu_help = Menu(menu, tearoff=False)
menu_help.add_command(label="Readme", command=partial(open_tab, "README.txt"))
menu_help.add_separator()
menu_help.add_command(label="About", command=about)
menu.add_cascade(label="Help", menu=menu_help)

root.config(menu=menu)

####################
# HOME PAGE DESIGN #
####################

home = ttk.Frame(nb, padding=30)
for i in range(2):
    home.rowconfigure(i, weight=i)
    home.columnconfigure(i, weight=1)

history_frame = Frame(home, highlightbackground="black", highlightthickness=3, background="white")
history_label = ttk.Label(history_frame, text="History")
history_label.pack(side=TOP, fill="x")
his_list = ["1", "2", "3", "4", "5"]
for entry in his_list:
    lab = ttk.Label(history_frame, text=entry, justify=LEFT, background="white", font=main_font_small)
    lab.bind("<Button-1>", partial(open_tab, entry))
    lab.bind("<Enter>", partial(color_config, lab, aseprite_yellow))
    lab.bind("<Leave>", partial(color_config, lab, "white"))
    lab.pack(side=TOP, fill="x")

history_frame.grid(row=1, column=0, sticky="NESW")

nb.add(home, text="Home")

nb.select(home)
nb.enable_traversal()

root.state("zoomed")
root.mainloop()
