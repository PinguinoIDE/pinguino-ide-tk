#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import Text, Frame, Menu, Button, Label, CENTER


from Tkinter import RAISED, LEFT, TOP, X, BOTH, Y, BOTTOM, RIGHT, END, SUNKEN, NO, YES, DISABLED, NORMAL, FLAT, GROOVE, RIDGE
from ttk import Notebook, Style, Treeview, Scrollbar, Separator

from events.events import PinguinoEvents
from styles import TkStyles

from PIL import Image, ImageTk

import os

from pinguino_api.pinguino_config import PinguinoConfig

class PinguinoIDE(Frame, PinguinoEvents):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        #super(PinguinoIDE, self).__init__(self, master) #tkinter is old-style classes, this not work


        self.parent = master

        self.parent.geometry("640x480")

        TkStyles.create_styles()

        self.Files = {}

        self.parent.title(os.getenv("NAME"))

        PinguinoConfig.set_environ_vars()


        self.build_menu()


        self.buil_output()
        self.buil_toolbar()
        self.build_notebook()
        #self.examples_view()


        self.connect_events()


        self.pack(fill=BOTH, expand=True)


        self.parent.config(menu=self.menuBar)





    #----------------------------------------------------------------------
    def build_notebook(self):

        banner = os.path.join("tkgui", "resources", "art", "banner.png")
        tkimage = ImageTk.PhotoImage(Image.open(banner))
        self.banner = Label(self, image=tkimage, justify = CENTER, height = 400, bg="#afc8e1")
        self.banner.photo = tkimage
        self.banner.pack(side=LEFT, fill=BOTH, expand=True)

        self.noteBook = Notebook(self, style="TNotebook")
        self.noteBook.pack(side=LEFT, fill=BOTH, expand=True)


    #----------------------------------------------------------------------
    def build_menu(self):
        """"""
        self.menuBar = Menu(self, borderwidth=1, relief=FLAT)

        filemenu = Menu(self.menuBar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        filemenu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        filemenu.add_separator()
        filemenu.add_command(label="Save file", command=self.save_file, accelerator="Ctrl+S")
        filemenu.add_command(label="Save as", command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Close", command=self.close_file, accelerator="Ctrl+W")
        filemenu.add_command(label="Close all", command=self.close_all)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.close_ide, accelerator="Ctrl+Q")
        self.menuBar.add_cascade(label="File", menu=filemenu)


        editmenu = Menu(self.menuBar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.edit_undo, accelerator="Ctrl+Z")
        editmenu.add_command(label="Redo", command=self.edit_redo, accelerator="Ctrl+Y")
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.edit_cut, accelerator="Ctrl+X")
        editmenu.add_command(label="Copy", command=self.edit_copy, accelerator="Ctrl+C")
        editmenu.add_command(label="Paste", command=self.edit_paste, accelerator="Ctrl+V")
        self.menuBar.add_cascade(label="Edit", menu=editmenu)

        configmenu = Menu(self.menuBar, tearoff=0)
        configmenu.add_command(label="Board Settings", command=self.new_file)
        configmenu.add_command(label="System paths", command=self.new_file)
        self.menuBar.add_cascade(label="Configuration", menu=configmenu)

        pinguinomenu = Menu(self.menuBar, tearoff=0)
        pinguinomenu.add_command(label="Compile", command=self.new_file, accelerator="F5")
        pinguinomenu.add_command(label="Upload", command=self.new_file, accelerator="F6")
        self.menuBar.add_cascade(label="Pinguino", menu=pinguinomenu)

        self.menuBar.add_cascade(label="Examples", menu=self.examples_view())

        helpmenu = Menu(self.menuBar, tearoff=0)
        links = Menu(helpmenu, tearoff=0)
        github = Menu(links, tearoff=0)
        github.add_command(label="IDE", command=lambda :self.open_web_site("https://github.com/PinguinoIDE/pinguino-ide/releases/latest"))
        github.add_command(label="Libraries", command=lambda :self.open_web_site("https://github.com/PinguinoIDE/pinguino-libraries/releases/latest"))
        github.add_command(label="Compilers", command=lambda :self.open_web_site("https://github.com/PinguinoIDE/pinguino-compilers/releases/latest"))
        links.add_cascade(label="GitHub", menu=github)
        links.add_command(label="Website", command=lambda :self.open_web_site("http://www.pinguino.cc/"))
        links.add_command(label="Wiki", command=lambda :self.open_web_site("http://wiki.pinguino.cc/"))
        links.add_command(label="Forum", command=lambda :self.open_web_site("http://forum.pinguino.cc/"))
        links.add_command(label="Blog", command=lambda :self.open_web_site("http://blog.pinguino.cc/"))
        links.add_command(label="Group", command=lambda :self.open_web_site("https://groups.google.com/forum/#!forum/pinguinocard"))
        links.add_command(label="Shop", command=lambda :self.open_web_site("http://shop.pinguino.cc/"))
        helpmenu.add_cascade(label="Links", menu=links)
        helpmenu.add_command(label="About...", command=self.new_file)
        self.menuBar.add_cascade(label="Help", menu=helpmenu)

        self.master.bind_all("<Control-n>", self.new_file)
        self.master.bind_all("<Control-o>", self.open_file)
        self.master.bind_all("<Control-s>", self.save_file)
        self.master.bind_all("<Control-w>", self.close_file)
        self.master.bind_all("<Control-q>", self.close_ide)

        self.master.bind_all("<Control-Z>", self.edit_undo)
        self.master.bind_all("<Control-Y>", self.edit_redo)

        self.master.bind_all("<Control-X>", self.edit_cut)
        self.master.bind_all("<Control-C>", self.edit_copy)
        self.master.bind_all("<Control-V>", self.edit_paste)

        #self.master.bind_all("<Control-V>", self.edit_paste)
        #self.master.bind_all("<Control-V>", self.edit_paste)


    #----------------------------------------------------------------------
    def examples_view(self):

        examplesmenu = Menu(self.menuBar, tearoff=0)
        return self.process_directory(examplesmenu, os.path.join(os.getenv("PINGUINO_USER_PATH"), "examples"))


    #----------------------------------------------------------------------
    def process_directory(self, parent, path):

        menu = Menu(parent, tearoff=0)
        for p in os.listdir(path):
            abspath = os.path.join(path, p)

            if os.path.isfile(abspath):
                label = os.path.split(abspath)[1]
                menu.add_command(label=label, command=lambda :self.open_file(abspath))

            if os.path.isdir(abspath):
                label = os.path.split(abspath)[1]
                menu.add_cascade(label=label, menu=self.process_directory(menu, abspath))

        return menu


    #----------------------------------------------------------------------
    def buil_toolbar(self):

        Separator(self, style="TSeparator").pack(side=TOP, fill=X, expand=False)

        self.toolBar = Frame(self, borderwidth=0, relief=FLAT, highlightthickness=0)
        self.toolBar.pack(side=TOP, fill=X, expand=False)

        Frame(self, height=4, bg="#afc8e1").pack(side=TOP, fill=X, expand=False)


    #----------------------------------------------------------------------
    def buil_output(self):


        self.output = Text(self, bg="#333333", fg="#ffffff", height=10, borderwidth=0, relief=FLAT, highlightthickness=0)
        HEAD = os.getenv("NAME") + " " + os.getenv("VERSION") + "\n"
        self.output.pack(side=BOTTOM, fill=X, expand=False)
        self.output.insert(END, "\n "+HEAD)
        self.output.config(state=DISABLED)

        Frame(self, height=4, bg="#afc8e1").pack(side=BOTTOM, fill=X, expand=False)

    #----------------------------------------------------------------------
    def write_log(self, *args, **kwargs):

        lines = ""
        for line in args:
            lines += " " + line
            #self.main.plainTextEdit_output.appendPlainText(line)

        for key in kwargs.keys():
            line = key + ": " + kwargs[key]
            lines += line

        self.output.config(state=NORNAL)
        self.output.insert(END, lines)
        self.output.config(state=DISABLED)



    #----------------------------------------------------------------------
    def build(self):
        """"""