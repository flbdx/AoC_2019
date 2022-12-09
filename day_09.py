#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer

if len(sys.argv) == 1:
    sys.argv += ["input_09"]

def prog_to_memory(prog):
    n = 0
    res = {}
    for v in prog.split(','):
        res[n] = int(v)
        n += 1
    return res

def test_p1():
    comp = IntComputer()
    
    memory = prog_to_memory("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
    comp.set_mem(memory)
    comp.run()
    assert comp.outputs == [int(v) for v in "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(',')]
    
    memory = prog_to_memory("1102,34915192,34915192,7,4,7,99,0")
    comp = IntComputer()
    comp.set_mem(memory)
    comp.run()
    assert comp.read_output() == 34915192*34915192
    
    memory = prog_to_memory("104,1125899906842624,99")
    comp = IntComputer()
    comp.set_mem(memory)
    comp.run()
    assert comp.read_output() == 1125899906842624
    
test_p1()

def p1():
    for line in fileinput.input():
        memory = prog_to_memory(line)
        comp = IntComputer()
        comp.set_mem(memory)
        comp.push_input(1)
        comp.run()
        print(comp.outputs)
p1()

def p2():
    for line in fileinput.input():
        memory = prog_to_memory(line)
        comp = IntComputer()
        comp.set_mem(memory)
        comp.push_input(2)
        comp.run()
        print(comp.outputs)
p2()
