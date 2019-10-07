import sys
import json
from backend import sort



special_json_list = []

num_objs = 0
str_json = ""
decoder = json.JSONDecoder()


for line in sys.stdin:
    str_json += line

while len(str_json)>0 or num_objs<10:
    try:
        obj, idx = decoder.raw_decode(str_json)
        str_json = str_json[idx:]
        special_json_list.append(obj)
        num_objs += 1
    except:
        str_json = str_json[1:]
    


if num_objs == 10:
    sorted_list = sort(special_json_list)
    sorted_list = json.dumps(sorted_list)

    sys.stdout.write(sorted_list)
