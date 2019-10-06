import sys
from backend2 import sort
import json


special_json_list = []


i = 0
temp = ""

while i < 10:
    # remove newline character after each special json obj
    var = sys.stdin.readline().rstrip()

    if var != "":
        try:
            json.loads(var)
            special_json_list.append(var)
            i+=1
        except:
            temp += var
            try:
                json.loads(temp)
                special_json_list.append(temp)
                i+=1
                temp = ""
                # print("made a valid json")
            except:
                # print("haven't made a json yet")
                pass
            # print("not a valid json")
    
sorted_list = sort(special_json_list)

"""
special_json_list = []
# for i in range(10):
    
data = json.load(sys.stdin)
special_json_list.append(obj)

sorted_list = sort(special_json_list)
"""


"""
for event in ijson.parse(sys.stdin):
    print(event)
    special_json_list.append(event)

sorted_list = sort(special_json_list)
"""

sys.stdout.write(sorted_list)
