import sys
import json
# from sys.path import sort
# from "../deliverables/2/2.1/backend" import sort
from math import floor

sys.path.append('../Deliverables/2/2.1')
sys.path.append('../2.1')
from backend import sort


"""
original_json_obj_list = []
temp_json = ""

for line in sys.stdin:
    line = line.rstrip()
    if line != "":
        
        temp_json += line
        try:
            obj = json.loads(temp_json)
            original_json_obj_list.append(obj)
            temp_json = ""
        except:
            pass
num_full_lists = floor(len(original_json_obj_list) / 10)
split_json_lists = [original_json_obj_list[x:x+10] for x in range(0,num_full_lists*10, 10)]
# for x in chunks:
    # print(x)
list_sorted_lists = [sort(x) for x in split_json_lists]



# sorted_list = original_json_obj_list



sorted_list = json.dumps(list_sorted_lists)
sys.stdout.write(sorted_list)
"""



# holds all the objects read from stdin
original_json_obj_list = []

# holds beginning parts of a json
temp_json = ""


for line in sys.stdin:
    line = line.rstrip()

    line_words = line.split()

    for words in line_words:

        temp_json += " " + words
        try:
            obj = json.loads(temp_json)
            original_json_obj_list.append(obj)
            temp_json = ""
        except:
            pass 

num_full_lists = floor(len(original_json_obj_list) / 10)
split_json_lists = [original_json_obj_list[x:x+10] for x in range(0,num_full_lists*10, 10)]

list_sorted_lists = [sort(x) for x in split_json_lists]

sorted_list = json.dumps(list_sorted_lists)
sys.stdout.write(sorted_list)



"""
# holds all the objects read from stdin
original_json_obj_list = []

# holds beginning parts of a json
temp_json = ""


for line in sys.stdin:
    line = line.rstrip()

    # line_words = line.split()

    for char in line:

        temp_json += char
        try:
            obj = json.loads(temp_json)
            original_json_obj_list.append(obj)
            temp_json = ""
        except:
            pass 

num_full_lists = floor(len(original_json_obj_list) / 10)
split_json_lists = [original_json_obj_list[x:x+10] for x in range(0,num_full_lists*10, 10)]

list_sorted_lists = [sort(x) for x in split_json_lists]

sorted_list = json.dumps(list_sorted_lists)
sys.stdout.write(sorted_list)
"""
