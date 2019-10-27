from interface_wrapper import InterfaceWrapper
import sys
import json
from game import Game

json_list = []

num_objs = 0
str_json = ""
decoder = json.JSONDecoder()


for line in sys.stdin:
    str_json += line

while len(str_json)>0:
    try:
        obj, idx = decoder.raw_decode(str_json)
        str_json = str_json[idx:]
        json_list.append(obj)
        num_objs += 1
    except:
        str_json = str_json[1:]


# ret_list = [InterfaceWrapper(obj).ret() for obj in json_list]

ret_list = Game(json_list).ret()

sys.stdout.write(json.dumps(ret_list))
