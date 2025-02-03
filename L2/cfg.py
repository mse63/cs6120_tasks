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

for i, instr in enumerate(instrs):
    if "op" in instr and "labels" in instr:
        for label in instr["labels"]:
            cfg[i].append(labels_to_indices[label])
    elif i != len(instrs) - 1:
        cfg[i].append(i + 1)

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
    connectionstyle="arc3,rad=0.1"
)

plt.title("Control Flow Graph")
plt.show()
