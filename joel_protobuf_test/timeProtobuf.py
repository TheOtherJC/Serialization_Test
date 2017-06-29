#! /usr/bin/env python

import cPickle
import timeit
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

with open('realstuff.pkl', 'r') as f:
    realStuff = cPickle.load(f)

setupStatement="""\
from __main__ import writePB, readPB, realStuff
"""

print 'write: %s' % timeit.timeit("writePB()", setup=setupStatement, number=1)
print 'read:  %s' % timeit.timeit("readPB()", setup=setupStatement, number=1)





