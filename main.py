from operator import pos
import time

req = open("queries.txt", "r")
strings = req.readlines()

position = open("position.txt", "r")
i = int(position.read().strip())
position.close()
position = open("position.txt", "w")

while 1:
    print(strings[i%100])
    i += 1
    position.write(str(i))
    time.sleep(1)

req.close()
position.close()