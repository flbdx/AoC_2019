#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
import math

class System(object):
    class Moon:
        def __init__(self, x, y, z):
            self.position = [x, y, z]
            self.velocity = [0, 0, 0]
        
        def __repr__(self):
            return "pos=<x={0}, y={1}, z={2}>, vel=<x={3}, y={4}, z={5}>".format(*(self.position + self.velocity))
    
    def __init__(self, lines):
        self.moons = []
        
        prog = re.compile("<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>")
        for line in lines:
            res = prog.match(line)
            self.moons.append(System.Moon(int(res.group(1)), int(res.group(2)), int(res.group(3))))
    
    def gravity_velocity(self, axes=range(0, 3)):
        for m1_idx in range(len(self.moons)):
            m1 = self.moons[m1_idx]
            for m2_idx in range(m1_idx + 1, len(self.moons)):
                m2 = self.moons[m2_idx]
                for axe in axes:
                    d = -1 if m1.position[axe] > m2.position[axe] else 1 if m1.position[axe] < m2.position[axe] else 0
                    m1.velocity[axe] += d
                    m2.velocity[axe] -= d
            for axe in axes:
                m1.position[axe] += m1.velocity[axe]
        
    def run(self, n_steps):
        for n in range(n_steps):
            self.gravity_velocity()
    
    def energy(self):
        total = 0
        for moon in self.moons:
            total += sum([abs(v) for v in moon.position]) * sum([abs(v) for v in moon.velocity])
        return total 
    
    def find_cycle(self):
        cycles = [None, None, None]
        for axe in range(0, 3):
            start_positions = []
            for moon in self.moons:
                start_positions.append(moon.position[axe])
            
            cont = True
            n_steps = 0
            while cont:
                self.gravity_velocity(axes=[axe])
                n_steps += 1
                cont = False
                for i in range(len(self.moons)):
                    if start_positions[i] != self.moons[i].position[axe]:
                        cont = True
                        break
                    if self.moons[i].velocity[axe] != 0:
                        cont = True
                        break
            cycles[axe] = n_steps
        def lcm(a, b):
            return a * b // math.gcd(a, b)
        return lcm(lcm(cycles[0], cycles[1]), cycles[2])

if len(sys.argv) == 1:
    sys.argv += ["input_12"]

def test_p1():
    s="""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""".split("\n")
    system = System(s)
    system.run(100)
    assert system.energy() == 1940
test_p1()

def p1():
    system = System(fileinput.input())
    system.run(1000)
    print(system.energy())
p1()

def test_p2():
    s="""<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""".split("\n")
    system = System(s)
    assert system.find_cycle() == 2772
test_p2()

def p2():
    system = System(fileinput.input())
    print(system.find_cycle())
p2()
