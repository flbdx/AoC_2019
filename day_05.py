#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

def intcode_comp(memory, inputs=[], outputs=[]):
    inputs_idx = 0
    ip = 0
    while True:
        instruction = memory[ip]
        
        op = (instruction % 100)
        param_mode = lambda i: ((instruction // (10 * (10 ** i))) % 10)
        def operand(i):
            mode = param_mode(i)
            if mode == 0:
                return memory[memory[ip + i]]
            elif mode == 1:
                return memory[ip + i]
        
        if op == 1: # addition
            memory[memory[ip + 3]] = operand(1) + operand(2)
            ip += 4
        elif op == 2: # multiplication
            memory[memory[ip + 3]] = operand(1) * operand(2)
            ip += 4
        elif op == 3: # input
            memory[memory[ip + 1]] = inputs[inputs_idx]
            inputs_idx += 1
            ip += 2
        elif op == 4: # output
            outputs.append(operand(1))
            ip += 2
        elif op == 5: # jump-if-true
            if operand(1) != 0:
                ip = operand(2)
            else:
                ip += 3
        elif op == 6: # jump-if-false
            if operand(1) == 0:
                ip = operand(2)
            else:
                ip += 3
        elif op == 7: # less than
            if operand(1) < operand(2):
                memory[memory[ip + 3]] = 1
            else:
                memory[memory[ip + 3]] = 0
            ip += 4
        elif op == 8: # equals
            if operand(1) == operand(2):
                memory[memory[ip + 3]] = 1
            else:
                memory[memory[ip + 3]] = 0
            ip += 4
        elif op == 99: # halt
            break
        else:
            raise Exception("Opcode inconnu " + repr(op) + " @ip=" + repr(ip))

def machine_p1(line, inputs=[]):
    outputs=[]
    mem = [int(v) for v in line.split(",")]
    intcode_comp(mem, inputs, outputs)
    return (mem, outputs)

def test_p1():
    assert machine_p1("3,0,4,0,99", [5])[1] == [5]
    assert machine_p1("1002,4,3,4,33")[0] == [1002, 4, 3, 4, 99]
    assert machine_p1("1101,100,-1,4,0")[0] == [1101, 100, -1, 4, 99]
test_p1()

def p1():
    for line in fileinput.input():
        mem, outputs = machine_p1(line, [1])
        print(outputs[-1])
p1()


def test_p2():
    assert machine_p1("3,9,8,9,10,9,4,9,99,-1,8", [8])[1] == [1]
    assert machine_p1("3,9,8,9,10,9,4,9,99,-1,8", [2])[1] == [0]
    
    assert machine_p1("3,9,7,9,10,9,4,9,99,-1,8", [7])[1] == [1]
    assert machine_p1("3,9,7,9,10,9,4,9,99,-1,8", [8])[1] == [0]
    
    assert machine_p1("3,3,1108,-1,8,3,4,3,99", [8])[1] == [1]
    assert machine_p1("3,3,1108,-1,8,3,4,3,99", [9])[1] == [0]
    
    assert machine_p1("3,3,1107,-1,8,3,4,3,99", [7])[1] == [1]
    assert machine_p1("3,3,1107,-1,8,3,4,3,99", [9])[1] == [0]
    
    assert machine_p1("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [10])[1] == [1]
    assert machine_p1("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [0])[1] == [0]
    
    assert machine_p1("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [10])[1] == [1]
    assert machine_p1("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [0])[1] == [0]
    
    large_test = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    assert machine_p1(large_test, [7])[1] == [999]
    assert machine_p1(large_test, [8])[1] == [1000]
    assert machine_p1(large_test, [9])[1] == [1001]
    
test_p2()

def p2():
    for line in fileinput.input():
        mem, outputs = machine_p1(line, [5])
        print(outputs[-1])
p2()
