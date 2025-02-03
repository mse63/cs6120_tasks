import json
import sys

with open(sys.argv[1], "r") as file:
    data = json.load(file)

recursion_count = 0;

for function in data["functions"]:
    function_name  = function["name"]
    for instr in function["instrs"]:
        if "op" in instr and instr["op"] == "call":
            recursion_count += instr["funcs"].count(function_name)
print(recursion_count)
