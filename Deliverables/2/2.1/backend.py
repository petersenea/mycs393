import json


f = open("input0", "r")
if f.mode == "r":
    special_json_list = f.read().split("\n")
    print("Input list:")
    print(special_json_list)



"""
    sort():
        list of special json objects -> list of special json objects
"""

def sort(special_json_list):
    num_list = []
    str_list = []
    obj_list = []

    for special_json in special_json_list:
        try:
            float(special_json)
            num_list.append(float(special_json))
        except ValueError:
            try:
                json_obj = json.loads(special_json)
                obj_list.append(json_obj)
            except:
                if type(special_json) == str:
                    str_list.append(special_json)
                else:
                    print("not a string, json, or number")

    num_list.sort()
    str_list.sort()

    print("Hello")
    print(len(obj_list))
    obj_list = _json_sort(obj_list)

    sorted_json_list = num_list + str_list + obj_list

    return sorted_json_list

"""
    _json_sort():
"""

# def _json_sort(obj_list):

#     for obj in obj_list:
#         print(obj['name'])
#         if type(obj["name"]) == str:

    
#     return obj_list

print("Output list:")
print(sort(special_json_list))