#!/usr/bin/python3
#encoding: UTF-8

import sys
import fileinput

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

def manathan(p):
    return sum(abs(v) for v in p)

# construire la liste des points intermédiaires
def build_segments(line):
    points = []
    p = [0, 0]
    points.append(tuple(p))
    instructions = {'R': (0,1), 'L': (0, -1), 'U': (1, 1), 'D': (1, -1)}
    for word in line.split(","):
        d,l = word[0], int(word[1:])
        d = instructions[d]
        p[d[0]] += d[1] * l
        points.append(tuple(p))
    return points

# retourne l'intersection de 2 segments ou None. Les segments sont forcément parallèles à l'un des axes
def intersect(p11, p12, p21, p22):
    x, y, sx, sy = [None]*4
    if p11[0] == p12[0] and p21[1] == p22[1]:
        x = p11[0]
        y = p21[1]
        sx = [p21[0], p22[0]]
        sy = [p11[1], p12[1]]
    if p11[1] == p12[1] and p21[0] == p22[0]:
        x = p21[0]
        y = p11[1]
        sx = [p11[0], p12[0]]
        sy = [p21[1], p22[1]]
    if x and x >= min(sx) and x <= max(sx) and y >= min(sy) and y <= max(sy):
        return (x, y)
    return None

def work_p1(line1, line2):
    pl1 = build_segments(line1)
    pl2 = build_segments(line2)
    best = None
    best_d = 0
    
    p11 = pl1[0]
    for p12 in pl1[1:]:
        p21 = pl2[0]
        for p22 in pl2[1:]:
            i = intersect(p11, p12, p21, p22)
            if i:
                d = manathan(i)
                if d != 0 and (best == None or d < best_d):
                    best_d = d
                    best = i
            p21 = p22
        p11 = p12
    return (best, best_d)

def test_p1():
    best, best_d = work_p1("R8,U5,L5,D3", "U7,R6,D4,L4")
    
    if best_d != 6 or best != (3,3):
        raise Exception("test_p1")

test_p1()

def p1():
    with fileinput.input() as f:
        best, best_d = work_p1(f.readline(), f.readline())
        print((best, best_d))
p1()

def distance2(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def work_p2(line1, line2):
    pl1 = build_segments(line1)
    pl2 = build_segments(line2)
    
    best = None
    best_d = 0
    
    
    p11 = pl1[0]
    d1 = 0
    for p12 in pl1[1:]:
        p21 = pl2[0]
        d2 = 0
        for p22 in pl2[1:]:
            i = intersect(p11, p12, p21, p22)
            if i:
                di1 = distance2(i, p11)
                di2 = distance2(i, p21)
                di = di1 + di2 + d1 + d2
                if di != 0 and (best == None or di < best_d):
                    best_d = di
                    best = i
            d2 += distance2(p21, p22)
            p21 = p22
        d1 += distance2(p11, p12)
        p11 = p12
    return (best, best_d)

def test_p2():
    best, best_d = work_p2("R8,U5,L5,D3", "U7,R6,D4,L4")
    if best_d != 30 or best != (6,5):
        raise Exception("test_p2")
test_p2()

def p2():
    with fileinput.input() as f:
        best, best_d = work_p2(f.readline(), f.readline())
        print((best, best_d))
p2()
