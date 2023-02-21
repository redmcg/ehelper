#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot, pi, tan, cos, power, sqrt, acos, sin
import argparse
import logging

def r2d(rads):
  return fdiv(fmul(rads,180),pi)

def main():
  parser = argparse.ArgumentParser(description='Analyse Phase of RL circuit')
  parser.add_argument('Vsrc', type=float, help='Measured Voltage from the source (RMS by default)')
  parser.add_argument('Vr', type=float, help='Measured voltage over the source resistor (RMS by default)')
  parser.add_argument('Vl', type=float, help='Measured voltage over the inductor (RMS by default)')
  parser.add_argument('Rr', type=float, help='Resistance of the resistor')
  parser.add_argument('Rlr', type=float, help='Resistance of the inductor')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  parser.add_argument('-m', '--max', action='store_true', help='Use maximum voltage for all measured voltages instead of RMS')
  args = parser.parse_args()

  Vsrc = args.Vsrc
  Vr = args.Vr
  Vl = args.Vl
  Rr = args.Rr
  Rlr = args.Rlr

  if args.max:
    Vsrc = fdiv(Vsrc,sqrt(2)) 
    Vr = fdiv(Vr,sqrt(2)) 
    Vl = fdiv(Vl,sqrt(2)) 

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vsrc: {Vsrc}, Vr: {Vr}, Vl: {Vl}, Rr: {Rr}, Rlr: {Rlr}')

  Itot = Ill = Il = Ilr = Ir = Isrc = fdiv(Vr,Rr)
  Ztot = fdiv(Vsrc,Isrc)
  Vtot = fmul(Itot, Ztot)
  Zl = fdiv(Vl,Il)

  Pl = acos(fdiv(fsub(fsub(power(Ztot,2),power(Rr,2)),power(Zl,2)),fmul(2,fmul(Rr,Zl))))
  Rl = fmul(Zl,cos(Pl))
  Rtot = Rl + Rr
  Xll = Xl = Xtot = fmul(Zl,sin(Pl))
  Ptot = acos(fdiv(Rtot,Ztot))

  Rll = Rl - Rlr
  Zll = sqrt(fadd(power(Rll,2),power(Xll,2)))
  Vll = fmul(Ill, Zll)
  Pll = acos(fdiv(Rll,Zll))
  Vll = fmul(Ill,Zll)

  Vlr = fmul(Ilr,Rlr)

  print("Isrc: {}".format(Isrc))
  print("Ptot: {}°, Ztot: {}, Rtot: {}, Xtot: {}".format(r2d(Ptot), Ztot, Rtot, Xtot))
  print("Pl: {}°, Zl: {}, Rl: {}, Xl: {}".format(r2d(Pl), Zl, Rl, Xl))
  print("Pll: {}°, Zll: {}, Rll: {}, Xll: {}".format(r2d(Pll), Zll, Rll, Xll))
  print("Vtot: {}, Vr: {}, Vl: {}, Vlr: {}, Vll: {}".format(Vtot, Vr, Vl, Vlr, Vll))

if __name__ == "__main__":
  main()
