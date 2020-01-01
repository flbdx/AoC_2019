#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from intcodecomp import IntComputer
import readline

if len(sys.argv) == 1:
    sys.argv += ["input_25"]

def prog_to_memory(prog):
    n = 0
    res = {}
    for v in prog.split(','):
        res[n] = int(v)
        n += 1
    return res

def p1():
    for line in fileinput.input():
        mem = prog_to_memory(line)
        comp = IntComputer()
        comp.set_mem(mem.copy())
        
        # this is juste an autoplayer taylored for my input
        
        paths=[]
        #take coin
        paths.append("NE")
        # take food ration,sand,astrolab
        paths.append("SWNNE")
        # take cake,weather machine,ornament,jam
        paths.append("ESWW")
        
        blacklist=["infinite loop", "photons", "giant electromagnet", "molten lava", "escape pod"]
        directions={"N": "north", "E": "east", "W": "west", "S": "south"}
        inv_directions={"S": "north", "W": "east", "E": "west", "N": "south"}
        
        items=[]
        
        # to security checkpoint
        paths.append("EEEE")
        
        
        def run():
            comp.run()
            s = "".join(chr(v) for v in comp.outputs)
            if len(s):
                print(s)
            comp.clear_outputs()
            return s
        
        # catch every items and stop on the security checkpoint
        for path in paths:
            for d in path:
                print(directions[d])
                comp.push_inputs(ord(c) for c in directions[d]+"\n")
            
                s = run()
                
                try:
                    item_idx = s.index("Items here:")
                    for line in s[item_idx:].splitlines():
                        if line.startswith("- "):
                            item = line.strip()[2:]
                            if not item in blacklist:
                                cmd = "take {0}\n".format(item)
                                print(cmd)
                                comp.push_inputs(ord(c) for c in cmd)
                                items.append(item)
                                run()
                except:
                    pass
                
            
            if "Security Checkpoint" in s:
                break
            
            # back to Hull Breach
            for d in path[::-1]:
                print(inv_directions[d])
                comp.push_inputs(ord(c) for c in inv_directions[d]+"\n")
            
                run()
        
        
        # drop all items
        for item in items:
            comp.push_inputs(ord(c) for c in "drop {0}\n".format(item))
        run()
        
        # security checkpoint out direction
        sec_out_dir = "south"
        
        # use gray codes to iterate over the item combinations
        item_states = [False for i in range(len(items))]
        for i in range(1, 1<<len(items)):
            state = i ^ (i >> 1)
            for bit in range(len(items)):
                if (state & (1 << bit)) != 0 and not item_states[bit]:
                    comp.push_inputs(ord(c) for c in "take {0}\n".format(items[bit]))
                    item_states[bit] = True
                elif (state & (1 << bit)) == 0 and item_states[bit]:
                    comp.push_inputs(ord(c) for c in "drop {0}\n".format(items[bit]))
                    item_states[bit] = False
            comp.push_inputs(ord(c) for c in "{0}\n".format(sec_out_dir))
            s = run()
            if "Security Checkpoint" not in s:
                break
                
p1()
