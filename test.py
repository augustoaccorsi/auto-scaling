
# generate random integer values
from random import seed
from random import randint
# seed random number generator

minutes = randint(1, 20)
sleep = (randint(1, 20) * 60)
print("calls: "+str(minutes))
print("sleep: "+str(sleep))