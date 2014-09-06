#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import Text, END, DISABLED, NORMAL, IntVar

from tkgui.ide.methods.syntax import directives, const

########################################################################
class PinguinoTextEdit(Text):

    #----------------------------------------------------------------------
    def __init__(self, root=None, **args):

        Text.__init__(self, root, **args)
        self.main = self.master.master
        self.create_syntas_tags()
        self.bind("<Key>", self.update_syntax)

        self.config(maxundo=15, undo=True, bg="white")
        self.update_linenumber()


    #----------------------------------------------------------------------
    def create_syntas_tags(self):

        self.tag_configure("directive", foreground="#d36820", font="mono 11")
        self.tag_configure("reserved", foreground="#0000ff", font="mono 11")
        self.tag_configure("number", foreground="#ff0000", font="mono 11")
        self.tag_configure("dquot", foreground="#7f0000", font="mono 11")
        self.tag_configure("squot", foreground="#cc0000", font="mono 11")
        self.tag_configure("dcomment", foreground="#c81818", font="mono 11")
        self.tag_configure("scomment", foreground="#007F00", font="mono 11")
        #self.tag_configure("operators", foreground="#000000", font="mono 11")


    #----------------------------------------------------------------------
    def set_linenumber(self, linenumber):

        self.linenumber = linenumber


    #----------------------------------------------------------------------
    def set_scrolls(self, xsb, ysb):

        self.xsb = xsb
        self.ysb = ysb


    #----------------------------------------------------------------------
    def update_linenumber(self, event=None):

        self.after(10, self.update_delay)


    #----------------------------------------------------------------------
    def update_delay(self):

        lines = self.get("0.0", END).count("\n")
        numbers = "\n".join(map(lambda s:" "+str(s).rjust(4, " ")+" ", range(1, lines+1)))
        self.linenumber.numbers.config(state=NORMAL)
        self.linenumber.numbers.delete("0.0", END)
        self.linenumber.numbers.insert(END, numbers)
        self.linenumber.numbers.config(state=DISABLED)
        self.linenumber.numbers.yview_moveto(self.yview()[0])


    #----------------------------------------------------------------------
    def text_changed(self):

        if not self.main.noteBook.tab(self.main.noteBook.select())["text"].endswith("*"):
            self.main.set_tab_text_changed(True)
        self.update_linenumber()


    #----------------------------------------------------------------------
    def update_syntax(self, key=None):

        if not key is None: self.text_changed()
        for name in self.tag_names(): self.tag_delete(name)
        self.create_syntas_tags()

        #directives
        self.highlight_pattern("(#"+"|#".join(directives)+")", "directive")
        self.highlight_pattern("#[ ]*[define|include|ifndef|endif|pragma][ ]*.*", "directive")

        #decimal
        self.highlight_pattern("\y[\d]+\y", "number")

        #floats
        self.highlight_pattern("\y[\d]+\.[\d]+\y", "number")

        #bin
        self.highlight_pattern("\y0[Bb][01]+\y", "number")

        #hexa
        self.highlight_pattern("\y0[Xx][A-Fa-f\d]+\y", "number")

        #reserved
        self.highlight_pattern("("+"|".join(const)+")", "reserved")

        ##operators
        #self.highlight_pattern("[()\[\]{}<>=\-\+\*\\%#!~&^,]", "operators")

        #library.function
        self.highlight_pattern("[^0-9][a-zA-Z0-9_]*\.[^0-9][a-zA-Z0-9_][^\\(]*", "reserved")

        #double quotation
        self.highlight_pattern(r'"[^"\\]*(\\.[^"\\]*)*"', "dquot")

        #single quotation
        self.highlight_pattern(r"'[^'\\]*(\\.[^'\\]*)*'", "squot")

        #single line comment
        self.highlight_pattern(r'//[^\n]*', "scomment")

        #multi line comment
        start = self.index("1.0")
        end = self.index("end")
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        self.mark_set("searchLimit", "end")
        while True:
            index = self.search("/*", "matchEnd", "searchLimit", count=count, regexp=False)
            if index == "": break
            self.mark_set("matchStart", index)
            index = self.search("*/", "matchEnd", "searchLimit", count=count, regexp=False)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add("dcomment", "matchStart", "matchEnd")


    #----------------------------------------------------------------------
    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=True):

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")
