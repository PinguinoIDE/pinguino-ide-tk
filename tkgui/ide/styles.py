#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import FLAT, GROOVE, RIDGE, BOTH
from ttk import Style

########################################################################
class TkStyles(object):

    #----------------------------------------------------------------------
    @classmethod
    def create_styles(self):
        """"""

        styles = Style()
        styles.configure("TNotebook", background="#afc8e1", borderwidth=0, relief=FLAT, highlightthickness=0)
        #styles.configure("Treeview", borderwidth=0, relief=FLAT, width=100)
        #styles.configure("TSeparator")
