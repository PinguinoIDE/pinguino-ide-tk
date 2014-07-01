#! /usr/bin/python
#-*- coding: utf-8 -*-

directives = ["define", "include", "ifndef", "endif", "undef", "if", "elif", "else", "error", "warning"]

#from const.h
const = [ "PI", "HALF_PI", "TWO_PI", "DEG_TO_RAD", "RAD_TO_DEG", "NULL", "ON", "OFF", "FALSE", "TRUE", "True", "False", "false", "true",
          "INPUT", "OUTPUT", "HIGH",
          "LOW", "AND", "OR",
          "BYTE", "BIN", "OCT", "DEC", "HEX", "FLOAT",
          "LED1", "LED2", "LED3", "LED4", "WHITELED", "GREENLED", "USERLED", "YELLOWLED", "REDLED", "PROGBUTTON", "USERBUTTON",
          "RTCC", "PMCS1", "PMRD", "PMWR", "PMA1",


          #Others, not in cons.h
          "FOSC", "MIPS",
          "PORTA", "PORTB", "PORTC", "PORTD", "PORTE", "PORTF", "PORTG",

          "void", "const", "BOOL", "char", "unsigned", "short", "int", "long", "float", "double", "byte", "word",
          "u8", "s8", "u16", "s16", "u32", "s32", "u64", "s64",

          "struct", "union", "typedef", "enum", "register", "static", "extern", "volatile",
          "loop", "setup", "INT_MILLISEC", "INT_MICROSEC", "INT_FALLING_EDGE", "interrupt",


          #C syntax
          "if", "switch", "for", "while", "do", "continue", "break", "else", "return", "case", "default",
]


const += ["P1_%d"%p for p in range(1, 17)]
const += ["P2_%d"%p for p in range(1, 17)]
const += ["D%d"%p for p in range(14)]
const += ["A%d"%p for p in range(8)]
const += ["PWM%d"%p for p in range(5)]
const += ["PWD%d"%p for p in range(8)]


