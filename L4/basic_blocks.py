from collections import defaultdict

def make_basic_blocks(data):
    cfg = defaultdict(set)

    for function in data["functions"]:
        if function["name"] == "main":
            instrs = function["instrs"]

    labels_to_indices = dict()
    for (i, instr) in enumerate(instrs):
        if "label" in instr:
            labels_to_indices[instr["label"]] = i

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

    start_to_blocks = dict()

    for s_b, e_b in blocks:
        start_to_blocks[s_b] = (s_b, e_b)

    for i, (s_b, e_b) in enumerate(blocks):
        last_instr = instrs[e_b - 1]
        if "op" in last_instr and "labels" in last_instr:
            for label in last_instr["labels"]:
                cfg[(s_b, e_b)].add(start_to_blocks[labels_to_indices[label]])
        elif i != len(blocks) - 1:
            cfg[(s_b, e_b)].add(blocks[i + 1])

    return cfg

