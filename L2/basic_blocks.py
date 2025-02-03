import json
import sys
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

with open(sys.argv[1], "r") as file:
    data = json.load(file)

cfg = defaultdict(list)

for function in data["functions"]:
    if function["name"] == "main":
        instrs = function["instrs"]

labels_to_indices = dict()
for (i, instr) in enumerate(instrs):
    if "label" in instr:
        labels_to_indices[instr["label"]] = i
    print(instr)

#instead of a list of instructions, I'm just making the blocks tuples of the [start, end) indices of the blocks, because the blocks are always consecutive instructions.
blocks = []
prev_end = 0
for i, instr in enumerate(instrs):
    if "label" in instr:
        #start a new block, with this instr in the new block
        #if statement to avoid creating empty blocks
        if prev_end != i:
            blocks.append((prev_end, i))
        prev_end = i
    elif "op" in instr and "labels" in instr:
        #start a new block, with this instr in the old block
        blocks.append((prev_end, i + 1))
        prev_end = i + 1
    if i == len(instrs) - 1:
        #if statement needed for edge case where last instruction is a label.
        if prev_end != len(instrs):
            blocks.append((prev_end, len(instrs)))
print(blocks)

start_to_blocks = dict()

for s_b, e_b in blocks:
    start_to_blocks[s_b] = (s_b, e_b)

for i, (s_b, e_b) in enumerate(blocks):
    last_instr = instrs[e_b - 1]
    if "op" in last_instr and "labels" in last_instr:
        for label in last_instr["labels"]:
            cfg[(s_b, e_b)].append(start_to_blocks[labels_to_indices[label]])
    elif i != len(blocks) - 1:
        cfg[(s_b, e_b)].append(blocks[i + 1])

G = nx.DiGraph()

for src, targets in cfg.items():
    for tgt in targets:
        G.add_edge(src, tgt)

plt.figure(figsize=(10, 6))
pos = nx.spectral_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(
    G, pos,
    connectionstyle="arc3,rad=0.1"  # <-- THIS IS IT
)

plt.title("Control Flow Graph of Basic Blocks")
plt.show()
