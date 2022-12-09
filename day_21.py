#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

def prog_to_memory(prog):
    n = 0
    res = {}
    for v in prog.split(','):
        res[n] = int(v)
        n += 1
    return res

def p1():
    for line in fileinput.input():
        comp = IntComputer()
        mem = prog_to_memory(line)
        
        comp.set_mem(mem.copy())
        comp.run()
        
        # sauter si on a un trou 3 devant (C == false) et  du sol en 4 (D == true)
        # toujours sauter si on a un trou juste devant (A == false)
        
        text = """NOT C J
AND D J
NOT A T
OR T J
WALK\n"""
        for c in text:
            comp.push_input(ord(c))
        comp.run()
        
        s = ""
        while True:
            v = comp.read_output()
            if v == None:
                break
            try:
                s += chr(v)
            except:
                s += repr(v)
        print(s)
    
p1()

def p2():
    for line in fileinput.input():
        comp = IntComputer()
        mem = prog_to_memory(line)
        
        comp.set_mem(mem.copy())
        comp.run()
        
        #    @   
        #  #####.#.##..#####
        #       CD   H
        # ne pas sauter trop tôt pour éviter de tomber dans H
        # NOT C J
        # AND D J
        # AND H J
        
        #          @
        #  #####.#.##.##.###
        #           ABCD
        # sauter immédiatement
        # NOT B T
        # AND D J
        
        # et en dernier recours, toujours sauter si on a un trou devant
        # NOT A J
        
        # le tout lié par des OR
        
        text = """NOT C J
AND D J
AND H J
NOT B T
AND D T
OR T J
NOT A T
OR T J
RUN\n"""
        for c in text:
            comp.push_input(ord(c))
        comp.run()
        
        s = ""
        while True:
            v = comp.read_output()
            if v == None:
                break
            try:
                s += chr(v)
            except:
                s += repr(v)
        print(s)
    
p2()
