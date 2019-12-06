#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_06"]

class Object(object):
    def __init__(self, name):
        self.name = name
        self.center = None
    def set_orbit(self, obj):
        self.center = obj
    def get_orbit(self):
        return self.center
    def get_name(self):
        return self.name
    
    #def __repr__(self):
        #r = ""
        #if self.center:
            #r += self.center.get_name()
        #else:
            #r += "None"
        
        #return r + " ) " + self.get_name()

def build_world_p1(lines):
    world = {}
    for line in lines:
        center, mobile = line.split(")")
        if not center in world:
            world[center] = Object(center)
        if not mobile in world:
            world[mobile] = Object(mobile)
    for line in lines:
        center, mobile = line.split(")")
        center_obj, mobile_obj = world[center], world[mobile]
        mobile_obj.set_orbit(center_obj)
    return world

def count_orbits(obj):
    c = obj.get_orbit()
    if c:
        return 1 + count_orbits(c)
    return 0

def count_orbits_p1(world):
    total = 0
    for obj in world:
        total += count_orbits(world[obj])
    return total

def test_p1():
    test_input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".split("\n")
    world = build_world_p1(test_input)
    assert count_orbits_p1(world) == 42
test_p1()

def p1():
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())
    world = build_world_p1(lines)
    print(count_orbits_p1(world))
p1()



def list_orbits(obj):
    c = obj.get_orbit()
    if c:
        return [obj] + list_orbits(c)
    return [obj]

def count_p2(world):
    orbits_you = list_orbits(world["YOU"])
    orbits_san = list_orbits(world["SAN"])
    dy = 0
    ds = 0
    for obj in orbits_you[1:]:
        ds = 0
        for obj2 in orbits_san[1:]:
            if obj == obj2:
                return dy + ds
            ds += 1
        dy += 1
    return -1

def test_p2():
    test_input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".split("\n")
    world = build_world_p1(test_input)
    assert count_p2(world) == 4
test_p2()

def p2():
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())
    world = build_world_p1(lines)
    print(count_p2(world))
p2()


