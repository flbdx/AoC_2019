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
        self.base = 0
        self.inputs=[]
        self.outputs=[]
        self.memory={0: 99}
        self.state = IntComputer.State.STARTING
    
    def set_mem(self, memory):
        if not isinstance(memory, type({})):
            self.memory = {}
            n = 0
            for v in memory:
                self.memory[n] = v
                n += 1
        else:
            self.memory = memory
        self.state = IntComputer.State.STARTING
        self.ip = 0
        self.base = 0
    
    def push_input(self, v):
        self.inputs.append(v)
        
    def push_inputs(self, inputs):
        self.inputs.extend(inputs)
    
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
    
    def run(self, break_after_output=False, max_instructions=0):
        self.state = IntComputer.State.RUNNING
        n_instructions = 0
        while True:
            instruction = self.memory[self.ip]
            
            op = (instruction % 100)
            param_mode = lambda i: ((instruction // (10 * (10 ** i))) % 10)
            def read_operand(i):
                mode = param_mode(i)
                idx = -1
                if mode == 0:
                    idx = self.memory[self.ip + i]
                elif mode == 1:
                    idx = self.ip + i
                elif mode == 2:
                    idx = self.base + self.memory[self.ip + i]
                
                if idx in self.memory:
                    return self.memory[idx]
                else:
                    self.memory[idx] = 0
                    return 0
                
            def write_operand(i, v):
                mode = param_mode(i)
                if mode == 0:
                    self.memory[self.memory[self.ip + i]] = v
                elif mode == 2:
                    self.memory[self.base + self.memory[self.ip + i]] = v
            
            
            if op == 1: # addition
                write_operand(3, read_operand(1) + read_operand(2))
                self.ip += 4
            elif op == 2: # multself.iplication
                write_operand(3, read_operand(1) * read_operand(2))
                self.ip += 4
            elif op == 3: # input
                if len(self.inputs) > 0:
                    write_operand(1, self.inputs.pop(0))
                    self.ip += 2
                else:
                    self.state = IntComputer.State.WAITING_FOR_INPUT
                    break
            elif op == 4: # output
                self.outputs.append(read_operand(1))
                self.ip += 2
                if break_after_output:
                    self.state = IntComputer.State.WAITING_AFTER_OUTPUT
                    break
            elif op == 5: # jump-if-true
                if read_operand(1) != 0:
                    self.ip = read_operand(2)
                else:
                    self.ip += 3
            elif op == 6: # jump-if-false
                if read_operand(1) == 0:
                    self.ip = read_operand(2)
                else:
                    self.ip += 3
            elif op == 7: # less than
                if read_operand(1) < read_operand(2):
                    write_operand(3, 1)
                else:
                    write_operand(3, 0)
                self.ip += 4
            elif op == 8: # equals
                if read_operand(1) == read_operand(2):
                    write_operand(3, 1)
                else:
                    write_operand(3, 0)
                self.ip += 4
            elif op == 9: # adjusts the relative base
                self.base += read_operand(1)
                self.ip += 2
            elif op == 99: # halt
                self.state = IntComputer.State.HALTED
                break
            else:
                raise Exception("Opcode inconnu " + repr(op) + " @ip=" + repr(self.ip))

            n_instructions += 1
            if max_instructions > 0 and n_instructions == max_instructions:
                break
