import sys
from backend2 import sort
import json

special_json_list = []

for i in range(10):
    var = sys.stdin.readline().rstrip()
    if var[0] == '"':
        var = var.strip('\"')
    special_json_list.append(var)

# sys.stdout.write(f'{special_json_list}')

sorted_list = sort(special_json_list)
# sorted_list = [12.4, 1100, 900000000, "banana", "big brown cow is hungry", "c", "ice cream", "toad", {"name": "potato pancakes"}, {"name": {"name": {"name": 5}}}]

# for i in range(1):
#     sorted_list[i] = float(special_json_list[i])

# sys.stdout.write(json.dumps(sorted_list))
json.dump(sorted_list, sys.stdout)