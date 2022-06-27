from contextlib import contextmanager
from ctypes import sizeof
import time

with open("queries.txt") as req:
    strings = [line.rstrip() for line in req]

clean_strings = []
for i in range (0, len(strings)):
    if len(strings[i]) != 0:
        clean_strings.append(strings[i])

"""leng = len(strings)
for i in range (0, leng):
    if len(strings[i]) == 0:
        strings.pop(i)
        leng -= 1
        i -= 1"""

with open("position.txt") as position:
    i = int(position.read().strip())

while 1:
    print(clean_strings[i % 100])
    i += 1
    with open("position.txt", "w") as position:
        position.write(str(i))
    time.sleep(1)
