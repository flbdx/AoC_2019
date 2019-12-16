#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer
import enum

if len(sys.argv) == 1:
    sys.argv += ["input_15"]
    
class LabBot(object):
    class Direction(enum.Enum):
        NORTH = 1
        SOUTH = 2
        WEST = 3
        EAST = 4
        
        def turn_left(self):
            if self == LabBot.Direction.NORTH:
                return LabBot.Direction.WEST
            if self == LabBot.Direction.WEST:
                return LabBot.Direction.SOUTH
            if self == LabBot.Direction.SOUTH:
                return LabBot.Direction.EAST
            if self == LabBot.Direction.EAST:
                return LabBot.Direction.NORTH
        def turn_right(self):
            if self == LabBot.Direction.NORTH:
                return LabBot.Direction.EAST
            if self == LabBot.Direction.WEST:
                return LabBot.Direction.NORTH
            if self == LabBot.Direction.SOUTH:
                return LabBot.Direction.WEST
            if self == LabBot.Direction.EAST:
                return LabBot.Direction.SOUTH
    
    def prog_to_memory(self, prog):
        n = 0
        res = {}
        for v in prog.split(','):
            res[n] = int(v)
            n += 1
        return res
    
    def __init__(self, program):
        self.comp = IntComputer()
        mem = self.prog_to_memory(program)
        self.comp.set_mem(mem)
        self.world = {(0, 0): 1}
        self.distances = {(0, 0): 0}
        self.pos = [0, 0]
        self.target = None
        self.direction = LabBot.Direction.NORTH
        self.distance = 0
        
    def walk_p1(self):
        
        steps = 0
        while steps < 3500:
            self.comp.push_input(self.direction.value)
            self.comp.run(break_after_output=True)
            res = self.comp.read_output()
            #print((self.pos, self.direction, res))
            if res == 0: # WALL
                t = None
                if self.direction == LabBot.Direction.NORTH:
                    t = (self.pos[0], self.pos[1] + 1)
                elif self.direction == LabBot.Direction.SOUTH:
                    t = (self.pos[0], self.pos[1] - 1)
                elif self.direction == LabBot.Direction.EAST:
                    t = (self.pos[0] + 1, self.pos[1])
                else:
                    t = (self.pos[0] - 1, self.pos[1])
                self.world[t] = 0
                self.direction = self.direction.turn_left()
            elif res == 1 or res == 2: # MOVED 1 STEP
                if self.direction == LabBot.Direction.NORTH:
                    self.pos[1] += 1
                elif self.direction == LabBot.Direction.SOUTH:
                    self.pos[1] -= 1
                elif self.direction == LabBot.Direction.EAST:
                    self.pos[0] += 1
                else:
                    self.pos[0] -= 1
                self.direction = self.direction.turn_right()
                self.world[tuple(self.pos)] = res
                d = self.distance + 1
                rec_d = self.distances.get(tuple(self.pos), None)
                if rec_d == None:
                    self.distances[tuple(self.pos)] = d
                    self.distance = d
                elif d < rec_d:
                    self.distances[tuple(self.pos)] = d
                    self.distance = d
                elif rec_d < d:
                    self.distance = rec_d
                    
                if res == 2:
                    self.target = self.pos.copy()
            steps += 1
        
        min_x = min([p[0] for p in self.world.keys()])
        max_x = max([p[0] for p in self.world.keys()])
        min_y = min([p[1] for p in self.world.keys()])
        max_y = max([p[1] for p in self.world.keys()])
        
        #max_d = max(self.distances.values()) + 1
        
        s = ""
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                if x == 0 and y == 0:
                    s += 'o'
                else:
                    v = self.world.get((x, y), -1)
                    if v == 0:
                        s += '#'
                    elif v == 1:
                        s += ' '
                        #s += repr((self.distances[(x, y)] * 10) // max_d)
                    elif v == 2:
                        s += 'X'
                    else:
                        s += '?'
            s += "\n"
        print(s)
        
    def walk_p2(self):
        
        steps = 0
        while steps < 3500:
            self.comp.push_input(self.direction.value)
            self.comp.run(break_after_output=True)
            res = self.comp.read_output()
            if res == 0: # WALL
                t = None
                if self.direction == LabBot.Direction.NORTH:
                    t = (self.pos[0], self.pos[1] + 1)
                elif self.direction == LabBot.Direction.SOUTH:
                    t = (self.pos[0], self.pos[1] - 1)
                elif self.direction == LabBot.Direction.EAST:
                    t = (self.pos[0] + 1, self.pos[1])
                else:
                    t = (self.pos[0] - 1, self.pos[1])
                self.world[t] = 0
                self.direction = self.direction.turn_left()
            elif res == 1 or res == 2: # MOVED 1 STEP
                if self.direction == LabBot.Direction.NORTH:
                    self.pos[1] += 1
                elif self.direction == LabBot.Direction.SOUTH:
                    self.pos[1] -= 1
                elif self.direction == LabBot.Direction.EAST:
                    self.pos[0] += 1
                else:
                    self.pos[0] -= 1
                self.direction = self.direction.turn_right()
                self.world[tuple(self.pos)] = res                    
                if res == 2:
                    self.target = self.pos.copy()
                    break
            steps += 1
        
        
        self.distances = {tuple(self.target): 0}
        
        steps = 0
        while steps < 3500:
            self.comp.push_input(self.direction.value)
            self.comp.run(break_after_output=True)
            res = self.comp.read_output()
            if res == 0: # WALL
                self.direction = self.direction.turn_left()
            elif res == 1 or res == 2: # MOVED 1 STEP
                if self.direction == LabBot.Direction.NORTH:
                    self.pos[1] += 1
                elif self.direction == LabBot.Direction.SOUTH:
                    self.pos[1] -= 1
                elif self.direction == LabBot.Direction.EAST:
                    self.pos[0] += 1
                else:
                    self.pos[0] -= 1
                self.direction = self.direction.turn_right()
                d = self.distance + 1
                rec_d = self.distances.get(tuple(self.pos), None)
                if rec_d == None:
                    self.distances[tuple(self.pos)] = d
                    self.distance = d
                elif d < rec_d:
                    self.distances[tuple(self.pos)] = d
                    self.distance = d
                elif rec_d < d:
                    self.distance = rec_d
                    
                if res == 2:
                    self.target = self.pos.copy()
                    break
            steps += 1

def p1():
    for line in fileinput.input():
        bot = LabBot(line)
        bot.walk_p1()
        print(bot.distances[tuple(bot.target)])
p1()

def p2():
    for line in fileinput.input():
        bot = LabBot(line)
        bot.walk_p2()
        print(max(bot.distances.values()))
p2()
        
