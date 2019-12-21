#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer

if len(sys.argv) == 1:
    sys.argv += ["input_19"]


def prog_to_memory(prog):
    n = 0
    res = {}
    for v in prog.split(','):
        res[n] = int(v)
        n += 1
    return res

def scanner_p1(line, max_x=50, max_y=50):
    comp = IntComputer()
    mem = prog_to_memory(line)
    x, y = 0, 0

    def test_point(x, y):
        comp.set_mem(mem.copy())
        comp.push_input(x)
        comp.push_input(y)
        comp.run()
        return comp.read_output() == 1

    min_x = 0
    world = set()
    for y in range(max_y):
        x = min_x
        while x < max_x:
            if test_point(x, y):
                world.add((x, y))
                min_x = x
                x += 1
                break
            else:
                x += 1
        while x < max_x:
            if not test_point(x, y):
                break
            world.add((x, y))
            x += 1
    
    return len(world)

def scanner_p2(line):
    comp = IntComputer()
    mem = prog_to_memory(line)
    x, y = 0, 0

    def test_point(x, y):
        if x < 0 or y < 0:
            return False
        comp.set_mem(mem.copy())
        comp.push_input(x)
        comp.push_input(y)
        comp.run()
        return comp.read_output() == 1

    min_x = 0

    while True:
        x = min_x
        max_x = x + 5
        found = False
        while x < max_x:
            if test_point(x, y):
                found = True
                break
            x += 1
        if found:
            min_x = x
            test = test_point(x, y-99) and test_point(x+99, y - 99) and test_point(x+99, y)
            if test:
                return x * 10000 + (y-99)
        y += 1

def p1():
    for line in fileinput.input():
        print(scanner_p1(line))
p1()

def p2():
    for line in fileinput.input():
        print(scanner_p2(line))
p2()