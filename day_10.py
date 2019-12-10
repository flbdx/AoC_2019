#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import math

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

class Field(object):
    def __init__(self, lines):
        self.data = []
        y = 0
        for line in lines:
            x = 0
            for c in line:
                if c == '#':
                    self.data.append([x, y])
                x += 1
            y += 1
        
    def eqn(p1, p2):
        # ax + by + c = 0
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = -( b * p1[1] + a * p1[0])
        
        norm = math.gcd(a, b)
        a //= norm
        b //= norm
        c //= norm
        return (a, b, c)
    
    def dist(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def angle(p1, p2):
        return math.pi - math.atan2(p2[0] - p1[0], p2[1] - p1[1])
        
    
    def count_p1(self):
        best = None
        most = -1
        for s in self.data:
            count = 0
            for d in self.data:
                if s == d:
                    continue
                eqn_s_d = Field.eqn(s, d)
                
                p = s.copy()
                p[0] -= eqn_s_d[1]
                p[1] += eqn_s_d[0]
                blocked = False
                while p != list(d):
                    if p in self.data:
                        blocked = True
                        break
                    p[0] -= eqn_s_d[1]
                    p[1] += eqn_s_d[0]
                    
                if not blocked:
                    count += 1
            if count > most:
                most = count
                best = s
        return ((best, most))
    
    def vaporize(self, center, limit=200):
        angles = {}
        distances = {}
        
        for s in self.data:
            if s == center:
                continue
        
            a = Field.angle(center, s)
            if a in angles:
                angles[a].append(s)
                angles[a] = sorted(angles[a], key=lambda x: Field.dist(x, center))
            else:
                angles[a] = [s]
        
        p = None
        while limit != 0:
            for a in sorted(angles.keys()):
                p = angles[a].pop(0)
                if len(angles[a]) == 0:
                    del(angles[a])
                limit -= 1
                if limit == 0:
                    break
        return p
            

def test_p1():
    s = """.#..#
.....
#####
....#
...##""".split("\n")
    f = Field(s)
    assert f.count_p1() == ([3, 4], 8)
    
    s = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""".split("\n")
    f = Field(s)
    assert f.count_p1() == ([5, 8], 33)
    
    s = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""".split("\n")
    f = Field(s)
    assert f.count_p1() == ([1, 2], 35)
    
    s = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".split("\n")
    f = Field(s)
    assert f.count_p1() == ([11, 13], 210)
test_p1()

def p1():
    f = Field(fileinput.input())
    print(f.count_p1())
p1()


def test_p2():
    s = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".split("\n")
    f = Field(s)
    center = [11, 13]
    assert f.vaporize(center, limit=200) == [8, 2]
test_p2()

def p2():
    f = Field(fileinput.input())
    center, count = f.count_p1()
    print(f.vaporize(center, limit=200))
p2()
