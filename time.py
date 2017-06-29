import time
from mpi4py import MPI
import pickle
import timeit
import msgpack
import sys
from test_pb2 import BunchOfTestDicts, TestDict, Pair

def writePB():
    bOTD = BunchOfTestDicts()
    for thisDict in realStuff:
        tD = bOTD.dicts.add()
        for k, v in thisDict.items():
            pair = tD.pairs.add()
            pair.key = k
            pair.value = v

    with open('realstuff.pb', 'wb') as f:
        f.write(bOTD.SerializeToString())

def readPB():
    bOTD = BunchOfTestDicts()
    with open('realstuff.pb', 'rb') as f:
        bOTD.ParseFromString(f.read())
    thisDictList = [{thisPair.key: thisPair.value
                             for thisPair in thisBufferedDict.pairs}
                    for thisBufferedDict in bOTD.dicts]
    return thisDictList

def writeReadPB():
    bOTD = BunchOfTestDicts()
    for thisDict in realStuff:
        tD = bOTD.dicts.add()
        for k, v in thisDict.items():
            pair = tD.pairs.add()
            pair.key = k
            pair.value = v
    #serializedPB = bOTD.SerializeToString()
    #print 'serialized PB length: %s'%len(serializedPB)
    #newBOTD = BunchOfTestDicts()
    #newBOTD.ParseFromString(serializedPB)
    newBOTD = bOTD
    thisDictList = [{thisPair.key: thisPair.value
                             for thisPair in thisBufferedDict.pairs}
                    for thisBufferedDict in newBOTD.dicts]
    return thisDictList


with open('realstuff.pkl', 'rb') as f:
    realStuff = pickle.load(f)

setupStatement="""\
from __main__ import writePB, readPB, writeReadPB, realStuff
"""

#print ('write: %s' % timeit.timeit("writePB()", setup=setupStatement, number=1))
#print ('read:  %s' % timeit.timeit("readPB()", setup=setupStatement, number=1))
print ('writeRead:  %s' % timeit.timeit("writeReadPB()", setup=setupStatement, number=10))
