#!/usr/bin/env python

from sys import argv
from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot
import argparse
import logging

def main(argv):
  parser = argparse.ArgumentParser(description='Design Parallel Diode')
  parser.add_argument('Vs', type=float, help='Voltage supply')
  parser.add_argument('Id', type=float, help='Desired current over the diode in Amps')
  parser.add_argument('IR2', type=float, help='Desired current over Resistor two in Amps')
  parser.add_argument('Is', type=float, nargs='?', default=1e-12, help='Diode Saturation current in Amps (default = 1e-12)')
  parser.add_argument('N', type=float, nargs='?', default=1, help='Emission Coefficient (default = 1)')
  parser.add_argument('--Vt', type=float, default=0.026, help='Thermal Voltage in Volts (default = 0.026)')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  Vs = args.Vs
  Id = args.Id
  IR2 = args.IR2
  Is = args.Is
  N = args.N
  Vt = args.Vt
  nVt = N*Vt

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vs: {Vs}, Id: {Id}, IR2: {IR2}, Is: {Is}, N: {N}, Vt: {Vt}')

  Vd = fmul(log(fadd(fdiv(Id,Is),mpf(1))),nVt)
  Rd = fdiv(Vd,Id)
  VR2 = Vd
  R2 = fdiv(VR2,IR2)
  Rd2 = fdiv(fmul(Rd,R2),fadd(Rd,R2))
  VR1 = fsub(Vs,Vd)
  IR1 = fadd(Id,IR2)
  R1 = fdiv(VR1,IR1)
  print("VR1: {}, IR1: {}, R1: {}".format(VR1, IR1, R1))
  print("VR2: {}, IR2: {}, R2: {}".format(VR2, IR2, R2))
  print("Vd: {}, Id: {}, Rd: {}".format(Vd, Id, Rd))
  if args.graph:
    plot([lambda x: fsub(Vs,fmul(fadd(x,fdiv(fmul(nVt,log(fadd(fdiv(x,Is),mpf(1)))),R2)),R1)), lambda x: fmul(nVt,log(fadd(fdiv(x,Is),mpf(1))))], [0, fdiv(Vs,fadd(R1,Rd2))], [0, Vs])

if __name__ == "__main__":
  main(argv[1:])
