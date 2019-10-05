import json
import functools




"""
    sorts and formats special_json_list
"""
def sort(special_json_list):
    special_json_list = [_type_convert(x) for x in special_json_list]
    special_json_list.sort(key = functools.cmp_to_key(_is_greater))

    special_json_list = json.dumps(special_json_list)

    return special_json_list



"""
    ########### private helper functions ##########
"""


def _sort_order(item):
    # print(f'{item}: {type(item)}')
    if isinstance(item, float) or isinstance(item, int):
        return 1
    elif isinstance(item, str):
        return 2
    elif isinstance(item, dict):
        return 3
    else:
        # print(type(item))
        print(item)
        # pass


def _is_greater(a, b):

    # determine the types of a and b, and convert them to their types
    order_a = _sort_order(a)
    order_b = _sort_order(b)

    if order_a == order_b:

        # both a and b are jsons, so run _is_greater on their "name" values recursively
        if isinstance(a, dict):
            return _is_greater(a["name"], b["name"])
        
        # both a and b are either strings or numbers, use python's > function
        else:
            if a > b:
                return 1
            elif a == b:
                return 0
            else:
                return -1

    # a and b are different types and thus follow type hierarchy of json > string > number
    else:
        if order_a > order_b:
            return 1
        else:
            return -1

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
        # pass

def _to_float_or_int(thing):
    if thing.is_integer():
        return int(thing)
    else:
        return thing

def _is_number(thing):
    try:
        float(thing)
        return True
    except (TypeError, ValueError):
        return False

def _is_json(thing):
    try:
        json_obj = json.loads(thing)
        return True            
    except ValueError:
        return False




"""
    Returns True if a string of type "number" is an int
""" 
'''
def _is_int(number):
    a = float(number)
    b = int(a)
    return a == b
'''
