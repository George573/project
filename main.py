import time

req = open("queries.txt", "r")
strings = req.readlines()

i = 0
while 1:
    print(strings[i%100])
    i += 1
    time.sleep(1)
    

req.close()