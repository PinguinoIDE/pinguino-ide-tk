#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

from Tkinter import Frame, BOTH, X, TOP, Label, RIGHT, LEFT, Checkbutton, Button, BOTTOM, IntVar
from ttk import Combobox

########################################################################
class BoardConfigAdvance(Frame):

    def __init__(self, master=None, main=None):
        Frame.__init__(self, master)

        self.parent = master
        self.main = main

        self.parent.geometry("280x174")
        self.parent.title(os.getenv("NAME") + " - Advance Board Config")
        self.master.configure(padx=10, pady=10)

        self.HEAPSIZE = {"512 byte": 512,
                         "1024 byte": 1024,}
        self.OPTIMIZATION = "-O2 -O3 -Os".split()

        self.mips16_var = IntVar()
        self.checkBox_mips16 = Checkbutton(self.parent, text="Mips16", anchor="w", variable=self.mips16_var)
        self.checkBox_mips16.pack(expand=True, fill=BOTH, side=TOP)

        frame_heap = Frame(self.parent)
        Label(frame_heap, text="Heap size:", anchor="w", width=12).pack(side=LEFT, fill=X, expand=True)
        self.comboBox_heapsize = Combobox(frame_heap, values=self.HEAPSIZE.keys())
        self.comboBox_heapsize.pack(fill=X, expand=True, side=RIGHT)
        frame_heap.pack(fill=X, expand=True, side=TOP)

        frame_opt = Frame(self.parent)
        Label(frame_opt, text="Optimization:", anchor="w", width=12).pack(side=LEFT, fill=X, expand=True)
        self.comboBox_optimization = Combobox(frame_opt, values=self.OPTIMIZATION)
        self.comboBox_optimization.pack(fill=X, expand=True, side=RIGHT)
        frame_opt.pack(fill=X, expand=True, side=TOP)

        frame_buttons = Frame(self.parent)
        Button(frame_buttons, text="Accept", command=self.accept_config).pack(fill=X, expand=True, side=LEFT)
        Button(frame_buttons, text="Restore Default", command=self.restore_default).pack(fill=X, expand=True, side=RIGHT)
        frame_buttons.pack(fill=X, expand=True, side=BOTTOM)

        self.load_config()


    #----------------------------------------------------------------------
    def quit(self):

        self.master.destroy()



    #----------------------------------------------------------------------
    def load_config(self):

        #Called in the parent frame
        #self.main.configIDE.load_config()

        if self.main.configIDE.config("Board", "mips16", True):
            self.checkBox_mips16.select()
        else:
            self.checkBox_mips16.deselect()

        heapsize = self.main.configIDE.config("Board", "heapsize", 512)
        for key in self.HEAPSIZE.keys():
            if self.HEAPSIZE[key] == heapsize:
                self.comboBox_heapsize.set(key)
                break

        optimization = self.main.configIDE.config("Board", "optimization", "-O3")
        self.comboBox_optimization.set(optimization)


    #----------------------------------------------------------------------
    def restore_default(self):

        self.checkBox_mips16.select()
        self.comboBox_heapsize.set(self.HEAPSIZE.keys()[1])
        self.comboBox_optimization.set(self.OPTIMIZATION[1])


    #----------------------------------------------------------------------
    def accept_config(self):

        self.save_config()
        self.main.configIDE.save_config()
        self.quit()


    #----------------------------------------------------------------------
    def save_config(self):

        self.main.configIDE.set("Board", "mips16", self.mips16_var.get()==1)
        heapsize = self.HEAPSIZE[self.comboBox_heapsize.get()]
        self.main.configIDE.set("Board", "heapsize", heapsize)
        self.main.configIDE.set("Board", "optimization", self.comboBox_optimization.get())
