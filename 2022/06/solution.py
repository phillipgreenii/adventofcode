
import re

from collections import deque

def find_first_unique_set_of_size(size, signal):
    for i in range(size-1, len(signal)):
        window = signal[(i-size):i]
        # print(window)
        uniq_symbols = set(window)
        # print(uniq_symbols)
        if len(uniq_symbols) == size:
            return i
    return None

def find_signal_start(signal):
    return find_first_unique_set_of_size(4, signal)

def find_message_start(signal):
    return find_first_unique_set_of_size(14, signal)

print("part 1")
#1582
with open("input1.txt", 'r') as file_in:
    for line in file_in:
        line = line.rstrip()
        if len(line) == 0:
            continue

        start = find_signal_start(line)
        print(start)
        
print("part 2")
#3588
with open("input2.txt", 'r') as file_in:
    for line in file_in:
        line = line.rstrip()
        if len(line) == 0:
            continue

        start = find_message_start(line)
        print(start)