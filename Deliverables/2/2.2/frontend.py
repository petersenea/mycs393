import sys
import json
from math import floor

sys.path.append('../Deliverables/2/2.1')
sys.path.append('../2.1')
from backend import sort


"""
    Main function calls the helper functions to read the json input, extract json objects, create lists
    containing 10 json objects each, sort the lists, and return the final json lists
"""
def main():
    str_json = _read_json_input()
    special_json_list = _extract_objects(str_json)
    split_json_lists = _create_ten_element_lists(special_json_list)
    list_sorted_lists = [sort(x) for x in split_json_lists]
    _output_lists(list_sorted_lists)
    

"""
    reads json input from stdin and compiles it into one string
"""
def _read_json_input():
    str_json = ""
    for line in sys.stdin:
        str_json += line
    return str_json


"""
    from the string compiled from the input extracts all json objects
"""
def _extract_objects(str_json):
    decoder = json.JSONDecoder()
    special_json_list = []
    while len(str_json)>0:
        try:
            obj, idx = decoder.raw_decode(str_json)
            str_json = str_json[idx:]
            special_json_list.append(obj)
        except:
            str_json = str_json[1:]
    return special_json_list


"""
    divides the list of json objects into smaller lists of 10 json objects
"""
def _create_ten_element_lists(special_json_list):
    num_full_lists = floor(len(special_json_list) / 10)
    split_json_lists = [special_json_list[x:x+10] for x in range(0,num_full_lists*10, 10)]
    return split_json_lists


"""
    outputs the list of lists of json objects as json
"""
def _output_lists(list_sorted_lists):
    sorted_list = json.dumps(list_sorted_lists)
    sys.stdout.write(sorted_list)

  
if __name__== "__main__":
  main()