#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer
import collections

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

def prog_to_memory(prog):
    n = 0
    res = {}
    for v in prog.split(','):
        res[n] = int(v)
        n += 1
    return res

class Network(object):
    def __init__(self, mem, size=50):
        self.size = size
        self.computers = [IntComputer() for i in range(size)]
        self.queues = [collections.deque() for i in range(size)]
        self.out_buffers = [collections.deque() for i in range(size)]
        self.idling = [0 for i in range(size)]
        self.nat_data = None
        self.nat_previous_y = None
        
        for i in range(size):
            self.computers[i].set_mem(mem.copy())
            self.computers[i].push_input(i)
    
    def run_p1(self):
        while True:
            all_stopped = True
            for i in range(self.size):
                state = self.computers[i].get_state()
                if state == IntComputer.State.HALTED:
                    continue
                else:
                    all_stopped = False
                    if state == IntComputer.State.WAITING_FOR_INPUT:
                        if len(self.queues[i]) >= 2:
                            while len(self.queues[i]) >= 2:
                                self.computers[i].push_input(self.queues[i].popleft())
                                self.computers[i].push_input(self.queues[i].popleft())
                        else:
                            self.computers[i].push_input(-1)
                    
                self.computers[i].run(max_instructions=50)
                
                while True:
                    v = self.computers[i].read_output()
                    if v == None:
                        break
                    self.out_buffers[i].append(v)
                
                while len(self.out_buffers[i]) >= 3:
                    addr = self.out_buffers[i].popleft()
                    x = self.out_buffers[i].popleft()
                    y = self.out_buffers[i].popleft()
                    if addr < self.size:
                        self.queues[addr].append(x)
                        self.queues[addr].append(y)
                    elif addr == 255:
                        return y
            
            
    def run_p2(self):
        while True:
            all_stopped = True
            for i in range(self.size):
                state = self.computers[i].get_state()
                if state == IntComputer.State.HALTED:
                    continue
                else:
                    all_stopped = False
                    if state == IntComputer.State.WAITING_FOR_INPUT:
                        self.idling[i] += 1
                        if len(self.queues[i]) >= 2:
                            while len(self.queues[i]) >= 2:
                                self.computers[i].push_input(self.queues[i].popleft())
                                self.computers[i].push_input(self.queues[i].popleft())
                        else:
                            self.computers[i].push_input(-1)
                    
                self.computers[i].run(max_instructions=50)
                
                while True:
                    v = self.computers[i].read_output()
                    if v == None:
                        break
                    self.out_buffers[i].append(v)
                    self.idling[i] = 0
                
                while len(self.out_buffers[i]) >= 3:
                    addr = self.out_buffers[i].popleft()
                    x = self.out_buffers[i].popleft()
                    y = self.out_buffers[i].popleft()
                    if addr < self.size:
                        self.queues[addr].append(x)
                        self.queues[addr].append(y)
                    elif addr == 255:
                        self.nat_data = (x, y)
            
            # NAT
            all_idle = True
            for i in range(self.size):
                if self.idling[i] < 10:
                    all_idle = False
                    break
            if all_idle and self.nat_data != None:
                self.queues[0].append(self.nat_data[0])
                self.queues[0].append(self.nat_data[1])
                if self.nat_data[1] == self.nat_previous_y:
                    return self.nat_previous_y
                self.nat_previous_y = self.nat_data[1]
                self.nat_data = None
            
            
            if all_stopped:
                break

def p1():
    for line in fileinput.input():
        mem = prog_to_memory(line)
        network = Network(mem)
        print(network.run_p1())
p1()

def p2():
    for line in fileinput.input():
        mem = prog_to_memory(line)
        network = Network(mem)
        print(network.run_p2())
p2()
