import json
import sys
from collections import defaultdict, namedtuple
import networkx as nx
import matplotlib.pyplot as plt

commutative_ops = {"add", "mul"}

#value completely encodes all that an instr can be
Value = namedtuple("Value", ["op", "args", "funcs", "labels", "var_name", "val_type" , "value"])

def delete_unused_variable_deadcode(program):
    num_deletions = 0
    for function in program["functions"]:
        used_variables = set()
        instrs = function["instrs"]
        used_variables = set()
        for instr in instrs:
            if "args" in instr:
                used_variables.update(instr["args"])
        new_instrs = list()
        for instr in instrs:
            if "dest" in instr and instr["dest"] not in used_variables:
                num_deletions += 1
            else:
                new_instrs.append(instr)
        function["instrs"] = new_instrs

    # print(f"Deleted {num_deletions} unused variable instructions", file=sys.stderr)
    return num_deletions

def delete_overwritten_variable_deadcode(program):
    num_deletions = 0
    for function in program["functions"]:
        #loop through function backwards. Future vars is the set of variables that are written to later. Therefore, if we see a write to a variable in future_vars, we know we can ignore it.
        #Entering a new basic block must reset future_vars
        future_vars = set()

        instrs = function["instrs"]
        new_instrs = list()
        for instr in reversed(instrs):
            #these indicate instructions that terminate basic blocks
            if "label" in instr or "labels" in instr:
                future_vars = set()
            if "dest" in instr:
                if instr["dest"] in future_vars:
                    #this is a redundant write, so skip this instructions
                    num_deletions += 1
                    continue
                else:
                    future_vars.add(instr["dest"])
            if "args" in instr:
                #if a variable is used, we remove it from future_vars,
                #since previous writes were not redundant
                for arg in instr["args"]:
                    if arg in future_vars:
                        future_vars.remove(arg)
            #if you've gotten this far, your instr isn't dead
            new_instrs.append(instr)
        function["instrs"] = list(reversed(new_instrs))
    # print(f"Deleted {num_deletions} overwritten variable instructions", file=sys.stderr)
    return num_deletions

def lvn(program):
    num_changes = 0
    for function in program["functions"]:
        instrs = function["instrs"]
        new_instrs = list()
        next_id = 0
        id_to_vars = defaultdict(list)
        val_to_id = dict()
        id_to_val = dict()
        var_to_id = dict()

        def new_id_from_var_name(var_name):
            nonlocal next_id
            next_id += 1
            id_to_vars[next_id].append(var_name)
            val = Value(
                op=None,
                args=None,
                funcs=None,
                labels=None,
                var_name=var_name,
                val_type=None,
                value=None,
                )
            val_to_id[val] = next_id
            id_to_val[next_id] = val
            var_to_id[var_name] = next_id
            return next_id

        def new_id_from_val(val, var_name):
            nonlocal next_id
            next_id += 1
            id_to_vars[next_id].append(var_name)
            val_to_id[val] = next_id
            id_to_val[next_id] = val
            var_to_id[var_name] = next_id

            return next_id

        def new_block():
            #when we enter a new block, clear all
            nonlocal next_id
            nonlocal id_to_vars
            nonlocal val_to_id
            nonlocal id_to_val
            nonlocal var_to_id
            next_id = 0
            id_to_vars = defaultdict(list)
            val_to_id = dict()
            id_to_val = dict()
            var_to_id = dict()

        unique_count = 0
        for instr in instrs:
            # print("id_to_vars", id_to_vars, file=sys.stderr)
            # print("val_to_id", val_to_id, file=sys.stderr)
            # print("var_to_id",var_to_id, file=sys.stderr)
            # print("\n\n", file=sys.stderr)
            # print(instr, file=sys.stderr)
            if "label" in instr:
                new_instrs.append(instr)
                new_block()
                continue

            op = None
            args = None
            funcs = None
            labels = None
            var_name = None
            const_value = None
            val_type = 0
            if "op" in instr:
                op = instr["op"]
                if op in {"alloc", "call"}:
                    op += str(unique_count)
                    unique_count += 1
            if "args" in instr:
                args = list()
                for arg in instr["args"]:
                    if arg in var_to_id:
                        args.append(var_to_id[arg])
                        continue
                    new_id = new_id_from_var_name(arg)
                    args.append(new_id)

                #Exploiting Commutativity
                if instr.get("op") in commutative_ops:
                    args.sort()
                args = tuple(args)
            if "funcs" in instr:
                funcs = tuple(instr["funcs"])
            if "labels" in instr:
                labels = tuple(instr["labels"])
            if "value" in instr:
                const_value = instr["value"]
            if "type" in instr:
                val_type = instr["type"]
                if isinstance(val_type, dict):
                    val_type = tuple(sorted(val_type.items()))
            val = Value(op=op, args=args, funcs=funcs, labels=labels, var_name= var_name, val_type=val_type ,value=const_value)

            #copy propogation. If this is "id x", make val the val of x, instead of a new "id x" value
            if val.op == "id":
                source_var = instr["args"][0]
                if source_var in var_to_id:
                    val = id_to_val[var_to_id[source_var]]
                else:
                    source_var_id = new_id_from_var_name(source_var)
                    val = id_to_val[source_var_id]

            var = instr.get("dest")
            old_id = None
            if var in var_to_id:
                old_id = var_to_id[var]
            if val in val_to_id and len(id_to_vars[val_to_id[val]]) > 0:
                val_id = val_to_id[val]
                canonical_var = id_to_vars[val_id][0]

                #constant propogation
                if val.op == "const":
                    new_instrs.append({"op": "const", "dest": var, "type": instr["type"], "value":  val.value })
                else:
                    new_instrs.append({"op": "id", "args": [canonical_var], "dest": var, "type": instr["type"]})

                id_to_vars[val_id].append(var)
                val_to_id[val] = val_id
                id_to_val[val_id] = val
                var_to_id[var] = val_id
            else:
                if var is not None:
                    new_id = new_id_from_val(val, var)
                if "args" in instr:
                    instr["args"] = []
                    for val_id in val.args:
                        canonical_var = id_to_vars[val_id][0]
                        instr["args"].append(canonical_var)
                new_instrs.append(instr)

            #do this shenaniganry so that the old variable is still available
            if old_id is not None:
                id_to_vars[old_id].remove(var)

            if instr.get("op") == "jmp" or instr.get("op") == "br":
                new_block()

        function["instrs"] = new_instrs

program = json.load(sys.stdin)
num_deletions = True
while num_deletions:
    num_deletions = 0
    lvn(program)
    num_deletions += delete_unused_variable_deadcode(program)
    num_deletions += delete_overwritten_variable_deadcode(program)

print(json.dumps(program, indent = 2))
