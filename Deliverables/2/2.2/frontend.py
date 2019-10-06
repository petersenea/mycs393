import sys
import json
from backend import sort
from math import floor
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

"""

original_json_obj_list = []
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
# for x in chunks:
    # print(x)
list_sorted_lists = [sort(x) for x in split_json_lists]

sorted_list = json.dumps(list_sorted_lists)
sys.stdout.write(sorted_list)
"""


stdin_chunks = []
original_json_obj_list = []
temp_json = ""

for line in sys.stdin:
    if line != "":
        line_words = line.split()
        for word in line_words:
            stdin_chunks.append(word)

for thing in stdin_chunks:
    temp_json += thing
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