import sys
import json
from basic_blocks import make_basic_blocks
from collections import namedtuple, defaultdict

reaching_definitions = set()

Defn = namedtuple("Defn", ["instr_id", "variable"])

with open(sys.argv[1], "r") as file:
    program = json.load(file)

cfg = make_basic_blocks(program)
preds = defaultdict(set)

for x in cfg:
    for elem in cfg[x]:
        preds[elem].add(x)

for function in program["functions"]:
    if function["name"] == "main":
        instrs = function["instrs"]
        args = set([arg ["name"] for arg in function["args"]])

def transfer(b, in_b):
    defs = defaultdict(set)
    for b_elem in in_b:
        defs[b_elem.variable].add(b_elem.instr_id)

    for i in range(b[0], b[1]):
        instr = instrs[i]
        if "dest" in instr:
            defs[instr["dest"]] = {i}

    ans = set()
    for variable in defs:
        for instr_id in defs[variable]:
            ans.add(Defn(variable=variable, instr_id = instr_id))
    return ans


in_blocks = dict()
out_blocks = defaultdict(set)

entry_in_args = {Defn(variable=arg["name"], instr_id = -1) for arg in function["args"]}

worklist = list(cfg)
while worklist:
    b = worklist.pop()
    old_out = out_blocks[b]
    if b[0] != 0:
        in_blocks[b] = set().union(*[out_blocks[p] for p in preds[b]])
    else:
        in_blocks[b] = entry_in_args

    out_blocks[b] = transfer(b, in_blocks[b])
    if out_blocks[b] != old_out:
        worklist += list(cfg[b])
for block in sorted(list(out_blocks)):
    print(block)
    for elem in sorted(out_blocks[block]):
        print("    ", elem.variable, elem.instr_id)
