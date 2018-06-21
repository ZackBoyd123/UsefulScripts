#!/bin/python3 
import sys

file= sys.argv[1]
with open(file, "r") as f1:
    head = f1.readline()
    seq = f1.readlines()
    f1.close()
pad = ""
for i in range(0,int(sys.argv[2])):
    i = "N"
    pad += i
newseq = []
for i in seq:
    if i.startswith(">"):
        i = pad
    newseq.append(i)

newseq = [i.replace("\n","") for i in newseq]
newseq = "".join(newseq)
sys.stdout = open(file.split(".")[0]+"_padded.fasta","w")
print(head+newseq)

