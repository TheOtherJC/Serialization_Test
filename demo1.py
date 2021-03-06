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



def osu_bcast(
    BENCHMARH = "MPI Gather Latency Test",
    skip = 1000,
    loop = 10000,
    skip_large = 10,
    loop_large = 100,
    large_message_size = 8192,
    MAX_MSG_SIZE = 1<<20,
    ):

    comm = MPI.COMM_WORLD
    myid = comm.Get_rank()
    numprocs = comm.Get_size()

    if numprocs < 2:
        if myid == 0:
            errmsg = "This test requires at least two processes"
        else:
            errmsg = None
        raise SystemExit(errmsg)

    if myid == 0:
        r_buf = allocate(MAX_MSG_SIZE*numprocs)
    else:
        s_buf = allocate(MAX_MSG_SIZE)

    if myid == 0:
        print ('# %s' % (BENCHMARH,))
    if myid == 0:
        print ('# %-8s%20s' % ("Size [B]", "Latency [us]"))

    for size in message_sizes(MAX_MSG_SIZE):
        if size > large_message_size:
            skip = skip_large
            loop = loop_large
        iterations = list(range(loop+skip))
        if myid == 0:
            s_msg = MPI.IN_PLACE
            r_msg = [r_buf, size, MPI.BYTE]
        else:
            s_msg = [s_buf, size, MPI.BYTE]
            r_msg = None
        #
        comm.Barrier()
        for i in iterations:
            if i == skip:
                t_start = MPI.Wtime()
            comm.Gather(s_msg, r_msg, 0)
        t_end = MPI.Wtime()
        comm.Barrier()
        #
        if myid == 0:
            latency = (t_end - t_start) * 1e6 / loop
            print ('%-10d%20.2f' % (size, latency))


def message_sizes(max_size):
    return [0] + [(1<<i) for i in range(30)
                  if (1<<i) <= max_size]

def allocate(n):
    try:
        import mmap
        return mmap.mmap(-1, n)
    except (ImportError, EnvironmentError):
        try:
            from numpy import zeros
            return zeros(n, 'B')
        except ImportError:
            from array import array
            return array('B', [0]) * n


if __name__ == '__main__':
    osu_bcast()
