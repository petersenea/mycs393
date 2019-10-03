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

        # check if special_json is a number
        try:
            float(special_json)
            num_list.append(float(special_json))
        except (TypeError, ValueError):

            # check if special_json is a json object
            try:
                json_obj = json.loads(special_json)
                obj_list.append(json_obj)
            except:

                # check if special_json is a string
                if type(special_json) == str:
                    str_list.append(special_json)

                else:
                    print("not a string, json, or number")

    # take advantage of sorting algorithms for numbers and strings
    num_list.sort()
    str_list.sort()

    # call helper sorting function for json objects
    sorted_obj_list = _json_sort(obj_list)

    # sorted_obj_list = []

    # sorted_obj_list.append(sort(obj_list))

    sorted_json_list = num_list + str_list + sorted_obj_list

    return sorted_json_list


"""
    _json_sort():
"""

def _json_sort(obj_list):

    num_list = []
    str_list = []

    for obj in obj_list:
        print(obj['name'])
        try:
            float(obj['name'])
            num_list.append(obj)
        except (TypeError, ValueError):
            try:
                json_obj = json.loads(obj['name'])
                obj_list = _json_sort(obj['name'])

    return obj_list

print("Output list:")
print(sort(special_json_list))