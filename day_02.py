#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import intcode_comp

if len(sys.argv) == 1:
    sys.argv += ["input_02"]
        
def machine_p1(line, mod=False):
    mem = [int(v) for v in line.split(",")]
    if mod:
        mem[1] = 12
        mem[2] = 2
    intcode_comp(mem)
    return mem[0]

def test_p1():
    assert machine_p1("1,9,10,3,2,3,11,0,99,30,40,50") == 3500
    assert machine_p1("1,1,1,4,99,5,6,0,99") == 30
test_p1()

def p1():
    for line in fileinput.input():
        print(machine_p1(line, True))
p1()

def machine_p2(line, target=19690720):
    mem_init = [int(v) for v in line.split(",")]
    for noun in range(0, 100):
        for verb in range(0, 100):
            mem = mem_init.copy()
            mem[1] = noun
            mem[2] = verb
            intcode_comp(mem)
            if mem[0] == 19690720:
                return noun * 100 + verb
    return None

def p2():
    for line in fileinput.input():
        print(machine_p2(line))
p2()
