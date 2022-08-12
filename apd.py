#!/usr/bin/env python

from sys import argv
from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot
import argparse
import logging

def main(argv):
  parser = argparse.ArgumentParser(description='Analyse Parallel Diode')
  parser.add_argument('Vs', type=float, help='Voltage supply')
  parser.add_argument('R1', type=float, help='Resistor 1 value in Ohms')
  parser.add_argument('R2', type=float, help='Resistor 2 value in Ohms')
  parser.add_argument('Is', type=float, nargs='?', default=1e-12, help='Diode Saturation current in Amps (default = 1e-12)')
  parser.add_argument('N', type=float, nargs='?', default=1, help='Emission Coefficient (default = 1)')
  parser.add_argument('--Vt', type=float, default=0.026, help='Thermal Voltage in Volts (default = 0.026)')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  Vs = args.Vs
  R1 = args.R1
  R2 = args.R2
  Is = args.Is
  N = args.N
  Vt = args.Vt
  nVt = N*Vt

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vs: {Vs}, R1: {R1}, R2: {R2}, Is: {Is}, N: {N}, Vt: {Vt}')

  x = fdiv(fmul(fmul(fmul(R1,R2),Is),exp(fdiv(fmul(R2,fadd(Vs,fmul(Is,R1))),(fmul(nVt,fadd(R1,R2)))))),fmul(nVt,fadd(R1,R2)))
  w = lambertw(x)
  Id = fsub(fdiv(fmul(fmul(nVt,w),fadd(R1,R2)),fmul(R1,R2)),Is)
  Vd = fmul(log(fadd(fdiv(Id,Is),mpf(1))),nVt)
  Rd = fdiv(Vd,Id)
  Rd2 = fdiv(fmul(Rd,R2),fadd(Rd,R2))
  VR2 = Vd
  IR2 = fdiv(VR2,R2)
  VR1 = fsub(Vs,Vd)
  IR1 = fdiv(VR1,R1)
  print("VR1: {}, IR1: {}".format(VR1, IR1))
  print("VR2: {}, IR2: {}".format(VR2, IR2))
  print("Vd: {}, Id: {}".format(Vd, Id))
  if args.graph:
    plot([lambda x: fsub(Vs,fmul(fadd(x,fdiv(fmul(nVt,log(fadd(fdiv(x,Is),mpf(1)))),R2)),R1)), lambda x: fmul(nVt,log(fadd(fdiv(x,Is),mpf(1))))], [0, fdiv(Vs,fadd(R1,Rd2))], [0, Vs])

if __name__ == "__main__":
  main(argv[1:])
