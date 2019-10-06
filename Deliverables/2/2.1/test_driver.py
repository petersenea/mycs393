import sys
from backend2 import sort
import json
# import ijson

"""
special_json_list = []


i = 0

while i < 10:
    # remove newline character after each special json obj
    var = sys.stdin.readline().rstrip()

    if var != "":
        special_json_list.append(var)
        i += 1
"""


special_json_list = []
# for i in range(10):
    
data = json.load(sys.stdin)
special_json_list.append(obj)

sorted_list = sort(special_json_list)


"""
for event in ijson.parse(sys.stdin):
    print(event)
    special_json_list.append(event)

sorted_list = sort(special_json_list)
"""

sys.stdout.write(sorted_list)
