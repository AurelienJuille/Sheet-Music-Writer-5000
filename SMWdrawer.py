from tkinter import *
from tkinter import ttk, font
from PIL import ImageTk, Image
import warnings
import math


###########
# MUSIC CLASSES #
###########
class Note:
    """
    Note musicale
    start : départ de la note en nombre de noires depuis le début du morceau
    dur : durée de la note en nombre de noires
    pitch : pitch de la note
    """

    def __init__(self, start, dur, pitch):
        self.pitch = pitch
        self.start = start
        self.dur = dur


class Bar:
    """
    Mesure musicale
    start : départ de la mesure en nombre de noires depuis le début du morceau
    meter : décomposition de la mesure (numérateur, dénominateur)
    notes : liste des notes présentes dans la mesure
    """
    first_bar_offset = 5 * 20

    def __init__(self, start, meter, notes=None, first=False):
        self.start = start
        self.meter = meter
        self.notes = notes
        self.first = first

    def get_width(self):
        if self.first:
            w = self.first_bar_offset
        else:
            w = 0
        w += 50 * (self.meter[0] * 4 / self.meter[1]) / min([k.dur for k in self.notes]) if self.notes != [] else 50
        return w


class Score:
    def __init__(self, bars=[], liste=[]):
        self.bars = bars
        self.liste = liste

    def write_notes(self, notes):
        for n in notes:
            if n not in self.liste:
                self.liste.append(n)
        for bar in self.bars:
            for note in notes:
                if bar.start <= note.start < bar.start + 4 * bar.meter[0] / bar.meter[1]:
                    bar.notes.append(note)


###############
# GUI CLASSES #
###############
class SheetCanvas(ttk.Frame):
    def __init__(self, win):
        Frame.__init__(self, win)
        self.background = "black"
        self.padding = 30
        self.canvas = Canvas(self, width=2480, height=3508, background="grey")
        self.xsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        # linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        # windows scroll
        self.canvas.bind("<MouseWheel>", self.zoomer)

        self.fontSize = 300

    # move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    def zoomer(self, event):
        if event.delta > 0:
            # self.config(width=self.winfo_width() * 1.1, height=self.winfo_height() * 1.1)
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
            self.fontSize = self.fontSize * 1.1
        elif event.delta < 0:
            # self.config(width=self.winfo_width() * .9, height=self.winfo_height() * .9)
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
            self.fontSize = self.fontSize * 0.9
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        for child_widget in self.canvas.find_withtag("text"):
            self.canvas.itemconfigure(child_widget, font=("Comic Sans MS", int(self.fontSize)))
            # self.canvas.itemconfigure(child_widget, font=child_widget.get_font)

    # linux zoom
    def zoomerP(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoomerM(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


score = Score()
page_width = 2480
page_height = 3508
system_width = 2180
system_height = 300
dist_between_systems = 244
dist_between_lines = 22.5


def start(note_list, num, den, tab, title):
    maximum = 0
    liste = []
    for x in note_list:
        liste.append(Note(x[0], x[1], x[2]))
        maximum = max(maximum, x[0] + x[1])
    score.liste = liste
    for y in range(int((maximum * den / (4 * num))-.01) + 1):
        new_bar = Bar(y * num * (4/den), (num, den), [])
        score.bars.append(new_bar)

    score.write_notes(liste)

    can = SheetCanvas(tab)
    tab.rowconfigure(0, weight=1)
    tab.columnconfigure(0, weight=1)
    can.grid(row=0, column=0)

    draw_score(can.canvas, title)


def draw_score(can, title):
    can.create_rectangle(0, 0, page_width, page_height, fill="white")
    can.create_text(page_width / 2, 400, text=title, tags="text", font=font.Font(family="Comic Sans MS", size=300))
    can.create_line(0, 0, page_width, 0)
    can.create_line(0, page_height, page_width, page_height)
    can.create_line(0, 0, 0, page_height)
    can.create_line(page_width, 0, page_width, page_height)

    for k in range(1, 6):
        draw_system(can, k)

    somme = 0
    barstodraw = []
    line = 1
    for k, bar in enumerate(score.bars):
        if somme + bar.get_width() <= system_width:
            somme += bar.get_width()
            barstodraw.append(bar)
            if k == len(score.bars)-1:
                draw_bars(can, barstodraw, somme, line)
        else:
            draw_bars(can, barstodraw, somme, line)
            somme = bar.get_width()
            barstodraw = []
            line += 1


def draw_system(can, line, first=False):
    x1 = get_line_pos(line)[0]
    x2 = page_width - x1
    y_start_1 = get_line_pos(line)[1]
    y_start_2 = y_start_1 + 210

    can.create_line(x1, y_start_1, x1, y_start_2 + 4 * dist_between_lines)
    can.create_line(x2, y_start_1, x2, y_start_2 + 4 * dist_between_lines)

    for n in range(5):
        can.create_line(x1, y_start_1 + n * dist_between_lines, x2, y_start_1 + n * dist_between_lines)

    for n in range(5):
        can.create_line(x1, y_start_2 + n * dist_between_lines, x2, y_start_2 + n * dist_between_lines)


def draw_bars(can, barstodraw, somme, line):
    s = 0
    for bar in barstodraw:
        barx = get_line_pos(line)[0] + s
        l = bar.get_width() * system_width / somme
        s += l
        can.create_line(get_line_pos(line)[0] + s, get_line_pos(line)[1], get_line_pos(line)[0] + s,
                        get_line_pos(line)[1] + system_height)
        for note in bar.notes:
            draw_note(can, barx, bar.start,line, note)


def draw_note(can, barx, barstart, line, note):
    x = barx + 40 + (note.start - barstart) * 100
    if note.pitch >= 60:
        y = get_line_pos(line)[1] + 5 * dist_between_lines - get_note_height(note.pitch)
    else:
        y = get_line_pos(line)[1] + system_height - 5 * dist_between_lines + get_note_height(note.pitch)
    can.create_oval(x-10, y-10, x+10, y+10, fill="black")


def get_note_height(pitch):
    print(pitch)
    l1 = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6]
    l2 = [0, 0, 6, 6, 5, 5, 4, 3, 3, 2, 2, 1]
    if pitch >= 60: return l1[pitch % 12] * dist_between_lines/2 + (3.5 * dist_between_lines) * int(abs((pitch - 60) / 12))
    else: return l2[pitch % 12] * dist_between_lines/2 + (3.5 * dist_between_lines) * int(abs((pitch - 60) / 12))


def get_line_pos(line):
    return int(line / 6) * page_width + (page_width - system_width) / 2, dist_between_systems + (dist_between_systems + system_height) * (line % 6)
