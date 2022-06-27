from contextlib import contextmanager
from ctypes import sizeof
import time

with open("queries.txt") as req:
    strings = req.readlines()

for i in range (0, len(strings)):
    strings[i] = strings[i].replace("\n", '')


with open("position.txt") as position:
    i = int(position.read().strip())

with open("position.txt", "w") as position:
    while 1:
        print(strings[i % 100])
        i += 1
        position.write(str(i))
        time.sleep(1)
