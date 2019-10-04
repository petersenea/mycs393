import sys
from backend2 import sort
import json

special_json_list = []

for i in range(10):
    # remove newline character after each special json obj
    var = sys.stdin.readline().rstrip()

    # remove additional "" marks from strings to avoid confusion between json objects and strings
    if var[0] == '"':
        var = var.strip('\"')
    
    special_json_list.append(var)

sorted_list = sort(special_json_list)

for i in sorted_list:
    print(type(i))

# json.dump(sorted_list, sys.stdout)
sys.stdout.write(sorted_list)
