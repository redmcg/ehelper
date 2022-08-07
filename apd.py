#!/usr/bin/env python

from sys import argv
from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot
from common import print_defaults, get_Is, get_nVt

def main(argv):
  if len(argv) < 3 or len(argv) > 5:
    print("Analyse Parallel Diode")
    print("Usage: apd <Vcc> <R1> <R2> [<Is>] [<nVt>]")
    print_defaults()
  else:
    Vcc = mpf(argv[0])
    R1 = mpf(argv[1])
    R2 = mpf(argv[2])
    Is = mpf(get_Is(argv, 3))
    nVt = mpf(get_nVt(argv, 4))
    x = fdiv(fmul(fmul(fmul(R1,R2),Is),exp(fdiv(fmul(R2,fadd(Vcc,fmul(Is,R1))),(fmul(nVt,fadd(R1,R2)))))),fmul(nVt,fadd(R1,R2)))
    w = lambertw(x)
    Id = fsub(fdiv(fmul(fmul(nVt,w),fadd(R1,R2)),fmul(R1,R2)),Is)
    Vd = fmul(log(fadd(fdiv(Id,Is),mpf(1))),nVt)
    Rd = fdiv(Vd,Id)
    Rd2 = fdiv(fmul(Rd,R2),fadd(Rd,R2))
    VR2 = Vd
    IR2 = fdiv(VR2,R2)
    VR1 = fsub(Vcc,Vd)
    IR1 = fdiv(VR1,R1)
    print("VR1: {}, IR1: {}".format(VR1, IR1))
    print("VR2: {}, IR2: {}".format(VR2, IR2))
    print("Vd: {}, Id: {}".format(Vd, Id))
    plot([lambda x: fsub(Vcc,fmul(fadd(x,fdiv(fmul(nVt,log(fadd(fdiv(x,Is),mpf(1)))),R2)),R1)), lambda x: fmul(nVt,log(fadd(fdiv(x,Is),mpf(1))))], [0, fdiv(Vcc,fadd(R1,Rd2))], [0, Vcc])

if __name__ == "__main__":
  main(argv[1:])
