#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot
import argparse
import logging

def main():
  parser = argparse.ArgumentParser(description='Design Serial Diode')
  parser.add_argument('Vs', type=float, help='Voltage supply')
  parser.add_argument('Id', type=float, help='Desired current over the diode in Amps')
  parser.add_argument('Is', type=float, nargs='?', default=1e-12, help='Diode Saturation current in Amps (default = 1e-12)')
  parser.add_argument('N', type=float, nargs='?', default=1, help='Emission Coefficient (default = 1)')
  parser.add_argument('--Vt', type=float, default=0.026, help='Thermal Voltage in Volts (default = 0.026)')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  Vs = args.Vs
  Id = args.Id
  Is = args.Is
  N = args.N
  Vt = args.Vt
  nVt = N*Vt

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vs: {Vs}, Id: {Id}, Is: {Is}, N: {N}, Vt: {Vt}')

  Vd = fmul(log(fadd(fdiv(Id,Is),mpf(1))),nVt)
  VR = fsub(Vs, Vd)
  IR = Id
  R = fdiv(VR,IR)
  print("VR: {}, IR: {}, R: {}".format(VR, IR, R))
  print("Vd: {}, Id: {}, Rd: {}".format(Vd, Id, fdiv(Vd,Id)))
  if args.graph:
    plot([lambda x: fsub(Vs,fmul(x,R)), lambda x: fmul(nVt,log(fadd(fdiv(x,Is),1)))], [0, fdiv(Vs,R)], [0, Vs])

if __name__ == "__main__":
  main()
