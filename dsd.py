#!/usr/bin/env python

from sys import argv
from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot

def main(argv):
  if len(argv) != 4:
    print "Design Serial Diode"
    print "Usage: psd <Vcc> <Id> <Is> <nVt>"
  else:
    Vcc = mpf(argv[0])
    Id = mpf(argv[1])
    Is = mpf(argv[2])
    nVt = mpf(argv[3])
    Vd = fmul(log(fadd(fdiv(Id,Is),mpf(1))),nVt)
    VR = fsub(Vcc, Vd)
    IR = Id
    R = fdiv(VR,IR)
    print "VR: {}, IR: {}, R: {}".format(VR, IR, R)
    print "Vd: {}, Id: {}, Rd: {}".format(Vd, Id, fdiv(Vd,Id))
    plot([lambda x: fsub(Vcc,fmul(x,R)), lambda x: fmul(nVt,log(fadd(fdiv(x,Is),1)))], [0, fdiv(Vcc,R)], [0, Vcc])

if __name__ == "__main__":
  main(argv[1:])
