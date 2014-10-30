#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from ConfigParser import RawConfigParser

from PIL import ImageTk
from Tkinter import Frame, TOP, RIGHT, X, INSERT, Button, LabelFrame, LEFT, Label, FLAT, Entry, END
from tkFileDialog import askdirectory

from tkgui.ide.methods.dialogs import Dialogs
from tkgui.pinguino_api.pinguino_config import PinguinoConfig
from tkgui.pinguino_api.pinguino_config import PinguinoConfig


########################################################################
class Paths(Frame):

    def __init__(self, master=None, main=None):
        Frame.__init__(self, master)

        self.parent = master
        self.main = main

        self.parent.geometry("640x150")
        self.parent.title(os.getenv("NAME")+" - Paths")

        self.master.configure(padx=10, pady=10)
        width = 14

        #icon
        icon = os.path.join("tkgui", "resources", "icons", "clear.png")
        image_clear = ImageTk.PhotoImage(file=icon)

        # lb8 = LabelFrame(self.parent, text="8-bit")
        # frame8 = Frame(self.parent)
        # self.parent.pack(fill=X, expand=True, side=TOP)

        frame8c = Frame(self.parent)
        frame_text1 = Frame(frame8c)
        frame_text1.pack(side=LEFT)
        # Label(frame_text1, text="SDCC compiler:", width=width, anchor="w").pack(side=LEFT)
        # self.label_sdcc_bin = Entry(frame8c)
        # self.label_sdcc_bin.pack(side=LEFT, fill=X, expand=True)
        frame8c.pack(fill=X, expand=True, side=TOP)

        # button = Button(frame8c, image=image_clear, relief=FLAT, command=lambda :self.reset_value("sdcc_bin"), borderwidth=0, highlightthickness=0)
        # button.image = image_clear
        # button.pack(side=LEFT, padx=2, pady=4)

        # Button(frame8c, text="Change...", command=self.set_dir_dialog(self.label_sdcc_bin)).pack(side=LEFT)

        frame8l = Frame(self.parent)
        frame_text2 = Frame(frame8l)
        frame_text2.pack(side=LEFT)
        Label(frame_text2, text="8-bit libraries:", width=width, anchor="w").pack(side=LEFT)
        self.label_pinguino_8_libs = Entry(frame8l)
        self.label_pinguino_8_libs.pack(side=LEFT, fill=X, expand=True)

        button = Button(frame8l, image=image_clear, relief=FLAT, command=lambda :self.reset_value("pinguino_8_libs"), borderwidth=0, highlightthickness=0)
        button.image = image_clear
        button.pack(side=LEFT, padx=2, pady=4)

        Button(frame8l, text="Change...", command=self.set_dir_dialog(self.label_pinguino_8_libs)).pack(side=LEFT)

        frame8l.pack(fill=X, expand=True, side=TOP)


        # lb32 = LabelFrame(self.parent, text="32-bit")

        # frame32 = Frame(lb32)


        frame32c = Frame(self.parent)
        frame_text3 = Frame(frame32c)
        frame_text3.pack(side=LEFT)
        # Label(frame_text3, text="GCC compiler:", width=width, anchor="w").pack(side=LEFT)
        # self.label_gcc_bin = Entry(frame32c)
        # self.label_gcc_bin.pack(side=LEFT, fill=X, expand=True)
        # button = Button(frame32c, image=image_clear, relief=FLAT, command=lambda :self.reset_value("gcc_bin"), borderwidth=0, highlightthickness=0)
        # button.image = image_clear
        # button.pack(side=LEFT, padx=2, pady=4)
        # Button(frame32c, text="Change...", command=self.set_dir_dialog(self.label_gcc_bin)).pack(side=LEFT)
        frame32c.pack(fill=X, expand=True, side=TOP)


        frame32l = Frame(self.parent)
        frame_text4 = Frame(frame32l)
        frame_text4.pack(side=LEFT)
        Label(frame_text4, text="32-bit libraries:", width=width, anchor="w").pack(side=LEFT)
        self.label_pinguino_32_libs = Entry(frame32l)
        self.label_pinguino_32_libs.pack(side=LEFT, fill=X, expand=True)
        button = Button(frame32l, image=image_clear, relief=FLAT, command=lambda :self.reset_value("pinguino_32_libs"), borderwidth=0, highlightthickness=0)
        button.image = image_clear
        button.pack(side=LEFT, padx=2, pady=4)
        Button(frame32l, text="Change...", command=self.set_dir_dialog(self.label_pinguino_32_libs)).pack(side=LEFT)
        frame32l.pack(fill=X, expand=True, side=TOP)


        # self.parent.pack(fill=X, expand=True, side=TOP)


        # lb8.pack(fill=X, expand=True, side=TOP, padx=10, pady=10)
        # lb32.pack(fill=X, expand=True, side=TOP, padx=10, pady=10)



        Label(self.master, text="Pinguino IDE requieres a restart to reinitialize its prefertences.", anchor="w").pack(side=LEFT)
        Button(self.master, text="Close", command=self.quit).pack(side=RIGHT)


        self.dialog_dirs = ((self.label_pinguino_8_libs, "PINGUINO_8_LIBS"),
                            (self.label_pinguino_32_libs, "PINGUINO_32_LIBS"),
                           )

        default_paths = {"PINGUINO_8_LIBS": self.main.configIDE.get_path("pinguino_8_libs"),
                         "PINGUINO_32_LIBS": self.main.configIDE.get_path("pinguino_32_libs"),
                         }

        for lineEdit, keyWord in self.dialog_dirs:
            lineEdit.delete(0, END)
            lineEdit.insert(INSERT, self.main.configIDE.config("Paths", keyWord, default_paths[keyWord]))


    #----------------------------------------------------------------------
    def reset_value(self, option):
        default = RawConfigParser()
        default.readfp(open(os.path.join(os.getenv("PINGUINO_HOME"), "tkgui", "config", "pinguino."+os.getenv("PINGUINO_OS_NAME")+".conf"), "r"))
        getattr(self, "label_"+option).delete(0, END)
        getattr(self, "label_"+option).insert(INSERT, default.get("Paths", option))



    #----------------------------------------------------------------------
    def quit(self):
        """"""

        if Dialogs.confirm_message("Do you really want save these paths?."):
            self.save_paths()


        self.master.destroy()


    #----------------------------------------------------------------------
    def save_paths(self):

        for lineEdit, keyWord in self.dialog_dirs:
            content = lineEdit.get()
            print content
            if content.isspace(): content = ""
            if not (os.path.exists(content) and content):
                Dialogs.error_message(keyWord + ": '" + content + "'\n"+"This path not exist.")
                return
            else: self.main.configIDE.set("Paths", keyWord, content)
        self.main.configIDE.save_config()
        PinguinoConfig.update_pinguino_paths(self.main.configIDE, self.main.pinguinoAPI)


    #----------------------------------------------------------------------
    def set_dir_dialog(self, lineEdit):

        def dummy_func():
            path = lineEdit.get()
            if not os.path.isfile(path):
                path = ""

            filename = askdirectory(parent=self,
                                    initialdir=path,
                                    title=os.getenv("NAME")+" - Select file",
                                    )

            if filename:
                lineEdit.delete(0, END)
                lineEdit.insert(INSERT, filename)

        return dummy_func
