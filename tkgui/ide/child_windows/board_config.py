#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

from Tkinter import Frame, LabelFrame, X, TOP, Radiobutton, LEFT, RIGHT, Label, BOTTOM, Button, BOTH, IntVar, StringVar, ACTIVE, DISABLED, Toplevel
from .board_config_advance import BoardConfigAdvance


########################################################################
class BoardConfig(Frame):

    def __init__(self, master=None, main=None):
        Frame.__init__(self, master)

        self.parent = master
        self.main = main

        self.parent.geometry("336x424")
        self.parent.title(os.getenv("NAME") + " - Board Config")
        self.master.configure(padx=10, pady=10)

        self.intvar = IntVar()

        #Arch
        self.arch_var = IntVar()
        lf_arch = LabelFrame(self.parent, text="Architecture")
        lf_arch.pack(fill=X, expand=True, side=TOP)

        frame_arch = Frame(lf_arch)
        frame_arch.pack(fill=X, expand=True, side=TOP)

        frame_left1 = Frame(frame_arch)
        frame_left1.pack(expand=True, fill=BOTH, side=LEFT)

        frame_right1 = Frame(frame_arch)
        frame_right1.pack(expand=True, fill=BOTH, side=RIGHT)

        self.radioButton_arch_8 = Radiobutton(frame_left1, text="8-bit ", anchor="w", width=10, value=8, variable=self.arch_var, command=self.update_mode)
        self.radioButton_arch_8.pack(fill=X, side=TOP)

        self.radioButton_arch_32 = Radiobutton(frame_right1, text="32-bit", anchor="w", width=10, value=32, variable=self.arch_var, command=self.update_mode)
        self.radioButton_arch_32.pack(fill=X, side=TOP)


        #Mode
        self.mode_var = StringVar()
        lf_mode = LabelFrame(self.parent, text="Programming mode")
        lf_mode.pack(fill=X, expand=True, side=TOP)

        frame_mode = Frame(lf_mode)
        frame_mode.pack(fill=X, expand=True, side=TOP)

        frame_left2 = Frame(frame_mode)
        frame_left2.pack(expand=True, fill=BOTH, side=LEFT)

        frame_right2 = Frame(frame_mode)
        frame_right2.pack(expand=True, fill=BOTH, side=RIGHT)

        self.radioButton_mode_icsp = Radiobutton(frame_left2, text="ICSP", anchor="w", width=10, value="icsp", variable=self.mode_var, command=self.update_mode)
        self.radioButton_mode_icsp.pack(side=TOP, fill=X)

        self.radioButton_mode_bootloader = Radiobutton(frame_right2, text="Bootloader", anchor="w", width=10, value="bootloader", variable=self.mode_var, command=self.update_mode)
        self.radioButton_mode_bootloader.pack(side=TOP, fill=X)


        #Bootloader
        self.boot_var = StringVar()
        self.lf_boot = LabelFrame(self.parent, text="Bootloader")
        self.lf_boot.pack(fill=X, expand=True, side=TOP)

        frame_boot = Frame(self.lf_boot)
        frame_boot.pack(fill=X, expand=True, side=TOP)

        frame_left3 = Frame(frame_boot)
        frame_left3.pack(expand=True, fill=BOTH, side=LEFT)

        frame_right3 = Frame(frame_boot)
        frame_right3.pack(expand=True, fill=BOTH, side=RIGHT)

        self.radioButton_bootloader_v1_v2 = Radiobutton(frame_left3, text="v1.x or v2.x", anchor="w", width=10, value="v1_v2", variable=self.boot_var)
        self.radioButton_bootloader_v1_v2.pack(fill=X, side=TOP, expand=True)
        self.radioButton_bootloader_v4 = Radiobutton(frame_right3, text="v4.x", anchor="w", width=10, value="v4", variable=self.boot_var)
        self.radioButton_bootloader_v4.pack(fill=X, side=TOP, expand=True)


        #Devices 8bit
        self.dev8_var = StringVar()
        self.lf_dev8 = LabelFrame(self.parent, text="Devices")
        self.lf_dev8.pack(fill=X, expand=True, side=TOP)

        self.frame_8b = Frame(self.lf_dev8)
        self.frame_8b.pack(fill=X, expand=True, side=TOP)


        #Devices 32bit
        self.dev32_var = StringVar()
        self.lf_dev32 = LabelFrame(self.parent, text="Devices")
        self.lf_dev32.pack(fill=X, expand=True, side=TOP)

        self.frame_32b = Frame(self.lf_dev32)
        self.frame_32b.pack(fill=X, expand=True, side=TOP)

        frame_buttons = Frame(self.parent)
        Button(frame_buttons, text="Accept", command=self.accept_config).pack(fill=X, expand=True, side=RIGHT)
        Button(frame_buttons, text="Cancel", command=self.quit).pack(fill=X, expand=True, side=LEFT)
        frame_buttons.pack(fill=X, expand=True, side=BOTTOM)

        frame_advance = Frame(self.parent)
        self.advanceoptions = Button(frame_advance, text="Advance options", command=self.advance)
        self.advanceoptions.pack(fill=X, expand=True, side=BOTTOM)
        frame_advance.pack(fill=X, expand=True, side=BOTTOM)

        frame_warning = Frame(self.parent)
        self.label_warning = Label(frame_warning, fg="red", text="warning!", anchor="w")
        self.label_warning.pack(fill=X, expand=True, side=BOTTOM)
        frame_warning.pack(fill=X, expand=True, side=BOTTOM)

        self.build_devices_arch()
        self.load_config()
        self.init_groups()




    #----------------------------------------------------------------------
    def quit(self):

        self.master.destroy()


    #----------------------------------------------------------------------
    def build_devices_arch(self):

        #8bits
        name_checked = self.main.configIDE.config("Board", "board_8", "Pinguino 2550")
        arch_8 = filter(lambda board:board.arch==8, self.main.pinguinoAPI._boards_)
        arch_8.sort()

        frame_left = Frame(self.frame_8b)
        frame_left.pack(expand=True, fill=BOTH, side=LEFT)

        frame_right = Frame(self.frame_8b)
        frame_right.pack(expand=True, fill=BOTH, side=RIGHT)

        count = 0
        parent = frame_left  #left
        for board in arch_8:
            if arch_8.index(board) == (len(arch_8) / 2) + 1:
                count = 0
                parent = frame_right  #rigth

            radio = Radiobutton(parent, text=board.name, anchor="w", width=10, value=board.name, variable=self.dev8_var, command=lambda :self.set_board_name(board.name, "8"))
            radio.pack(expand=True, fill=X, side=TOP)

            #radio = QtGui.QRadioButton(self.board_config.groupBox_devices_8)
            #self.board_config.gridLayout_device_8.addWidget(radio, count, side, 1, 1)
            #radio.setText(board.name)
            #radio.setToolTip(board.proc)

            if name_checked == board.name: radio.select()
            #self.connect(radio, QtCore.SIGNAL("clicked()"), self.set_board_name(board.name, "8"))
            count += 1


        #32bits
        name_checked = self.main.configIDE.config("Board", "board_32", "PIC32 Pinguino OTG")
        arch_32 = filter(lambda board:board.arch==32, self.main.pinguinoAPI._boards_)
        arch_32.sort()

        frame_left0 = Frame(self.frame_32b)
        frame_left0.pack(expand=True, fill=BOTH, side=LEFT)

        frame_right0 = Frame(self.frame_32b)
        frame_right0.pack(expand=True, fill=BOTH, side=RIGHT)


        count = 0
        parent = frame_left0  #left
        for board in arch_32:
            if arch_32.index(board) == (len(arch_32) / 2) + 1:
                count = 0
                parent = frame_right0  #rigth

            radio = Radiobutton(parent, text=board.name, anchor="w", width=10, value=board.name, variable=self.dev32_var, command=lambda :self.set_board_name(board.name, "32"))
            radio.pack(expand=True, fill=X, side=TOP)

            #radio = QtGui.QRadioButton(self.board_config.groupBox_devices_32)
            #self.board_config.gridLayout_device_32.addWidget(radio, count, side, 1, 1)
            #radio.setText(board.name)
            #radio.setToolTip(board.proc)

            if name_checked == board.name: radio.select()
            #self.connect(radio, QtCore.SIGNAL("clicked()"), self.set_board_name(board.name, "32"))
            count += 1


    #----------------------------------------------------------------------
    def load_config(self):

        self.main.configIDE.load_config()

        arch = self.main.configIDE.config("Board", "arch", 8)
        getattr(self.radioButton_arch_8, "select" if (arch == 8) else "deselect")()
        getattr(self.radioButton_arch_32, "select" if (arch == 32) else "deselect")()

        if arch == 32: self.advanceoptions.pack(fill=X, expand=True, side=BOTTOM)
        else: self.advanceoptions.forget()

        mode = self.main.configIDE.config("Board", "mode", "bootloader")
        getattr(self.radioButton_mode_bootloader, "select" if (mode == "bootloader") else "deselect")()
        getattr(self.radioButton_mode_icsp, "select" if (mode == "icsp") else "deselect")()

        bootloader = self.main.configIDE.config("Board", "bootloader", "v1_v2")
        getattr(self.radioButton_bootloader_v1_v2, "select" if (bootloader == "v1_v2") else "deselect")()
        getattr(self.radioButton_bootloader_v4, "select" if (bootloader == "v4") else "deselect")()

        self.update_mode()


    #----------------------------------------------------------------------
    def update_mode(self):

        mode_boot = self.mode_var.get() == "bootloader"
        arch_8 = self.arch_var.get() == 8

        if mode_boot and arch_8: self.lf_boot.pack(fill=X, expand=True, side=TOP)
        else: self.lf_boot.forget()
        self.init_groups()

        if not mode_boot:
            self.label_warning.configure(text="WARNING!! this mode can overwite the bootloader code.")
        else:
            self.label_warning.configure(text="")



    #----------------------------------------------------------------------
    def set_board_name(self, name, arch):

        def dummy():
            self.main.configIDE.set("Board", "board_"+arch, name)
        return dummy


    #----------------------------------------------------------------------
    def init_groups(self):

        self.lf_dev32.forget()
        self.lf_dev8.forget()

        if self.arch_var.get() == 8:
            self.lf_dev8.pack(fill=X, expand=True, side=TOP)
            self.advanceoptions.forget()

        else:
            self.lf_dev32.pack(fill=X, expand=True, side=TOP)
            self.advanceoptions.pack(fill=X, expand=True, side=BOTTOM)



    #----------------------------------------------------------------------
    def save_config(self):

        #if self.board_config.radioButton_arch_8.isChecked(): arch = 8
        #else: arch = 32
        self.main.configIDE.set("Board", "arch", self.arch_var.get())

        #if self.board_config.radioButton_mode_bootloader.isChecked(): mode = "bootloader"
        #else: mode = "icsp"
        self.main.configIDE.set("Board", "mode", self.mode_var.get())

        #if self.board_config.radioButton_bootloader_v1_v2.isChecked(): bootloader = "v1_v2"
        #else: bootloader = "v4"
        self.main.configIDE.set("Board", "bootloader", self.boot_var.get())

        name = self.main.configIDE.config("Board", "board_"+str(self.arch_var.get()), None)
        self.main.configIDE.set("Board", "board", name)



    #----------------------------------------------------------------------
    def accept_config(self):

        self.save_config()
        self.main.configIDE.save_config()
        self.main.statusbar_ide(self.main.get_status_board())
        self.close_advance()
        self.quit()


    #----------------------------------------------------------------------
    def advance(self):

        root = Toplevel()
        self.frame_advance = BoardConfigAdvance(master=root, main=self.main)
        self.frame_advance.mainloop()


    #----------------------------------------------------------------------
    def close_advance(self):

        try: assert self.frame_advance
        except: return
        self.frame_advance.quit()
