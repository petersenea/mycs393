import json

# start STDIN
#~~~~~~~~~~~~~~REMOVE FROM FINAL SUBMIT~~~~~~~~~~~~~~~~~
# f = open("input0", "r")
# if f.mode == "r":
#     special_json_list = f.read().split("\n")
#     print("Input list:")
#     print(special_json_list)



def sort(special_json_list):

    _insertion_sort(special_json_list, len(special_json_list))

    _format_list(special_json_list)

    return special_json_list

def _insertion_sort(special_json_list, n):
    
    if n <= 1:
        return
    
    _insertion_sort(special_json_list, n-1)
    last = special_json_list[n-1]
    j = n - 2

    while j >= 0 and _is_greater(special_json_list[j], last):
        special_json_list[j+1] = special_json_list[j]
        j = j - 1
    
    special_json_list[j+1] = last

def _is_greater(a, b):
    # print(f'a: {a}')
    # print(f'b: {b}')

    type_a, a = _type(a)
    # print(f'done a {type_a}')
    type_b, b = _type(b)
    # print(f'done b {type_b}')

    if type_a == "string":
        if type_b == "string":
            if a > b:
                return True
            else: 
                return False
        elif type_b == "number":
            return True
        elif type_b == "json":
            return False
    
    elif type_a == "number":
        if type_b == "string":
            return False
        elif type_b == "number":
            if a > b:
                return True
            else:
                return False
        elif type_b == "json":
            return False
    
    elif type_a == "json":
        if type_b == "string":
            return True
        elif type_b == "number":
            return True
        elif type_b == "json":
            # print(type(a["name"]))
            return _is_greater(a["name"], b["name"])
    
def _type(thing):
    if isinstance(thing, dict):
        return "json", thing

    else:
        try:
            float(thing)
            return "number", float(thing)

        except (TypeError, ValueError):

            try:
                json_obj = json.loads(thing)

                return "json", json_obj
            
            except ValueError:

                if type(thing) == str:
                    return "string", thing
                else:
                    print("not a string, json, or float")

"""
    Returns True if a string of type "number" is an int
""" 
def _is_int(number):
    a = float(number)
    b = int(a)
    return a == b
    
def _format_list(special_json_list):
    for i in range(len(special_json_list)):
        thing = special_json_list[i]
        type_thing, _ = _type(thing)
        if type_thing == "number":
            if _is_int(thing):
                special_json_list[i] = int(thing)
            else:
                special_json_list[i] = float(thing)

        elif type_thing == "json":
            special_json_list[i] = json.loads(thing)
            # special_json_list[i] = json.dumps(temp)
            print(type(special_json_list[i]))


        else:
            special_json_list[i] = thing





# print(f"Output List:  {sort(special_json_list)}")
