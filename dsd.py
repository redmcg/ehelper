#!/usr/bin/env python

from sys import argv
from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot
from common import print_defaults, get_Is, get_nVt

def main(argv):
  if len(argv) < 2 or len(argv) > 4:
    print("Design Serial Diode")
    print("Usage: dsd <Vcc> <Id> [<Is>] [<nVt>]")
    print_defaults()
  else:
    Vcc = mpf(argv[0])
    Id = mpf(argv[1])
    Is = mpf(get_Is(argv, 2))
    nVt = mpf(get_nVt(argv, 2))
    Vd = fmul(log(fadd(fdiv(Id,Is),mpf(1))),nVt)
    VR = fsub(Vcc, Vd)
    IR = Id
    R = fdiv(VR,IR)
    print("VR: {}, IR: {}, R: {}".format(VR, IR, R))
    print("Vd: {}, Id: {}, Rd: {}".format(Vd, Id, fdiv(Vd,Id)))
    plot([lambda x: fsub(Vcc,fmul(x,R)), lambda x: fmul(nVt,log(fadd(fdiv(x,Is),1)))], [0, fdiv(Vcc,R)], [0, Vcc])

if __name__ == "__main__":
  main(argv[1:])
