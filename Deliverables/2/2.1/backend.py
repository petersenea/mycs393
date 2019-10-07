import json
import functools


"""
    sorts and formats special_json_list
"""
def sort(special_json_list):
    
    special_json_list.sort(key = functools.cmp_to_key(_is_greater))
    return special_json_list


"""
    ########### private helper functions ##########
"""

"""
    returns the placement order of an object by type only
"""
def _sort_order(item):
    if isinstance(item, float) or isinstance(item, int):
        return 1
    elif isinstance(item, str):
        return 2
    elif isinstance(item, dict):
        return 3
    else:
        print(type(item))

"""
    compares elements to find order
"""
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



