#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer
import enum

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

def prog_to_memory(prog):
    n = 0
    res = {}
    for v in prog.split(','):
        res[n] = int(v)
        n += 1
    return res

class Direction(enum.Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    
    def turn_left(self):
        if self == Direction.UP:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.UP
    def turn_right(self):
        if self == Direction.UP:
            return Direction.RIGHT
        if self == Direction.LEFT:
            return Direction.UP
        if self == Direction.DOWN:
            return Direction.LEFT
        if self == Direction.RIGHT:
            return Direction.DOWN

def work_p1(program, start_color=0):
    memory = prog_to_memory(program)
    comp = IntComputer()
    comp.set_mem(memory)
    
    world = {}
    
    pos = [0, 0] # [x, y], y croissant : up, x croissant : right
    world[tuple(pos)] = start_color
    direction = Direction.UP
    
    while True:
        color = world.get(tuple(pos))
        if color == None:
            color = 0
        comp.push_input(color)
        comp.run()
        if comp.get_state() == IntComputer.State.HALTED:
            break
        
        world[tuple(pos)] = comp.read_output()
        turn = comp.read_output()
        
        if turn == 0:
            direction = direction.turn_left()
        else:
            direction = direction.turn_right()
        
        if direction == Direction.UP:
            pos[1] += 1
        elif direction == Direction.LEFT:
            pos[0] -= 1
        elif direction == Direction.DOWN:
            pos[1] -= 1
        else:
            pos[0] += 1
    
    return world

def p1():
    for line in fileinput.input():
        world = work_p1(line)
        print(len(world))

p1()

def p2():
    for line in fileinput.input():
        world = work_p1(line, 1)
        
        min_x = min([p[0] for p in world.keys()])
        max_x = max([p[0] for p in world.keys()])
        min_y = min([p[1] for p in world.keys()])
        max_y = max([p[1] for p in world.keys()])
        
        
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                c = world.get((x, y))
                if c == 1:
                    sys.stdout.write('#')
                else:
                    sys.stdout.write(' ')
            sys.stdout.write("\n")
        
p2()
