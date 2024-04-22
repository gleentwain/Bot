import random

Guesslst = {} 

name = "?"
for i in range(1, 4):
        Guesslst[i] = name
        name += "?"

message = "?"

if message in Guesslst.values():
        ans = random.randint(1,3)
        if Guesslst[ans] == message:
            print("H")
        else:
            print("J")