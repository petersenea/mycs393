import sys
import json
from backend import sort

original_json_obj_list = []
temp_json = ""

for line in sys.stdin:
    line = line.rstrip()
    if line != "":

        temp_json += line
        try:
            obj = json.loads(temp_json)
            original_json_obj_list.append(obj)
            num_objs += 1
            temp_json = ""
        except:
            pass

sorted_list = original_json_obj_list

sorted_list = json.dumps(sorted_list)
sys.stdout.write(sorted_list)
