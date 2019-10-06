import sys
from backend import sort
import json

"""
########################## HELPER METHODS FOR CONVERTING STRING TO JSON ################################
"""

def _type_convert(thing):

    # check if thing is a dict, thus a json
    if isinstance(thing, dict):
        return thing
    elif _is_number(thing):
        return _to_float_or_int(float(thing))
    elif _is_json(thing):
        return json.loads(thing)
    elif isinstance(thing, str):
        return thing
    else:
        print('Error, unexpected', thing)

def _is_number(thing):
    try:
        float(thing)
        return True
    except (TypeError, ValueError):
        return False

def _to_float_or_int(thing):
    if thing.is_integer():
        return int(thing)
    else:
        return thing

def _is_json(thing):
    try:
        json_obj = json.loads(thing)
        return True            
    except ValueError:
        return False

"""
########################## START READING FROM STDIN ################################
"""

special_json_list = []

i = 0
temp = ""

while i < 10:
    # remove newline character after each special json obj
    var = sys.stdin.readline().rstrip()

    if var != "":
        try:
            obj = json.loads(var)
            special_json_list.append(obj)
            i+=1
        except:
            temp += var
            try:
                obj = json.loads(temp)
                special_json_list.append(obj)
                i+=1
                temp = ""
            except:
                pass

# special_json_list = [_type_convert(x) for x in special_json_list]
# special_json_list = [json.loads(x) for x in special_json_list]

sorted_list = sort(special_json_list)

sys.stdout.write(sorted_list)

