import json
import functools

"""
    sorts and formats special_json_list
"""
def sort(special_json_list):

    _insertion_sort(special_json_list)

    _format_list(special_json_list)

    return special_json_list

"""
    ########### private helper functions ###########
"""

"""
    Insertion Sorts special_json_list in place in ascending order
"""
def _insertion_sort(special_json_list):
    
    for i in range(1,len(special_json_list)):

        value = special_json_list[i]

        j = i - 1
        while j >= 0 and _is_greater(special_json_list[j], value):
            special_json_list[j+1] = special_json_list[j]
            j -= 1
        special_json_list[j+1] = value



"""
    Returns True if a is greater than b, False otherwise
"""
def _is_greater(a, b):

    type_a, a = _type(a)
    type_b, b = _type(b)

    if type_a == type_b:

        # both a and b are jsons, so run _is_greater on their "name" values recursively
        if type_a == 3:
            return _is_greater(a["name"], b["name"])
        else:
            return a > b

    # a and b are different types and thus follow type hierarchy of json > string > number
    else:
        return type_a > type_b



"""
    Returns the type of the input (one of 1 (for numbers), 2 (for strings), or 3 (for jsons)) and the input converted from string or dict to its type
"""
def _type(thing):

    # check if thing is a dict, thus a json
    if isinstance(thing, dict):
        return 3, thing

    else:

        # check if string thing is a float, thus a number
        try:
            float(thing)
            return 1, float(thing)

        except (TypeError, ValueError):

            # check if string thing is a json object, thus a json
            try:
                json_obj = json.loads(thing)

                return 3, json_obj
            
            except ValueError:

                # check if string thing is a string, not strictly necessary but is useful for clear code
                if type(thing) == str:
                    return 2, thing
                else:
                    print("not a string, json, or float")



"""
    Returns True if a string of type "number" is an int
""" 
def _is_int(number):
    a = float(number)
    b = int(a)
    return a == b


    
"""
    Converts all of the elements of special_json_list into their appropriate types
"""
def _format_list(special_json_list):
    for i in range(len(special_json_list)):
        thing = special_json_list[i]
        type_thing, _ = _type(thing)
        if type_thing == 1:
            if _is_int(thing):
                special_json_list[i] = int(thing)
            else:
                special_json_list[i] = float(thing)

        elif type_thing == 3:
            special_json_list[i] = json.loads(thing)
            # special_json_list[i] = json.dumps(temp)
            print(type(special_json_list[i]))

        else:
            special_json_list[i] = thing







'''
def _is_greater(a, b):

    type_a, a = _type(a)
    type_b, b = _type(b)

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
            return _is_greater(a["name"], b["name"])
'''




'''
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
'''