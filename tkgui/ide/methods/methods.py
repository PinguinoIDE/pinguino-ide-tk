#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import webbrowser

from Tkinter import LEFT, BOTH, Toplevel

from tkgui.ide.child_windows.stdout import Stdout
from tkgui.ide.child_windows.paths import Paths
from tkgui.ide.child_windows.about import About
from tkgui.ide.child_windows.board_config import BoardConfig
from tkgui.ide.styles import TkStyles


########################################################################
class PinguinoMethods(object):


    #----------------------------------------------------------------------
    def __get_name__(self, ext=".pde"):

        index = 1
        name = "untitled-%d" % index + ext
        filenames = [self.noteBook.tab(tab)["text"] for tab in self.noteBook.tabs()]
        while name in filenames or name + "*" in filenames:
            index += 1
            name = "untitled-%d" % index + ext
        return name + "*"



    #----------------------------------------------------------------------
    def get_current_textedit(self):

        return self.Files[self.noteBook.select()]["textedit"]


    #----------------------------------------------------------------------
    def get_current_filename(self):

        return self.Files[self.noteBook.select()]["filename"]


    #----------------------------------------------------------------------
    def get_tab(self, value, fix_ouput=True):

        tab_value = self.noteBook.tab(self.noteBook.select())[value]

        if tab_value.endswith("*") and fix_ouput: return tab_value[:-1]
        else: return tab_value


    #----------------------------------------------------------------------
    def set_tab_text_changed(self, changed):

        if changed: self.noteBook.tab(self.noteBook.select(), text=self.get_tab("text") + "*")
        else: self.noteBook.tab(self.noteBook.select(), text=self.get_tab("text"))


    #----------------------------------------------------------------------
    def check_notebook_visibility(self):

        tabs = len(self.noteBook.tabs())

        if tabs > 0:
            self.banner.pack_forget()
            TkStyles.create_styles()
            self.noteBook.pack(side=LEFT, fill=BOTH, expand=True)
        else:
            self.noteBook.pack_forget()
            self.banner.pack(side=LEFT, fill=BOTH, expand=True)



    #----------------------------------------------------------------------
    def open_web_site(self, url):
        webbrowser.open_new_tab(url)


    #----------------------------------------------------------------------
    def set_board(self):

        board_name = self.configIDE.config("Board", "board", "Pinguino 2550")
        for board in self.pinguinoAPI._boards_:
            if board.name == board_name:
                self.pinguinoAPI.set_board(board)

        arch = self.configIDE.config("Board", "arch", 8)
        if arch == 8:
            bootloader = self.configIDE.config("Board", "bootloader", "v1_v2")
            if bootloader == "v1_v2":
                self.pinguinoAPI.set_bootloader(self.pinguinoAPI.Boot2)
            else:
                self.pinguinoAPI.set_bootloader(self.pinguinoAPI.Boot4)

        os.environ["PINGUINO_BOARD_ARCH"] = str(arch)

        compiler = self.configIDE.get_path("sdcc_bin"), "sdcc"

        if os.getenv("PINGUINO_OS_NAME") == "windows":
            ext = ".exe"
        elif os.getenv("PINGUINO_OS_NAME") == "linux":
            ext = ""

        if arch == 8:
            compiler = os.path.exists(os.path.join(self.configIDE.get_path("sdcc_bin"), "sdcc" + ext))
            libraries = os.path.exists(self.configIDE.get_path("pinguino_8_libs"))

        elif arch == 32:
            #RB20140615:
            #- gcc toolchain has been renamed from mips-elf-gcc to p32-gcc
            #- the toolchain is now based on gcc 4.8.2
            #compiler = os.path.exists(os.path.join(self.configIDE.get_path("gcc_bin"), "mips-elf-gcc-4.5.2" + ext))
            compiler = os.path.exists(os.path.join(self.configIDE.get_path("gcc_bin"), "p32-gcc" + ext))
            libraries = os.path.exists(self.configIDE.get_path("pinguino_32_libs"))

        no_compile = False
        if not compiler: no_compile = True
        elif  not libraries: no_compile = True
        if not libraries and not compiler: no_compile = True

        if no_compile: os.environ["PINGUINO_CAN_COMPILE"] = "False"
        else: os.environ["PINGUINO_CAN_COMPILE"] = "True"



    #----------------------------------------------------------------------
    def __show_stdout__(self, event=None):

        root = Toplevel()
        app = Stdout(master=root)
        app.mainloop()

    #----------------------------------------------------------------------
    def __show_paths__(self, event=None):

        root = Toplevel()
        app = Paths(master=root, main=self)
        app.mainloop()

    #----------------------------------------------------------------------
    def __show_about__(self, event=None):

        root = Toplevel()
        app = About(master=root)
        app.mainloop()

    #----------------------------------------------------------------------
    def __show_board_config__(self, event=None):

        root = Toplevel()
        app = BoardConfig(master=root, main=self)
        app.mainloop()


    #----------------------------------------------------------------------
    def get_status_board(self):

        self.set_board()
        board = self.pinguinoAPI.get_board()
        board_config = board.name

        if board.arch == 8 and board.bldr == "boot4":
            board_config += " - Boootloader: v4"
        if board.arch == 8 and board.bldr == "boot2":
            board_config += " - Boootloader: v1 & v2"

        return board_config