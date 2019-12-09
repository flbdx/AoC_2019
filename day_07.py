#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import intcode_comp, IntComputer
import itertools

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

def work_p1(program):
    n_amps = 5
    phase_settings = list(range(0, n_amps))
    
    max_v = 0
    max_settings = None
    
    for settings in itertools.permutations(phase_settings, len(phase_settings)):
        prev_input = 0
        for amp in range(0, n_amps):
            comp = IntComputer()
            comp.set_mem(program.copy())
            comp.push_input(settings[amp])
            comp.push_input(prev_input)
            comp.run()
            assert comp.get_state() == IntComputer.State.HALTED
            prev_input = comp.read_output()
        if prev_input > max_v:
            max_v = prev_input
            max_settings = settings
    return (max_settings, max_v)

def test_p1():
    max_s, max_v = work_p1([int(v) for v in "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(",")])
    assert max_s == (4,3,2,1,0) and max_v == 43210
    
    max_s, max_v = work_p1([int(v) for v in "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0".split(",")])
    assert max_s == (0,1,2,3,4) and max_v == 54321
    
    max_s, max_v = work_p1([int(v) for v in "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0".split(",")])
    assert max_s == (1,0,4,3,2) and max_v == 65210
test_p1()

def p1():
    for line in fileinput.input():
        print(work_p1([int(v) for v in line.split(",")]))
p1()


def work_p2(program):
    n_amps = 5
    phase_settings = list(range(5, 5+n_amps))
    
    max_v = 0
    max_settings = None
    
    for settings in itertools.permutations(phase_settings, len(phase_settings)):
        chain_input = 0
        thuster_output = 0
        computers = [None] * n_amps
        for i in range(n_amps):
            computers[i] = IntComputer()
            computers[i].set_mem(program.copy())
            computers[i].push_input(settings[i])
        
        halted = False
        while not halted:
            for amp in range(n_amps):
                computers[amp].push_input(chain_input)
                computers[amp].run(True)
                if computers[amp].get_state() == IntComputer.State.WAITING_AFTER_OUTPUT:
                    chain_input = computers[amp].read_output()
                else:
                    assert computers[amp].get_state() == IntComputer.State.HALTED
                    halted = True
                    break
            thuster_output = chain_input
        
        if thuster_output > max_v:
            max_v = thuster_output
            max_settings = settings
    return (max_settings, max_v)

def test_p2():
    max_s, max_v = work_p2([int(v) for v in "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(",")])
    assert max_s == (9,8,7,6,5) and max_v == 139629729
    
    max_s, max_v = work_p2([int(v) for v in "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".split(",")])
    assert max_s == (9,7,8,5,6) and max_v == 18216
test_p2()

def p2():
    for line in fileinput.input():
        print(work_p2([int(v) for v in line.split(",")]))
p2()
