import sys
import json
from backend import sort
from math import floor

original_json_obj_list = []
temp_json = ""
num_objs = 0

# list_sorted_lists = []

# stuff = sys.stdin.read()

for line in sys.stdin:
    line = line.rstrip()
    # print(line)
    if line != "":

        temp_json += line
        try:
            obj = json.loads(temp_json)
            original_json_obj_list.append(obj)
            num_objs += 1
            temp_json = ""
        except:
            pass

chunks = [original_json_obj_list[x:x+10] for x in range(0,floor(len(original_json_obj_list)/10)*10, 10)]
# for x in chunks:
    # print(x)
list_sorted_lists = [sort(x) for x in chunks]


# sorted_list = original_json_obj_list



sorted_list = json.dumps(list_sorted_lists)
sys.stdout.write(sorted_list)
