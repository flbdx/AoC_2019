#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_16"]

def pattern(digit, position):
     position = ((position + 1) % (digit * 4)) // digit
     return (0, 1, 0, -1)[position]

def phase(input_digits):
    for d in range(len(input_digits)):
        # NOTE: first "d" factors from the pattern are 0
        input_digits[d] = abs(sum(input_digits[i] * pattern(d + 1, i) for i in range(d, len(input_digits)))) % 10
    
def work_p1(line):
    digits = [int(c) for c in line]
    for i in range(100):
        phase(digits)
    return "".join([repr(c) for c in digits[:8]])

def phase_rev(input_digits):
    for d in range(len(input_digits)-1, 0, -1):
        input_digits[d-1] = (input_digits[d-1] + input_digits[d]) % 10

def work_p2(line):
    digits = [int(c) for c in line]
    offset = int(line[:7])
    digits *= 10000
    
    # NOTE: the given offset is well over half the sequence, close to the end
    #       the pattern parameters are all 1's in this part of the multiplication
    digits = digits[offset:]
    for i in range(100):
        phase_rev(digits)
    return "".join([repr(c) for c in digits[:8]])


def test_p1():
    assert work_p1("80871224585914546619083218645595") == "24176176"
    assert work_p1("19617804207202209144916044189917") == "73745418"
    assert work_p1("69317163492948606335995924319873") == "52432133"
    
test_p1()

def p1():
    for line in fileinput.input():
        print(work_p1(line.strip()))
p1()


def test_p2():
    assert work_p2("03036732577212944063491565474664") == "84462026"
    assert work_p2("02935109699940807407585447034323") == "78725270"
    assert work_p2("03081770884921959731165446850517") == "53553731"
test_p2()

def p2():
    for line in fileinput.input():
        print(work_p2(line.strip()))
p2()
