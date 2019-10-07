import sys
import json
# from sys.path import sort
# from "../deliverables/2/2.1/backend" import sort
from math import floor

sys.path.append('../Deliverables/2/2.1')
sys.path.append('../2.1')
from backend import sort


special_json_list = []

str_json = ""
decoder = json.JSONDecoder()


for line in sys.stdin:
    str_json += line

while len(str_json)>0:
    try:
        obj, idx = decoder.raw_decode(str_json)
        str_json = str_json[idx:]
        special_json_list.append(obj)
    except:
        str_json = str_json[1:]

num_full_lists = floor(len(special_json_list) / 10)
split_json_lists = [special_json_list[x:x+10] for x in range(0,num_full_lists*10, 10)]

list_sorted_lists = [sort(x) for x in split_json_lists]

sorted_list = json.dumps(list_sorted_lists)
sys.stdout.write(sorted_list)


