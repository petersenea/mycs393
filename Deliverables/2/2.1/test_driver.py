import sys
from backend2 import sort
import json

special_json_list = []

for i in range(10):
    # remove newline character after each special json obj
    var = sys.stdin.readline().rstrip()
   
    special_json_list.append(var)

sorted_list = sort(special_json_list)

# print(type(sorted_list))
# json.dump(sorted_list, sys.stdout,ensure_ascii=False)
sys.stdout.write(sorted_list)
