#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer
import enum
import itertools

if len(sys.argv) == 1:
    sys.argv += ["input_17"]


def prog_to_memory(prog):
    n = 0
    res = {}
    for v in prog.split(','):
        res[n] = int(v)
        n += 1
    return res

def work_p1(line):
    comp = IntComputer()
    mem = prog_to_memory(line)
    comp.set_mem(mem)
    world = {}
    
    comp.run()
    x = 0
    y = 0
    while True:
        c = comp.read_output()
        if c == None:
            break
        if chr(c) == '\n':
            y += 1
            x = 0
        else:
            world[(x, y)] = c
            x += 1
        
    width = max(p[0] for p in world.keys()) + 1
    height = max(p[1] for p in world.keys()) + 1
    
    checksum = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if world[(x, y)] == ord('#') == world[(x+1, y)] == world[(x-1, y)] == world[(x, y+1)] == world[(x, y-1)]:
                checksum += x * y
    return checksum

class Direction(enum.Enum):
    UP = ord('^')
    DOWN = ord('v')
    LEFT = ord('<')
    RIGHT = ord('>')
    
    def turn_left(self):
        if self == Direction.UP:
            return Direction.LEFT
        if self == Direction.RIGHT:
            return Direction.UP
        if self == Direction.DOWN:
            return Direction.RIGHT
        if self == Direction.LEFT:
            return Direction.DOWN
    def turn_right(self):
        if self == Direction.UP:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.UP
    
    def next(self, p):
        if self == Direction.UP:
            return [p[0], p[1] - 1]
        if self == Direction.RIGHT:
            return [p[0] + 1, p[1]]
        if self == Direction.DOWN:
            return [p[0], p[1] + 1]
        if self == Direction.LEFT:
            return [p[0] - 1, p[1]]

def work_p2(line):
    comp = IntComputer()
    mem = prog_to_memory(line)
    mem[0] = 2
    comp.set_mem(mem)
    world = {}
    
    comp.run()
    x = 0
    y = 0
    bob_p = None
    direction = None
    while True:
        c = comp.read_output()
        if c == None:
            break
        if chr(c) == '\n':
            y += 1
            x = 0
        else:
            if chr(c) in '^v<>':
                bob_p = [x, y]
                direction = Direction(c)
            world[(x, y)] = c
            x += 1
    
    instructions = []
    print((bob_p, direction))
    
    p = [bob_p[0],  bob_p[1]]
    
    steps = 0
    while True:
        next_p = direction.next(p)
        next_v = world.get(tuple(next_p), ord('.'))
        if next_v == ord('#'): # follow in the same direction
            steps += 1
            p = next_p
        else:
            # try left
            left_turn = True
            next_p = direction.turn_left().next(p)
            next_v = world.get(tuple(next_p), ord('.'))
            if next_v != ord('#'): # try right
                left_turn = False
                next_p = direction.turn_right().next(p)
                next_v = world.get(tuple(next_p), ord('.'))
                if next_v != ord('#'): # end of the line
                    if steps != 0:
                        instructions.append(steps)
                    break
            if steps != 0:
                instructions.append(steps)
            steps = 1
            p = next_p
            if left_turn:
                direction = direction.turn_left()
                instructions.append('L')
            else:
                direction = direction.turn_right()
                instructions.append('R')
    print(",".join(str(c) for c in instructions))
    
    subsequences = {}
    # search only for 3 dir+len or 4 dir+len couples
    # max size for a 4-size sequence is 4 * 5 = 20
    min_len = 3
    max_len = 4
    for l in range(min_len * 2, max_len * 2 + 1, 2):
        for i in range(0, len(instructions) - l + 1, 2):
            t = tuple(instructions[i:i+l])
            subsequences[t] = subsequences.get(t, 0) + 1
    
    # try all triplet of sequences
    valid_triplet = None
    valid_calls = []
    for triplet in itertools.combinations(subsequences.keys(), 3):
        i = 0
        valid_sequence = []
        ok = True
        while ok and i < len(instructions):
            found = False
            for s in triplet:
                if i + len(s) <= len(instructions) and tuple(instructions[i:i+len(s)]) == s:
                    i += len(s)
                    valid_sequence.append(s)
                    found = True
                    break
            if not found:
                ok = False
        if ok:
            valid_triplet = {triplet[0]: 'A', triplet[1]: 'B', triplet[2]: 'C'}
            valid_calls = [valid_triplet[s] for s in valid_sequence]
            valid_triplet = {'A': triplet[0], 'B': triplet[1], 'C': triplet[2]}
            if len(",".join(valid_calls)) < 20:
                break
    
    input_prog = ",".join(valid_calls) # main routine
    input_prog += "\n"
    input_prog += ",".join(str(c) for c in valid_triplet['A']) # A
    input_prog += "\n"
    input_prog += ",".join(str(c) for c in valid_triplet['B']) # B
    input_prog += "\n"
    input_prog += ",".join(str(c) for c in valid_triplet['C']) # C
    input_prog += "\n"
    input_prog += "n\n"
    print(input_prog)
    
    for c in input_prog:
        comp.push_input(ord(c))
    comp.run()
    
    s = ""
    while True:
        c = comp.read_output()
        if c == None:
            break
        try:
            s += chr(c)
        except ValueError:
            s += str(c)
    print(s)
    

def p1():
    for line in fileinput.input():
        print(work_p1(line.strip()))
p1()

def p2():
    for line in fileinput.input():
        work_p2(line.strip())
p2()
