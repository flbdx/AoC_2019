#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer

if len(sys.argv) == 1:
    sys.argv += ["input_13"]

class Arcade(object):
    def prog_to_memory(self, prog):
        n = 0
        res = {}
        for v in prog.split(','):
            res[n] = int(v)
            n += 1
        return res
    
    def __init__(self, program, credits=None):
        self.comp = IntComputer()
        mem = self.prog_to_memory(program)
        if credits != None:
            mem[0] = credits
        self.comp.set_mem(mem)
        self.world = {}
        self.score = 0
    
    def run_p1(self):
        while self.comp.get_state() != IntComputer.State.HALTED:
            self.comp.run(break_after_output=True)
            self.comp.run(break_after_output=True)
            self.comp.run(break_after_output=True)
            x = self.comp.read_output()
            y = self.comp.read_output()
            t = self.comp.read_output()
            self.world[(x, y)] = t
    
    def run(self):
        while True:
            self.comp.run()
            while True:
                x = self.comp.read_output()
                if x == None:
                    break
                y = self.comp.read_output()
                t = self.comp.read_output()
                if x >= 0 and y >= 0:
                    self.world[(x, y)] = t
                else:
                    self.score = t
            if self.comp.get_state() == IntComputer.State.HALTED or self.comp.get_state() == IntComputer.State.WAITING_FOR_INPUT:
                break;
    
    def print_screen(self, width=38, height=20):
        for y in range(0, height):
            s = ""
            for x in range(0, width):
                t = self.world[(x, y)]
                if t == 0: # blank
                    s += ' '
                elif t == 1: # wall
                    s += '#'
                elif t == 2: # block
                    s += '~'
                elif t == 3: # paddle
                    s += '-'
                elif t == 4: # ball
                    s += 'o'
            print(s)
        print("\n*** {0} ***\n".format(self.score))
    
    def play(self):
        i = 0
        while self.comp.get_state() != IntComputer.State.HALTED:
            self.run()
            ball_p = None
            padd_p = None
            for t in self.world:
                if self.world[t] == 4:
                    ball_p = t
                elif self.world[t] == 3:
                    padd_p = t
            if ball_p[0] < padd_p[0]:
                self.comp.push_input(-1)
            elif ball_p[0] > padd_p[0]:
                self.comp.push_input(1)
            else:
                self.comp.push_input(0)
            #self.print_screen()
        self.print_screen()

                    

def p1():
    for line in fileinput.input():
        arcade = Arcade(line)
        arcade.run_p1()
        
        n_blocks = 0
        for tile in arcade.world:
            if arcade.world[tile] == 2:
                n_blocks += 1
        print(n_blocks)
p1()

def p2():
    for line in fileinput.input():
        arcade = Arcade(line, 2)
        arcade.play()
p2()
