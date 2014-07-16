#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

from PIL import ImageTk
from Tkinter import Frame, Label, BOTH, TOP, X, BOTTOM, Button, RIGHT, LEFT, SUNKEN
from ttk import Notebook, Style

########################################################################
class About(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.parent = master

        self.parent.geometry("640x480")
        self.parent.title(os.getenv("NAME") + " - About")
        self.master.configure(padx=10, pady=10)

        self.name_version = os.getenv("NAME")+" "+os.getenv("VERSION")+"-"+os.getenv("SUBVERSION")


        icon = os.path.join("tkgui", "resources", "art", "pinguino11.png")
        self.image_pinguino = ImageTk.PhotoImage(file=icon)

        self.style_text = {"font": "inherit 20",}


        self.build_home()


    #----------------------------------------------------------------------
    def build_home(self):

        if getattr(self, "credits", False): self.credits.pack_forget()
        if getattr(self, "license", False): self.license.pack_forget()

        self.home = Frame(self.parent)
        self.home.pack(expand=True, fill=BOTH)

        Label(self.home, text=self.name_version, **self.style_text).pack(side=TOP, expand=True, fill=X)

        image = Label(self.home, image=self.image_pinguino)
        image.photo = self.image_pinguino
        image.pack(side=TOP, expand=True, fill=BOTH)

        description = "Pinguino is an Open Software and Open Hardware\nArduino-like project.\
Boards are based on 8 or 32-bit USB built-in\nMicrochip microcontrollers. The main goal\
is to build a real\nUSB system without USB to serial converter."

        Label(self.home, text=description).pack(side=TOP, expand=True, fill=X)


        self.panel_buttons = Frame(self.home)
        self.panel_buttons.pack(side=BOTTOM, fill=BOTH, expand=True)


        Button(self.panel_buttons, text="Close", command=self.quit).pack(side=RIGHT, fill=X, expand=True)
        Button(self.panel_buttons, text="Credits", command=self.build_credits).pack(side=LEFT, fill=X, expand=True)


    #----------------------------------------------------------------------
    def build_credits(self):

        if getattr(self, "home", False): self.home.pack_forget()
        if getattr(self, "license", False): self.license.pack_forget()

        self.credits = Frame(self.parent)
        self.credits.pack(expand=True, fill=BOTH)

        Label(self.credits, text="Credits", **self.style_text).pack(side=TOP, expand=True, fill=X)

        style = Style()
        style.configure("BW.TNotebook", background=self.parent.cget("bg"), borderwidth=1, relief=SUNKEN, highlightthickness=1)


        notebook = Notebook(self.credits, style="BW.TNotebook")

        write = ("Jean-Pierre Mandon",
                 "Régis Blanchot",
                 "Marcus Fazzi",
                 "Jesus Carmona Esteban",
                 "Alfred Broda",
                 "Yeison Cardona",
                 "Henk Van Beek",
                 "Björn Pfeiffer",
                 "Alexis Sánchez",
                 )

        label_write = Label(self.credits, text="\n\n".join(write))
        label_write.pack(side=TOP, expand=True, fill=BOTH)
        notebook.add(label_write, text="Write by")

        doc = ("Benoit Espinola",
               "Sebastien Koechlin",
               "Ivan Ricondo",
               "Jesus Carmona Esteban",
               "Marcus Fazzi",
               "Régis Blanchot",
               )

        label_doc = Label(self.credits, text="\n\n".join(doc))
        label_doc.pack(side=TOP, expand=True, fill=BOTH)
        notebook.add(label_doc, text="Documented by")

        trans = ("Joan Espinoza",
                 "Alexis Sánchez",
                 "Régis Blanchot",
                 "Moreno Manzini",
                 "Yeison Cardona",
                 "\"Avrin\"",
                )

        label_trans = Label(self.credits, text="\n\n".join(trans))
        label_trans.pack(side=TOP, expand=True, fill=BOTH)
        notebook.add(label_trans, text="Translated by")

        art = ("France Cadet",
               "Laurent Cos--tes",
               "Daniel Rodri­guez",
               )

        label_art = Label(self.credits, text="\n\n".join(art))
        label_art.pack(side=TOP, expand=True, fill=BOTH)
        notebook.add(label_art, text="Art by")

        notebook.pack(side=TOP, fill=BOTH, expand=True)

        self.panel_buttons = Frame(self.credits)
        self.panel_buttons.pack(side=BOTTOM, fill=BOTH, expand=True)

        Button(self.panel_buttons, text="Close", command=self.quit).pack(side=RIGHT, fill=X, expand=True)
        Button(self.panel_buttons, text="License", command=self.build_license).pack(side=LEFT, fill=X, expand=True)



    #----------------------------------------------------------------------
    def build_license(self):

        if getattr(self, "home", False): self.home.pack_forget()
        if getattr(self, "credits", False): self.credits.pack_forget()

        self.license = Frame(self.parent)
        self.license.pack(expand=True, fill=BOTH)

        Label(self.license, text="License", **self.style_text).pack(side=TOP, expand=True, fill=BOTH)

        lic = """Pinguino is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later version.

Pinguino is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details. You should have received a copy of
the GNU General Public License along with File Hunter; if not, write to
the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA""" + "\n" * 10

        Label(self.license, text=lic).pack(side=TOP, expand=True, fill=X)

        self.panel_buttons = Frame(self.license)
        self.panel_buttons.pack(side=BOTTOM, fill=BOTH, expand=True)

        Button(self.panel_buttons, text="Close", command=self.quit).pack(side=RIGHT, fill=X, expand=True)
        Button(self.panel_buttons, text="About", command=self.build_home).pack(side=LEFT, fill=X, expand=True)




    #----------------------------------------------------------------------
    def quit(self):
        """"""
        self.master.destroy()