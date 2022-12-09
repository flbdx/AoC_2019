#!/usr/bin/python3
#encoding: UTF-8

import sys
import fileinput
import itertools

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

def check_number_p1(number):
    if number < 100000 or number > 999999:
        return False
    
    digits = []
    for digit in range(1, 7):
        d = number // (10 ** (6 - digit))
        digits.append(d)
        number -= d * (10 ** (6 - digit))
    
    for i in range(1, 6):
        if digits[i] < digits[i - 1]:
            return False
    
    for k, g in itertools.groupby(digits):
        if len(list(g)) >= 2:
            return True
    
    return False

def test_p1():
    assert check_number_p1(111111) == True
    assert check_number_p1(223450) == False
    assert check_number_p1(123789) == False

test_p1()

def p1():
    for line in fileinput.input():
        rng = [int(n) for n in line.split("-")]
        total = 0
        for n in range(rng[0], rng[1] + 1):
            if check_number_p1(n):
                total += 1
        print((rng, total))
p1()

def check_number_p2(number):
    if number < 100000 or number > 999999:
        return False
    
    digits = []
    for digit in range(1, 7):
        d = number // (10 ** (6 - digit))
        digits.append(d)
        number -= d * (10 ** (6 - digit))
    
    for i in range(1, 6):
        if digits[i] < digits[i - 1]:
            return False
    
    for k, g in itertools.groupby(digits):
        if len(list(g)) == 2:
            return True
    
    return False

def test_p2():
    assert check_number_p2(123443) == False
    assert check_number_p2(112233) == True
    assert check_number_p2(123444) == False
    assert check_number_p2(111122) == True

test_p2()

def p2():
    for line in fileinput.input():
        rng = [int(n) for n in line.split("-")]
        total = 0
        for n in range(rng[0], rng[1] + 1):
            if check_number_p2(n):
                total += 1
        print((rng, total))
p2()
