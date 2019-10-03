import sys
from backend2 import sort
import json

special_json_list = []

for i in range(10):
    var = sys.stdin.readline().rstrip()
    if var[0] == '"':
        var = var.strip('\"')
    # print(var)
    special_json_list.append(var)

# sys.stdout.write(f'{special_json_list}')

sorted_list = sort(special_json_list)

# for i in range(1):
#     sorted_list[i] = float(special_json_list[i])

sys.stdout.write(json.dumps(special_json_list))