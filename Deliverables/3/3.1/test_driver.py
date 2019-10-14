from board import WrapperBoard
import sys
import json



json_list = []

num_objs = 0
str_json = ""
decoder = json.JSONDecoder()


for line in sys.stdin:
    str_json += line

# decodes the first 10 objects, 
# or all of the objects in the file if there are less than 10
while len(str_json)>0:
    try:
        obj, idx = decoder.raw_decode(str_json)
        str_json = str_json[idx:]
        json_list.append(obj)
        num_objs += 1
    except:
        str_json = str_json[1:]



ret_list = [WrapperBoard(obj).ret() for obj in json_list]

sys.stdout.write(json.dumps(ret_list))


"""
# Load data in from stdin, if not valid json, raises exception
try:
    data = json.load(sys.stdin)
except:
    raise BaseException("Input is not valid json.")

# If the json is not a list of 2, raises exception
if type(data) != list and len(data) != 2:
    raise BaseException("Input is not of type list.")

my_board = Board(data[0])
print(my_board.board_array)

method = data[1][0]
args = data[1][1:]
print(method)
print(args)

if method == "occupied?":
    ret_data = my_board.is_occupied(args[0])
elif method == "occupies?":
    ret_data = my_board.does_occupy(args[0], args[1])
elif method == "reachable?":
    ret_data = my_board.is_reachable(args[0], args[1])
elif method == "place":
    ret_data = my_board.place(args[0], args[1])
elif method == "remove":
    ret_data = my_board.remove(args[0], args[1])
elif method == "get-points":
    ret_data = my_board.get_points(args[0])

sys.stdout.write(json.dumps(ret_data))
"""