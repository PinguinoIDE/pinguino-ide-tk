#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import Text, INSERT, END, Label, DISABLED, NORMAL

from ..methods.syntax import directives, const

import re

class PinguinoTextEdit(Text):


    tags = {'directive': '#d36820',
            'reserved': '#0000ff',
            "number": "#ff0000",
            "dquot": "#7f0000",
            "squot": "#cc0000",
            "scomment": "#007F00",
            }

    def __init__(self, root=None, **args):
        Text.__init__(self, root, **args)
        self.config_tags()

        self.main = self.master.master

        self.bind('<Key>', self.key_press)

        self.config(maxundo=15, undo=True)
        self.update_linenumber()



    #----------------------------------------------------------------------
    def set_linenumber(self, linenumber):
        """"""
        self.linenumber = linenumber


    #----------------------------------------------------------------------
    def set_scrolls(self, xsb, ysb):
        """"""
        self.xsb = xsb
        self.ysb = ysb



    #----------------------------------------------------------------------
    def update_linenumber(self, event=None):
        """"""
        self.after(10, self.update_delay)

    def update_delay(self):
        lines = self.get("0.0", END).count("\n")
        numbers = "\n".join(map(lambda s:" "+str(s).rjust(4, " ")+" ", range(1, lines+1)))

        #self.linenumber.numbers.configure(text=numbers)
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


    def config_tags(self):
        for tag, val in self.tags.items():
            self.tag_config(tag, foreground=val)

    def remove_tags(self, start, end):
        for tag in self.tags.keys():
            self.tag_remove(tag, start, end)

    def key_press(self, key):

        self.text_changed()

        cline = self.index(INSERT).split('.')[0]
        lastcol = 0
        char = self.get('%s.%d'%(cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d'%(cline, lastcol))

        buffer = self.get('%s.%d'%(cline,0),'%s.%d'%(cline,lastcol))
        tokenized = buffer.split(' ')

        self.remove_tags('%s.%d'%(cline, 0), '%s.%d'%(cline, lastcol))

        start, end = 0, 0
        for token in tokenized:
            end = start + len(token)

            #directives
            if token in map(lambda x:"#"+x, directives):
                self.tag_add('directive', '%s.%d'%(cline, start), '%s.%d'%(cline, end))
            elif re.match("#[ ]*[define|include|ifndef|endif|pragma][ ]*.*", token):
                self.tag_add('directive', '%s.%d'%(cline, start), '%s.%d'%(cline, end))

            #reserved
            elif token in const:
                self.tag_add('reserved', '%s.%d'%(cline, start), '%s.%d'%(cline, end))

            #library.function
            elif re.match("\\b[\D][\w]*\.[\D][\w]*", token):
                self.tag_add('reserved', '%s.%d'%(cline, start), '%s.%d'%(cline, end))

            #decimal
            elif re.match("\\b[\d]+\\b", token):
                self.tag_add('number', '%s.%d'%(cline, start), '%s.%d'%(cline, end))

            #floats
            elif re.match("\\b[\d]+\.[\d]+\\b", token):
                self.tag_add('number', '%s.%d'%(cline, start), '%s.%d'%(cline, end))

            #hexa
            elif re.match("\\b0[Xx][A-Fa-f\d]+\\b", token):
                self.tag_add('number', '%s.%d'%(cline, start), '%s.%d'%(cline, end))

            #bin
            elif re.match("\\b0[Bb][01]+\\b", token):
                self.tag_add('number', '%s.%d'%(cline, start), '%s.%d'%(cline, end))

            ##quotation
            #elif re.match(r'"[^"\\]*(\\.[^"\\]*)*"', token):
                #self.tag_add('dquot', '%s.%d'%(cline, start), '%s.%d'%(cline, end))
            #elif re.match(r"'[^'\\]*(\\.[^'\\]*)*'", token):
                #self.tag_add('squot', '%s.%d'%(cline, start), '%s.%d'%(cline, end))

            ##single line comment
            #elif re.match(r'//[^\n]*', token):
                #self.tag_add('scomment', '%s.%d'%(cline, start), '%s.%d'%(cline, end))





            #else:
                #for index in range(len(token)):
                    #try:
                        #int(token[index])
                    #except ValueError:
                        #pass
                    #else:
                        #self.tag_add('int', '%s.%d'%(cline, start+index))



            start += len(token)+1