#!/usr/bin/env python
# convert yawat files to files as if aligned with (m)giza++ and subsequent 
# symal symmetrization
# written by Ulrich Germann

import sys,os

usage = """
usage: %s <stem>

where <stem> is the base name of the .crp and .aln files of the respective document.

The program will produce the following files:
   <stem>.id: one segment ID per line
   <stem>.src: source text, one segment per line
   <stem>.trg: target text, one segment per line
   <stem>.symal: alignment in symal format 
"""%sys.argv[0]

if len(sys.argv) != 2:
    print usage
    sys.exit(1)

stem = sys.argv[1]
if stem[-1] == ".": stem = stem[:-1]
crpfile = stem+".crp"
alnfile = stem+".aln"

# sanity checks
if not os.path.exists(crpfile):
    print >>sys.stderr,"FATAL ERROR: file '%s' not found."%crpfile
    sys.exit(1)
    pass

if not os.path.exists(alnfile):
    print >>sys.stderr,"FATAL ERROR: file '%s' not found."%crpfile
    sys.exit(1)
    pass

id_out    = open(stem+".id",'w')
src_out   = open(stem+".src",'w')
trg_out   = open(stem+".trg",'w')
symal_out = open(stem+".symal",'w')

CRP = [x.strip() for x in open(crpfile).readlines() if len(x.strip())]
ALN = [x.strip() for x in open(alnfile).readlines() if len(x.strip())]

assert(len(CRP) == 3*len(ALN))

S = {}
T = {}
A = {}
for i in xrange(len(ALN)):
    tag = CRP[3*i]
    S[tag] = CRP[3*i+1]
    T[tag] = CRP[3*i+2]
    pass

for i in xrange(len(ALN)):
    a = ALN[i].strip().split()
    A[a[0]] = a[1:]
    pass

def cmptag(x,y):
    x = x.split("-")[-1]
    y = y.split("-")[-1]
    if x[0] == 'P':
        if y[0] =='P' and y[-1] == 'A':
            return 1
        return -1
    if y[0] == 'P':
        return 1
    if x[-2:] == "10":
        return 1
    if y[-2:] == "10":
        return -1
    if x[-1] < y[-1]:
        return -1
    return  1

def convert(a):
    R = []
    for chunk in a:
        X,Y = chunk.split(":")[:2]
        for x in X.split(","):
            if len(x) == 0: continue
            for y in Y.split(","):
                if len(y) == 0: continue
                try:
                    R.append((int(x),int(y)))
                except:
                    print a
                    print chunk
                    print x,y
                    sys.exit(1)
                pass
            pass
        pass
    R.sort()
    return R

k = A.keys()
k.sort(lambda x,y: cmptag(x,y))
print k
for a in k:
    print >>id_out,a
    print >>src_out,S[a]
    print >>trg_out,T[a]
    print >>symal_out," ".join(["%d-%d"%(y,z) for y,z in convert([x for x in A[a]])])
    pass
