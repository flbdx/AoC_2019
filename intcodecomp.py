#!/usr/bin/python3
#encoding: UTF-8

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


import enum

class IntComputer(object):
    class State(enum.Enum):
        STARTING = 0
        RUNNING = 1
        WAITING_FOR_INPUT = 2
        WAITING_AFTER_OUTPUT = 3
        HALTED = 4
    
    def __init__(self):
        self.ip = 0
        self.inputs=[]
        self.outputs=[]
        self.memory=[99]
        self.state = IntComputer.State.STARTING
    
    def set_mem(self, memory):
        self.memory = memory
        self.state = IntComputer.State.STARTING
        self.ip = 0
    
    def push_input(self, v):
        self.inputs.append(v)
    
    def read_output(self):
        if len(self.outputs) != 0:
            return self.outputs.pop(0)
        return None
    
    def clear_outputs(self):
        self.outputs = []
    
    def clear_inputs(self):
        self.inputs = []
    
    def get_state(self):
        return self.state
    
    def get_memory(self, idx=None):
        if idx != None:
            return self.memory[idx]
        else:
            return self.memory
    
    def run(self, break_after_output=False):
        self.state = IntComputer.State.RUNNING
        while True:
            instruction = self.memory[self.ip]
            
            op = (instruction % 100)
            param_mode = lambda i: ((instruction // (10 * (10 ** i))) % 10)
            def operand(i):
                mode = param_mode(i)
                if mode == 0:
                    return self.memory[self.memory[self.ip + i]]
                elif mode == 1:
                    return self.memory[self.ip + i]
            
            if op == 1: # addition
                self.memory[self.memory[self.ip + 3]] = operand(1) + operand(2)
                self.ip += 4
            elif op == 2: # multself.iplication
                self.memory[self.memory[self.ip + 3]] = operand(1) * operand(2)
                self.ip += 4
            elif op == 3: # input
                if len(self.inputs) > 0:
                    self.memory[self.memory[self.ip + 1]] = self.inputs.pop(0)
                    self.ip += 2
                else:
                    self.state = IntComputer.State.WAITING_FOR_INPUT
                    break
            elif op == 4: # output
                self.outputs.append(operand(1))
                self.ip += 2
                if break_after_output:
                    self.state = IntComputer.State.WAITING_AFTER_OUTPUT
                    break
            elif op == 5: # jump-if-true
                if operand(1) != 0:
                    self.ip = operand(2)
                else:
                    self.ip += 3
            elif op == 6: # jump-if-false
                if operand(1) == 0:
                    self.ip = operand(2)
                else:
                    self.ip += 3
            elif op == 7: # less than
                if operand(1) < operand(2):
                    self.memory[self.memory[self.ip + 3]] = 1
                else:
                    self.memory[self.memory[self.ip + 3]] = 0
                self.ip += 4
            elif op == 8: # equals
                if operand(1) == operand(2):
                    self.memory[self.memory[self.ip + 3]] = 1
                else:
                    self.memory[self.memory[self.ip + 3]] = 0
                self.ip += 4
            elif op == 99: # halt
                self.state = IntComputer.State.HALTED
                break
            else:
                raise Exception("Opcode inconnu " + repr(op) + " @ip=" + repr(self.ip))
