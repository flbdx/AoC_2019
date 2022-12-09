#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
import itertools
from collections import namedtuple, OrderedDict

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

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
    # si part_2, alors modifications pour 2ème partie
    def __init__(self, lines, part_2=False):
        self.world = {}
        self.start_positions = None
        self.keys = {}
        self.doors = {}
        
        for y, line in enumerate(lines):
            for x, c in enumerate(line.strip()):
                self.world[(x, y)] = c
                if c == '@':
                    self.start_positions = {'@': (x, y)}
                elif c.islower():
                    self.keys[(x, y)] = c
                elif c.isupper():
                    self.doors[(x, y)] = c
        
        
        # modification pour 2ème partie
        if part_2:
            start_pos = self.start_positions['@']
            self.start_positions = {'@': (start_pos[0]+1, start_pos[1]+1),
                                    '=': (start_pos[0]+1, start_pos[1]-1),
                                    '$': (start_pos[0]-1, start_pos[1]+1),
                                    '&': (start_pos[0]-1, start_pos[1]-1)}
            self.world[start_pos] = '#'
            self.world[(start_pos[0]+1, start_pos[1])] = '#'
            self.world[(start_pos[0]-1, start_pos[1])] = '#'
            self.world[(start_pos[0], start_pos[1]+1)] = '#'
            self.world[(start_pos[0], start_pos[1]-1)] = '#'
        
        # nouvelles marques pour les positions de départ : @=$&
        for s in self.start_positions:
            self.world[self.start_positions[s]] = s
        
        
        # précalculer les chemins entre les positions de départ et les clés, 
        # ainsi qu'entre les différentes clés
        # on stocke la distance et les portes rencontrées
        self.paths = {}
        #for s in self.start_positions:
            #self.paths[s] = self.__cache_paths(self.start_positions[s])
        #for key in self.keys:
            #self.paths[self.keys[key]] = self.__cache_paths(key)
        for s in self.start_positions:
            self.__cache_paths_2(s, self.start_positions[s])
        for key in self.keys:
            self.__cache_paths_2(self.keys[key], key)
        
        # un cache pour les nombreux appels à __rec_search
        # pas possible d'utiliser functools.lru_cache car les arguments ne sont pas hashables
        self.__rec_search_call_cache = {}
        
    
    def __cache_paths(self, position):
        if not isinstance(position, type( () )):
            position = tuple(position)
        
        # "structure"
        State = namedtuple("State", ["position", "dependencies"])
        # liste de noeuds à parcourir
        queue = [State(position, set())]
        # noeuds déjà parcouru position -> distance
        visited = {position: 0}
        
        paths = OrderedDict()
        
        distance = 1
        while len(queue) != 0:
            next_queue = []
            for s in queue:
                for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                    next_p = d.next(s.position)
                    if next_p in visited and visited[next_p] < distance: # déjà visité
                        continue
                    v = self.world[d.next(s.position)]
                    if v == "#": # brick wall
                        continue
                    
                    # est-ce une clé
                    if v.islower():
                        paths[v] = (distance, s.dependencies)
                    
                    next_s = State(next_p, s.dependencies.copy())
                    
                    # est-ce une porte
                    if v.isupper():
                        next_s.dependencies.add(v.lower()) # stocker les portes en minuscules pour simplifier les comparaisons
                    
                    # enregistrer le passage
                    visited[next_p] = distance
                    
                    # et continuer
                    next_queue.append(next_s)
            queue = next_queue
            distance += 1
        
        return paths
    
    def __cache_paths_2(self, key_name, position):
        if not isinstance(position, type( () )):
            position = tuple(position)
        
        if not key_name in self.paths:
            self.paths[key_name] = OrderedDict()
        
        # "structure"
        State = namedtuple("State", ["position", "dependencies"])
        # liste de noeuds à parcourir
        queue = [State(position, set())]
        # noeuds déjà parcouru position -> distance
        visited = {position: 0}
                
        distance = 1
        while len(queue) != 0:
            next_queue = []
            for s in queue:
                for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                    next_p = d.next(s.position)
                    if next_p in visited and visited[next_p] < distance: # déjà visité
                        continue
                    v = self.world[d.next(s.position)]
                    if v == "#": # brick wall
                        continue
                    
                    # est-ce une clé
                    if v.islower():
                        self.paths[key_name][v] = (distance, s.dependencies)
                    
                    next_s = State(next_p, s.dependencies.copy())
                    
                    # est-ce une porte
                    if v.isupper():
                        next_s.dependencies.add(v.lower()) # stocker les portes en minuscules pour simplifier les comparaisons
                    
                    # enregistrer le passage
                    visited[next_p] = distance
                    
                    # et continuer
                    next_queue.append(next_s)
            queue = next_queue
            distance += 1
            
    def __rec_search(self, points_names, keyring, missing_keys):
        best = -1
        
        if len(missing_keys) == 0:
            return 0
        
        cache_key = "".join(points_names) + "".join(keyring)
        if cache_key in self.__rec_search_call_cache:
            return self.__rec_search_call_cache[cache_key]
        
        for k in missing_keys:
            # trouver qui peut chopper la clé k
            for bot in points_names:
                # regarder si ce bot peut chopper cette clé
                if not k in self.paths[bot]:
                    continue
            
                # aller chopper k
                distance, dependencies = self.paths[bot][k]
                if best != -1 and best <= distance: # on a déjà mieux
                    continue
                if not keyring.issuperset(dependencies): # on ne peut pas ouvrir les portes pour attendre k
                    continue
                # continuer avec cette clé dans le keyring en remplaçant la position de ce bot par la clé
                r = self.__rec_search(points_names.difference({ bot }).union( { k } ), keyring.union({ k }) , missing_keys - { k })
                # est-ce qu'on progresse
                if best == -1 or (r != -1 and best > distance + r):
                    best = distance + r
        self.__rec_search_call_cache[cache_key] = best
        return best
    
    def work(self):
        res = self.__rec_search(set(self.start_positions.keys()), set(), set(self.keys.values()))
        return res

def test_p1():
    lines="""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""".split("\n")
    world = World(lines)
    assert world.work() == 86
    
    lines="""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""".split("\n")
    world = World(lines)
    assert world.work() == 81
    
    lines="""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""".split("\n")
    world = World(lines)
    assert world.work() == 136

test_p1()

def p1():
    world = World(fileinput.input(), False)
    print(world.work())
p1()

def test_p2():
    lines="""#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""".split("\n")
    world = World(lines, True)
    assert world.work() == 8
    
    lines="""#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############""".split("\n")
    world = World(lines, True)
    assert world.work() == 32
    
test_p2()

def p2():
    world = World(fileinput.input(), True)
    print(world.work())
p2()
