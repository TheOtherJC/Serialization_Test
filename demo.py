import numpy as np
from mpi4py import MPI
import pickle
import timeit
import msgpack
import sys
from test_pb2 import BunchOfTestDicts, TestDict, Pair

with open('realstuff.pkl', 'rb') as f:
    realStuff = pickle.load(f)

def writeReadMSG():
    serializedMSG = msgpack.dumps(realStuff)
    #print ('MsgPack length: %s'%len(serializedMSG))
    rslt = msgpack.loads(serializedMSG)
    return rslt

setupStatement="""\
from __main__ import writeReadMSG
"""

<<<<<<< HEAD

=======
>>>>>>> 58db5a0663869e214ff6fef968069772520f99f0
#print ('writeRead:  %s' % timeit.timeit("writeReadMSG()", setup=setupStatement, number=10))


comm = MPI.COMM_WORLD

name = MPI.Get_processor_name()
size = comm.Get_size()
rank = comm.Get_rank()

start = MPI.Wtime()

if rank == 0:
    data = writeReadMSG()
    comm.send(data, dest = 1)
    print ("From rank", rank, "we sent:", len(data))
    #print data
    #print
    #print
    #pickle.dump(data,open('dataon0.pkl','w'))
    
elif rank == 1:
    data = comm.recv(source = 0)
    print ("on node", rank, "we received:", len(data))
    #print data
    #print
    #print
    #pickle.dump(data,open('dataon1.pkl','w'))

end = MPI.Wtime()
print (end - start)
