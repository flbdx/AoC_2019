#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import defaultdict

if len(sys.argv) == 1:
    sys.argv += ["input_24"]

class SimuP1(object):
    def __init__(self, lines):
        self.world = 0
        
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    self.world = SimuP1.set_p(self.world, x, y)
    
    def set_p(w, x, y):
        return w | (1 << (y*5 + x))
    def test_p(w, x, y):
        if x >= 0 and x < 5 and y >= 0 and y < 5:
            return (w >> (y*5 + x)) & 1 != 0
        return 0
    
    def adj(self, x, y):
        return SimuP1.test_p(self.world, x - 1, y) + \
               SimuP1.test_p(self.world, x + 1, y) + \
               SimuP1.test_p(self.world, x, y + 1) + \
               SimuP1.test_p(self.world, x, y - 1)
    
    def step(self):
        nworld = 0
        for y in range(5):
            for x in range(5):
                n_adj = self.adj(x, y)
                if SimuP1.test_p(self.world, x, y):
                    if n_adj == 1:
                        nworld = SimuP1.set_p(nworld, x, y)
                else:
                    if n_adj == 1 or n_adj == 2:
                        nworld = SimuP1.set_p(nworld, x, y)
        self.world = nworld
    
    def run(self):
        values = {self.world}
        while True:
            self.step()
            if self.world in values:
                return self.world
            values.add(self.world)
    
    def print(self):
        s = ""
        for y in range(5):
            for x in range(5):
                s += '#' if self.test_p(x, y) else '.'
            s += "\n"
        print(s)

def test_p1():
    lines = """....#
#..#.
#..##
..#..
#....""".split("\n")
    simu = SimuP1(lines)
    assert simu.run() == 2129920
test_p1()

def p1():
    simu = SimuP1(fileinput.input())
    print(simu.run())
p1()


class SimuP2(object):
    def __init__(self, lines):
        self.worlds = defaultdict(lambda: 0)
        
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    self.__set_p(x, y, 0)
                    
    def set_p(w, x, y):
        return w | (1 << (y*5 + x))
    def test_p(w, x, y):
        if x >= 0 and x < 5 and y >= 0 and y < 5:
            return (w >> (y*5 + x)) & 1 != 0
        return 0
    def __set_p(self, x, y, l):
        self.worlds[l] = SimuP2.set_p(self.worlds[l], x, y)
    def __test_p(self, x, y, l):
        if x >= 0 and x < 5 and y >= 0 and y < 5:
            return SimuP2.test_p(self.worlds[l], x, y)
        return 0
    
    def adj(self, x, y, l):
        n_adj = 0
        # en dessous (y + 1)
        if y == 1 and x == 2:
            n_adj += sum((self.__test_p(X, 0, l + 1) for X in range(5)), 0)
        elif y != 4:
            n_adj += self.__test_p(x, y + 1, l)
        else:
            n_adj += self.__test_p(2, 3, l - 1)
        
        # au dessus (y - 1)
        if y == 3 and x == 2:
            n_adj += sum((self.__test_p(X, 4, l + 1) for X in range(5)), 0)
        elif y != 0:
            n_adj += self.__test_p(x, y - 1, l)
        else:
            n_adj += self.__test_p(2, 1, l - 1)
        
        # à droite (x + 1)
        if x == 1 and y == 2:
            n_adj += sum((self.__test_p(0, Y, l + 1) for Y in range(5)), 0)
        elif x != 4:
            n_adj += self.__test_p(x + 1, y, l)
        else:
            n_adj += self.__test_p(3, 2, l - 1)
        
        # à gauche (x - 1)
        if x == 3 and y == 2:
            n_adj += sum((self.__test_p(4, Y, l + 1) for Y in range(5)), 0)
        elif x != 0:
            n_adj += self.__test_p(x - 1, y, l)
        else:
            n_adj += self.__test_p(1, 2, l - 1)
        
        return n_adj
    
    def step(self):
        levels = self.worlds.keys()
        min_level = min(l for l in levels if self.worlds[l] != 0) - 1
        max_level = max(l for l in levels if self.worlds[l] != 0) + 1
        
        nworlds = defaultdict(lambda: 0)
        for l in range(min_level, max_level + 1):
            nworlds[l] = 0
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        continue
                    n_adj = self.adj(x, y, l)
                    if self.__test_p(x, y, l):
                        if n_adj == 1:
                            nworlds[l] = SimuP2.set_p(nworlds[l], x, y)
                    else:
                        if n_adj == 1 or n_adj == 2:
                            nworlds[l] = SimuP2.set_p(nworlds[l], x, y)
        self.worlds = nworlds
    
    def run(self, n_steps):
        for n in range(n_steps):
            self.step()

    def count(self):
        c = 0
        for l, world in self.worlds.items():
            c += sum( [ world & (1<<i) != 0 for i in range(25) ] )
        return c
    
    def print(self):
        levels = self.worlds.keys()
        min_level = min(l for l in levels if self.worlds[l] != 0)
        max_level = max(l for l in levels if self.worlds[l] != 0)
        
        for l in range(min_level, max_level + 1):
            s = "LEVEL {0}\n".format(l)
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        s += "?"
                    else:
                        s += '#' if self.__test_p(x, y, l) else '.'
                s += "\n"
            print(s)

def test_p2():
    lines = """....#
#..#.
#.?##
..#..
#....""".split("\n")
    simu = SimuP2(lines)
    simu.run(10)
    assert simu.count() == 99
test_p2()

def p2():
    simu = SimuP2(fileinput.input())
    simu.run(200)
    print(simu.count())
p2()
