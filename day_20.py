#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
from collections import namedtuple

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

# Link = 
class Link(object):
    def __init__(self, a, b, w):
        if a < b:
            self.a = a
            self.b = b
            self.w = w
        else:
            self.b = a
            self.a = b
            self.w = w
    
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b
    
    def __hash__(self):
        return (self.a + self.b).__hash__()
    
    def __repr__(self):
        return "[{0}-{1} : {2}]".format(self.a, self.b, self.w)
    
    def other(self, v):
        return self.b if v == self.a else self.a

Node = namedtuple("Node", ["name", "links"])


class Direction(Enum):
    UP = ord('^')
    DOWN = ord('v')
    LEFT = ord('<')
    RIGHT = ord('>')
    
    def next(self, p):
        if self == Direction.UP:
            return (p[0], p[1] - 1)
        if self == Direction.RIGHT:
            return (p[0] + 1, p[1])
        if self == Direction.DOWN:
            return (p[0], p[1] + 1)
        if self == Direction.LEFT:
            return (p[0] - 1, p[1])

class World(object):
    def __init__(self, lines):
        self.world = {}

        # lecture de toute l'entrée
        for y, line in enumerate(lines):
            for x, c in enumerate(line.strip("\n")):
                self.world[(x, y)] = c
        
        width = max(p[0] for p in self.world) - 4 + 1
        height = max(p[1] for p in self.world) - 4 + 1

        # recherche trou du donut
        x, y = 2, 2 + height // 2
        while self.world[(x, y)] in ['.', '#']:
            x += 1
        center_left = x
        while self.world[(x, y)] not in ['.', '#']:
            x += 1
        center_right = x - 1
        x, y = 2 + width // 2, 2
        while self.world[(x, y)] in ['.', '#']:
            y += 1
        center_top = y
        while self.world[(x, y)] not in ['.', '#']:
            y += 1
        center_bottom = y - 1
        
        self.outer_nodes_pos = set()
        self.inner_nodes_pos = set()

        # scan des portes à l'extérieur, concaténer les 2 caractères
        for x in range(2, 2+width):
            c = self.world[(x, 1)]
            if c != " ":
                self.world[(x, 1)] = self.world[(x, 0)] + c
                self.world[(x, 0)] = ' '
                self.outer_nodes_pos.add((x, 1))
            c = self.world[(x, 2 + height)]
            if c != " ":
                self.world[(x, 2 + height)] = c + self.world[(x, 3 + height)]
                self.world[(x, 3 + height)] = ' '
                self.outer_nodes_pos.add((x, 2 + height))
        for y in range(2, 2 + height):
            c = self.world[(1, y)]
            if c != " ":
                self.world[(1, y)] = self.world[(0, y)] + c
                self.world[(0, y)] = ' '
                self.outer_nodes_pos.add((1, y))
            c = self.world[(2 + width, y)]
            if c != " ":
                self.world[(2 + width, y)] = c + self.world[(3 + width, y)]
                self.world[(3 + width, y)] = ' '
                self.outer_nodes_pos.add((2 + width, y))
        
        # scan des portes à l'intérieur
        for x in range(center_left, center_right + 1):
            c = self.world[(x, center_top)]
            if c != " ":
                self.world[(x, center_top)] = c + self.world[(x, center_top + 1)]
                self.world[(x, center_top + 1)] = ' '
                self.inner_nodes_pos.add((x, center_top))
            c = self.world[(x, center_bottom)]
            if c != " ":
                self.world[(x, center_bottom)] = self.world[(x, center_bottom - 1)] + c
                self.world[(x, center_bottom - 1)] = ' '
                self.inner_nodes_pos.add((x, center_bottom))
        for y in range(center_top, center_bottom + 1):
            c = self.world[(center_left, y)]
            if c != " ":
                self.world[(center_left, y)] = c + self.world[(center_left + 1, y)]
                self.world[(center_left + 1, y)] = ' '
                self.inner_nodes_pos.add((center_left, y))
            c = self.world[(center_right, y)]
            if c != " ":
                self.world[(center_right, y)] = self.world[(center_right - 1, y)] + c
                self.world[(center_right - 1, y)] = ' '
                self.inner_nodes_pos.add((center_right, y))
    
    def __gen_graph(world):
        node_names = set([v for v in world.values() if v not in [' ', '#', '.']])
        nodes = {}
        for node_name in node_names:
            node = Node(node_name, set())
            nodes[node_name] = node
            
            for start_pos in [p for p, v in world.items() if v == node_name]:
                visited = {start_pos: 0}
                queue = [start_pos]
                distance = 0
                while len(queue) != 0:
                    next_queue = []
                    for pos in queue:
                        for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                            next_p = d.next(pos)
                            if next_p in visited and visited[next_p] < distance:
                                continue
                            v = world.get(next_p, None)
                            if v == "#" or v == " ":
                                continue
                            if v == ".":
                                next_queue.append(next_p)
                            else:
                                link = Link(node_name, v, distance)
                                node.links.add(link)
                            visited[next_p] = distance
                    distance += 1
                    queue = next_queue
        return nodes

    def work_p1(self):
        node_names = set([v for v in self.world.values() if v not in [' ', '#', '.']])
        nodes = World.__gen_graph(self.world)
        
        # Dijkstra
        distances = {n:float("inf") for n in node_names}
        distances["AA"] = 0
        subgraph = set()
        subgraph_complement = node_names.copy()
        
        while True:
            if len(subgraph_complement) == 0:
                break
            min_d = min({distances[n] for n in subgraph_complement})
            
            for node_name in [n for n in subgraph_complement if distances[n] == min_d]:
                node = nodes[node_name]
                for link in node.links:
                    other_node_name = link.other(node_name)
                    new_d = min_d + link.w
                    if new_d < distances[other_node_name]:
                        distances[other_node_name] = new_d
            min_d = min({distances[n] for n in subgraph_complement})
            best_node = next(n for n in subgraph_complement if distances[n] == min_d)
            subgraph.add(best_node)
            subgraph_complement.remove(best_node)
            if best_node == "ZZ":
                break
        return distances["ZZ"] - 1
    
    def work_p2(self, n_recs=30):
        def gen_subgraph(depth, last=False):
            world = self.world.copy()
            for pos in self.outer_nodes_pos:
                c = world[pos]
                if depth > 0 and c in ["AA", "ZZ"]:
                    world[pos] = '#'
                else:
                    world[pos] += repr(depth)
            for pos in self.inner_nodes_pos:
                world[pos] = "#" if last else world[pos] + repr(depth + 1)
            return World.__gen_graph(world)

        nodes = {}
        for depth in range(n_recs):
            new_nodes = gen_subgraph(depth, depth == n_recs - 1)
            for n_node in new_nodes.values():
                if n_node.name in nodes:
                    nodes[n_node.name].links.update(n_node.links)
                else:
                    nodes[n_node.name] = n_node

        node_names = set(nodes.keys())
        # Dijkstra
        distances = {n:float("inf") for n in node_names}
        distances["AA0"] = 0
        subgraph = set()
        subgraph_complement = node_names.copy()
        
        while True:
            if len(subgraph_complement) == 0:
                break
            min_d = min({distances[n] for n in subgraph_complement})
            
            for node_name in [n for n in subgraph_complement if distances[n] == min_d]:
                node = nodes[node_name]
                for link in node.links:
                    other_node_name = link.other(node_name)
                    new_d = min_d + link.w
                    if new_d < distances[other_node_name]:
                        distances[other_node_name] = new_d
            min_d = min({distances[n] for n in subgraph_complement})
            best_node = next(n for n in subgraph_complement if distances[n] == min_d)
            subgraph.add(best_node)
            subgraph_complement.remove(best_node)
            if best_node == "ZZ0":
                break
        return distances["ZZ0"] - 1

def test_p1():
    world = World(fileinput.input(files="input_20_t1"))
    assert world.work_p1() == 23
test_p1()

def p1():
    world = World(fileinput.input())
    print(world.work_p1())
p1()

def test_p2():
    world = World(fileinput.input(files="input_20_t1"))
    assert world.work_p2(2) == 26
    world = World(fileinput.input(files="input_20_t2"))
    assert world.work_p2(11) == 396
test_p2()

def p2():
    world = World(fileinput.input())
    print(world.work_p2(30))
p2()
