#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_01"]


def mass_to_fuel_p1(mass):
    return (mass // 3) - 2

def test_p1():
    assert mass_to_fuel_p1(1969) == 654
    assert mass_to_fuel_p1(100756) == 33583

test_p1()

def p1():
    total = 0
    for line in fileinput.input():
        total += mass_to_fuel_p1(int(line))
    return total
print(p1())




def mass_to_fuel_p2(mass):
    eqn = lambda m : (m//3) - 2
    t = 0
    while mass >= 9:
        r = eqn(mass)
        t += r
        mass = r
    return t

def test_p2():
    assert mass_to_fuel_p2(1969) == 966
    assert mass_to_fuel_p2(100756) == 50346

test_p2()

def p2():
    total = 0
    for line in fileinput.input():
        total += mass_to_fuel_p2(int(line))
    return total
print(p2())
