import sys
import json
from backend import sort

"""
special_json_list = []

num_objs = 0
temp_json = ""

while num_objs < 10:
    # remove newline character after each special json obj
    line = sys.stdin.readline().rstrip()
    
    line_words = line.split()

    for words in line_words:

        temp_json += " " + words
        try:
            obj = json.loads(temp_json)
            special_json_list.append(obj)
            num_objs += 1
            temp_json = ""
        except:
            pass

sorted_list = sort(special_json_list)
sorted_list = json.dumps(sorted_list)

sys.stdout.write(sorted_list)
"""

special_json_list = []

num_objs = 0
temp_json_obj = ""
temp_json_str = ""
temp_json_num = ""
can_load_json = False


while num_objs < 10:

    line = sys.stdin.readline().rstrip()
    
    for char in line:

        if char == '"' and temp_json_obj == "" and temp_json_str = "" and temp_json_num = "":
            # start creating a string
            temp_json_str += char
        elif char == '"' and temp_json_str != "":
            # finish creating a string
            temp_json_str += char
            can_load_json = True
        elif temp_json_str != "":
            temp_json_str += char
        elif char == "{":

        elif can_load_json:
            try:
                obj = json.loads(temp_json)
                special_json_list.append(obj)
                num_objs += 1
                temp_json = ""
            except:
                pass
