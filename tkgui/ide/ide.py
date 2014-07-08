#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from PIL import ImageTk

from Tkinter import Text, Frame, Menu, Button, Label, CENTER
from Tkinter import RAISED, LEFT, TOP, X, BOTH, Y, BOTTOM, RIGHT, END, SUNKEN, NO, YES, DISABLED, NORMAL, FLAT, GROOVE, RIDGE
from ttk import Notebook, Style, Treeview, Scrollbar, Separator

from styles import TkStyles
from events.events import PinguinoEvents
from ..pinguino_api.pinguino import Pinguino, AllBoards
from ..pinguino_api.pinguino_config import PinguinoConfig
from .methods.config import Config


########################################################################
class PinguinoIDE(Frame, PinguinoEvents):

    def __init__(self, master=None):

        Frame.__init__(self, master)

        self.parent = master

        self.parent.geometry("640x480")
        self.parent.title(os.getenv("NAME"))

        icon = os.path.join(os.getcwd(), "tkgui", "resources", "art", "pinguino11.xbm")
        self.parent.wm_iconbitmap("@"+icon)

        TkStyles.create_styles()
        self.Files = {}

        PinguinoConfig.set_environ_vars()
        PinguinoConfig.check_user_files()

        self.pinguinoAPI = Pinguino()
        self.pinguinoAPI._boards_ = AllBoards

        self.configIDE = Config()

        PinguinoConfig.update_pinguino_paths(self.configIDE, self.pinguinoAPI)
        PinguinoConfig.update_pinguino_extra_options(self.configIDE, self.pinguinoAPI)
        PinguinoConfig.update_user_libs(self.pinguinoAPI)
        self.pinguinoAPI.set_os_variables()

        self.set_board()





        self.build_menu()

        self.buil_output()
        self.buil_toolbar()
        self.build_notebook()
        self.connect_events()

        self.pack(fill=BOTH, expand=True)

        self.parent.config(menu=self.menuBar)


        os_name = os.getenv("PINGUINO_OS_NAME")
        if os_name == "windows":
            os.environ["PATH"] = os.environ["PATH"] + ";" + self.configIDE.get_path("sdcc_bin")

        elif os_name == "linux":
            os.environ["LD_LIBRARY_PATH"]="/usr/lib32:/usr/lib:/usr/lib64"


    #----------------------------------------------------------------------
    def build_notebook(self):

        banner = os.path.join("tkgui", "resources", "art", "banner.png")
        tkimage = ImageTk.PhotoImage(file=banner)
        self.banner = Label(self, image=tkimage, justify = CENTER, height = 400, bg="#afc8e1")
        self.banner.photo = tkimage
        self.banner.pack(side=LEFT, fill=BOTH, expand=True)

        self.noteBook = Notebook(self, style="TNotebook")
        self.noteBook.pack(side=LEFT, fill=BOTH, expand=True)


    #----------------------------------------------------------------------
    def build_menu(self):

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
        configmenu.add_command(label="System paths", command=self.__show_paths__)
        self.menuBar.add_cascade(label="Configuration", menu=configmenu)

        pinguinomenu = Menu(self.menuBar, tearoff=0)
        pinguinomenu.add_command(label="Compile", command=self.pinguino_compile, accelerator="F5")
        pinguinomenu.add_command(label="Upload", command=self.pinguino_upload, accelerator="F6")
        pinguinomenu.add_separator()
        pinguinomenu.add_command(label="Stdout", command=self.__show_stdout__, accelerator="F9")
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

        self.master.bind_all("<F5>", self.pinguino_compile)
        self.master.bind_all("<F6>", self.pinguino_upload)
        self.master.bind_all("<F9>", self.__show_stdout__)


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
                if abspath.endswith(".pde"):
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

        self.output = Text(self, bg="#333333", fg="#ffffff", height=10, borderwidth=0, relief=FLAT, highlightthickness=0, font="mono 10")
        HEAD = os.getenv("NAME") + " " + os.getenv("VERSION") + "\n"
        self.output.pack(side=BOTTOM, fill=X, expand=False)
        self.output.insert(END, "\n "+HEAD)
        self.output.config(state=DISABLED)

        Frame(self, height=4, bg="#afc8e1").pack(side=BOTTOM, fill=X, expand=False)


    #----------------------------------------------------------------------
    def write_log(self, *args, **kwargs):

        lines = " "
        for line in args:
            lines += line + "\n"

        for key in kwargs.keys():
            line = key + ": " + kwargs[key]
            lines += line

        self.output.config(state=NORMAL)
        self.output.insert(END, lines.replace("\n", "\n ")[:-1])
        self.output.see(END)
        self.output.config(state=DISABLED)


