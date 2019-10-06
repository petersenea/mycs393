import sys
from backend2 import sort
import json

special_json_list = []


i = 0

while i < 10:
    # remove newline character after each special json obj
    var = sys.stdin.readline().rstrip()

    if var != "":
        special_json_list.append(var)
        i += 1

"""
for i in range(10):
    # remove newline character after each special json obj
    var = sys.stdin.readline().rstrip()
   
    special_json_list.append(var)
"""

sorted_list = sort(special_json_list)

# print(type(sorted_list))
# json.dump(sorted_list, sys.stdout,ensure_ascii=False)
sys.stdout.write(sorted_list)
