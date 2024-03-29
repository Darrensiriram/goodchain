from blockchainActions.BlockChain import CBlock
import time
import pickle
from blockchainActions.TxBlock import *

alltrans = []
with open("../pool.dat","rb") as f:
    try:
        while True:
            alltrans.append(pickle.load(f))
    except EOFError:
       pass

i = 0
while i < len(alltrans):
    tx = alltrans[i]
    if i == 0:
        root = TxBlock(None)
        root.addTx(tx)
    print(tx)
    i += 1


print("Mining.... root")
root.mine(leading_zeros=2)

b1 = TxBlock(root)
b1.addTx(tx)

start = time.time()
print("Mining ")
if b1.mine(leading_zeros = 2):
        print("Success! Mining was successful!")
else:
    print("ERROR! Mining was not successful!")

elapsed = time.time() - start

print("elapsed time: " + str(elapsed) + " s.")
if elapsed < 30:
    print("Alarm! Mining is too fast")
elif elapsed > 60:
    print("Alarm! Mining is too Slow")
