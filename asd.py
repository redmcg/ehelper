#!/usr/bin/env python

from sys import argv
from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot

def main(argv):
  if len(argv) != 4:
    print "Analyse Serial Diode"
    print "Usage: asd <Vcc> <R> <Is> <nVt>"
  else:
    Vcc = mpf(argv[0])
    R = mpf(argv[1])
    Is = mpf(argv[2])
    nVt = mpf(argv[3])
    x = fdiv(fmul(fmul(Is,R),fsub(exp(fdiv(Vcc,nVt)),mpf(1))),nVt)
    w = lambertw(x)
    Id = fdiv(fmul(w,nVt),R)
    Vd = fmul(log(fadd(fdiv(Id,Is),mpf(1))),nVt)
    VR = fsub(Vcc, Vd)
    IR = fdiv(VR, R)
    print "VR: {}, IR: {}".format(VR, IR)
    print "Vd: {}, Id: {}".format(Vd, Id)
    plot([lambda x: fsub(Vcc,fmul(x,R)), lambda x: fmul(nVt,log(fadd(fdiv(x,Is),1)))], [0, fdiv(Vcc,R)], [0, Vcc])

if __name__ == "__main__":
  main(argv[1:])
