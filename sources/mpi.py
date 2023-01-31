from mpi4py import MPI
import numpy

n=3
b=4
p=2
final=0
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
if rank == 0:
    jeton = 0
    comm.send(jeton, dest=1)
    final=comm.recv(source=n*b*p)
    print("jeton=",final)

for i in range(n*b*p-1):

    if rank == i:
        jeton = comm.recv(source=i)
        comm.send(jeton, dest=i+1)

if rank==n*b*p:
    jeton=comm.recv(source=n*b*p-1)
    comm.send(jeton,dest=0)

