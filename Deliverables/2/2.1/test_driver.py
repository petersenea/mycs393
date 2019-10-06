import sys
import json
from backend import sort


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

sorted_list = sort(special_json_list)

sys.stdout.write(sorted_list)

