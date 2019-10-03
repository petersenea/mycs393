import sys
from backend2 import sort
import json

special_json_list = []

for i in range(10):
    var = sys.stdin.readline().rstrip()
    if var[0] == '"':
        var = var.strip('\"')
    special_json_list.append(var)

sorted_list = sort(special_json_list)

json.dump(sorted_list, sys.stdout)