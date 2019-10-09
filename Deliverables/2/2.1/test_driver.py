import sys
import json
from backend import sort



special_json_list = []

num_objs = 0
str_json = ""
decoder = json.JSONDecoder()


for line in sys.stdin:
    str_json += line

# decodes the first 10 objects, 
# or all of the objects in the file if there are less than 10
while len(str_json)>0 or num_objs<10:
    try:
        obj, idx = decoder.raw_decode(str_json)
        str_json = str_json[idx:]
        special_json_list.append(obj)
        num_objs += 1
    except:
        str_json = str_json[1:]
    

# checks to make sure there are exactly 10 objects
if num_objs == 10:
    sorted_list = sort(special_json_list)
    sorted_list = json.dumps(sorted_list)

    sys.stdout.write(sorted_list)
