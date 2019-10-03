import sys
from backend2 import sort

special_json_list = []

for i in range(10):

    special_json_list.append(sys.stdin.readline().rstrip())

sys.stdout.write(f'{sort(special_json_list)}')