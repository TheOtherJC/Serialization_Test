# Synopsis


**Pickle**
   * Pickle serialises the object first before writing it to a file, which seems to very useful for what we're trying to do.
   
**Protobuf**
   * Protobuf doesn't deal with schema evolution which would cause most to assume it would be more efficient, yet is the least efficient out of the three choices.
    
**MsgPack**
   * Msgpack can distinguish string and binary type, yet it doesn't work well with Python 2 which could be a hindrance. However it does produce the shortest string length and is the quickest out the three.

# Installation
**Pickle:**

`import pickle`

**Protobuf:**

`$ sudo pip3 install protobuf`

`syntax = "proto2"`

**MsgPack:**

`$ sudo pip install msgpack-python`

`import msgpack`
# Results

**Pickle:**

```bash
def writeReadPkl():
    serializedPkl = pickle.dumps(realStuff, protocol=2)
    print ('pickle string length: %s'%len(serializedPkl))
    rslt = pickle.loads(serializedPkl)
    return rslt

setupStatement="""\
from __main__ import writeReadPkl, realStuff
"""

print ('writeRead:  %s' % timeit.timeit("writeReadPkl()", setup=setupStatement, number=10))
```
output:

* pickle string length: 26798577
* writeRead:  4.851042742000573

**Protobuf:**

`$ sudo pip install msgpack-python`

**MsgPack:**

```bash
def writeReadMSG():
    serializedMSG = msgpack.dumps(realStuff)
    print ('MsgPack length: %s'%len(serializedMSG))
    rslt = msgpack.loads(serializedMSG)
    return rslt

setupStatement="""\
from __main__ import writeReadMSG
"""

print ('writeRead:  %s' % timeit.timeit("writeReadMSG()", setup=setupStatement, number=10))
```

* MsgPack string length: 16099141
* writeRead:  3.323402583000643
