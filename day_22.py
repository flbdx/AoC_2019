#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_22"]


class Schuffle(object):
    def __init__(self, lines, size=10007):
        self.size = size
        self.ops = []
        self.track = {}
        
        for line in lines:
            if line.startswith("deal into new stack"):
                self.ops.append([Schuffle.__deal_into_new_stack])
            elif line.startswith("cut"):
                self.ops.append([Schuffle.__cut, int(line.split(" ")[-1])])
            elif line.startswith("deal with increment"):
                self.ops.append([Schuffle.__deal_with_increment, int(line.split(" ")[-1])])
    
    def exec(self, track, times=1):
        self.track = {v:v for v in track}
        
        for t in range(times):
            for i in self.ops:
                i[0](self, *i[1:])
        
        return self.track.copy()
    
    def __deal_into_new_stack(self):
        for name, p in self.track.items():
            self.track[name] = self.size - p - 1
    
    def __cut(self, n):
        for name, p in self.track.items():
            self.track[name] = (p - n) % self.size
    
    def __deal_with_increment(self, n):
        for name, p in self.track.items():
            self.track[name] = (p * n) % self.size

def test_p1():
    lines="""deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""".split("\n")
    schuffle = Schuffle(lines, 10)
    track = schuffle.exec(range(10))
    track = {v:k for k, v in track.items()}
    assert [track[v] for v in range(10)] == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

test_p1()

def p1():
    schuffle = Schuffle(fileinput.input())
    track = schuffle.exec([2019])
    print(track)
p1()

def test_p2():
    deck_size = 10007
    schuffle = Schuffle(fileinput.input(), deck_size)
    
    def compo(n, c, d, q, p):
        t1 = (n * pow(d, q, p)) % p
        t2 = (1 - pow(d, q, p)) % p
        t2 = (t2 * pow(1 - d, p-2, p)) % p
        t2 = (c * d * t2) % p
        return (t1 - t2) % p
    
    track = schuffle.exec([0, 1], 1)
    print(track)
    incr_value = (track[1] - track[0]) % deck_size
    print("incr : " + repr(incr_value))
    cut_value = (-(track[0] * pow(incr_value, deck_size-2, deck_size))) % deck_size
    print("cut : " + repr(cut_value))
    assert compo(0, cut_value, incr_value, 1, deck_size) == 7408
    assert compo(2019, cut_value, incr_value, 1, deck_size) == 1498
test_p2()

def p2():
    deck_size = 119315717514047
    n_shuffles = 101741582076661
    schuffle = Schuffle(fileinput.input(), deck_size)
    track = schuffle.exec([0, 1])
    d = (track[1] - track[0]) % deck_size
    print(("incr", d))
    c = (-(track[0] * pow(d, deck_size-2, deck_size))) % deck_size
    print(("cut", c))
    
    def calc(target, c, d, q, p):
        t = (1 - pow(d, q, p)) % p
        t = (t * pow(1 - d, p - 2, p)) % p
        t = (c * d * t) % p
        t = (t + target) % p
        t = (t * pow(pow(d, q, p), p-2, p)) % p
        return t
    
    print(calc(2020, c, d, n_shuffles, deck_size))
p2()
