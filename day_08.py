#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

PIX_W = 25
PIX_H = 6

def read_picture(line, pix_w=PIX_W, pix_h=PIX_H):
    layers = []
    layer_len = pix_w * pix_h
    while len(line) != 0:
        layer = []
        for i in range(layer_len):
            layer.append(int(line[i]))
        layers.append(layer)
        line = line[layer_len:]
    return layers

def test_p1():
    layers = read_picture("123456789012", 3, 2)
    assert len(layers) == 2
    assert len(layers[0]) == 6
    assert len(layers[1]) == 6
test_p1()

def count_elem(layer, v):
    c = 0
    for e in filter(lambda x: x == v, layer):
        c += 1
    return c

def work_p1(line):
    layers = read_picture(line)
    best_n_zeros = -1
    zero_layer = None
    for n in range(len(layers)):
        layer = layers[n]
        n_zeros = count_elem(layer, 0)
        if best_n_zeros == -1 or n_zeros < best_n_zeros:
            zero_layer = n
            best_n_zeros = n_zeros
    layer = layers[zero_layer]
    n_one = count_elem(layer, 1)
    n_two = count_elem(layer, 2)
    return n_one * n_two

def p1():
    for line in fileinput.input():
        print(work_p1(line.strip()))
p1()

def decode(layers):
    res = []
    layer_len = len(layers[0])
    
    for i in range(layer_len):
        r = -1
        for layer in layers:
            r = layer[i]
            if r != 2:
                break
        res.append(r)
    return res

def p2():
    for line in fileinput.input():
        layers = read_picture(line.strip())
        res = decode(layers)
        s = "".join(['#' if v == 1 else ' ' for v in res ])
        for h in range(PIX_H):
            print(s[h*PIX_W : (h+1)*PIX_W])
p2()
        
        
