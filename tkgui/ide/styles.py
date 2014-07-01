#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import FLAT, GROOVE, RIDGE, BOTH
from ttk import Style

########################################################################
class TkStyles(object):
    """"""

    #----------------------------------------------------------------------
    @classmethod
    def create_styles(self):
        """"""

        styles = Style()
        styles.configure("TNotebook", background="#afc8e1", borderwidth=0, relief=FLAT, highlightthickness=0)
        #styles.configure("Treeview", borderwidth=0, relief=FLAT, width=100)
        styles.configure("TSeparator")

        #noteStyler.configure("TNotebook.Tab", background=COLOR_1, foreground=COLOR_3, lightcolor=COLOR_6, borderwidth=0)
        #noteStyler.configure("TFrame", background=COLOR_1, foreground=COLOR_2, borderwidth=0)

