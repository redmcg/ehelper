#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot, pi, tan, cos, power, sqrt, acos, sin, asin
import argparse
import logging

def d2r(rads):
  return fdiv(fmul(rads,pi),180)

def r2d(rads):
  return fdiv(fmul(rads,180),pi)

def main():
  parser = argparse.ArgumentParser(description='Design RL circuit')
  parser.add_argument('Vsrc', type=float, help='Voltage from the source (RMS by default)')
  parser.add_argument('Vf', type=float, help='Voltage frequency')
  parser.add_argument('Rl', type=float, help='Resistance of the inductor')
  parser.add_argument('Ll', type=float, help='Inductance of the inductor (in henries)')
  parser.add_argument('VP', choices=['V','P','R'], help='V, P or R; V if the desired value is to be voltage, P if the desired value is to be phase, R if the desired output is a ratio of the resistors value')
  parser.add_argument('value', type=float, help='Desired voltage, phase or ratio of the inductor (RMS for voltage by default, degrees for phase, a decimal fraction for ratio, such as 1 to match, 2 to double or .5 for half the resistor value)')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  parser.add_argument('-m', '--max', action='store_true', help='Use maximum voltage for all voltages instead of RMS')
  args = parser.parse_args()

  Vsrc = args.Vsrc
  Vf = args.Vf
  Rl = args.Rl
  Ll = args.Ll
  VP = args.VP
  value = args.value

  if args.max:
    Vsrc = fdiv(Vsrc,sqrt(2)) 
    if args.VP == 'V':
      value = fdiv(value,sqrt(2)) 

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vsrc: {Vsrc}, Vf: {Vf}, Rl: {Rl}, Ll: {Ll}, VP: {VP}, value: {value}')

  Xl = Xtot = fmul(fmul(fmul(2,pi),Vf),Ll)
  Zl = sqrt(fadd(power(Rl,2),power(Xl,2)))
  Pl = acos(fdiv(Rl,Xl))

  Vtot = Vsrc

  if VP == 'V':
    Vl = value
    Il = Ir = Itot = fdiv(Vl,Zl)
    Ztot = fdiv(Vtot,Itot)
  elif VP == 'P':
    Ptot = d2r(value)
    Ztot = fdiv(Xtot,sin(Ptot))
  elif VP == 'R':
    Rr = fdiv(Zl, value)
    Rtot = fadd(Rr, Rl)
    Ztot = sqrt(fadd(power(Rtot,2),power(Xtot,2)))

  if VP == 'P' or VP == 'R':
    Il = Ir = Itot = fdiv(Vtot,Ztot)
    Vl = fmul(Il, Zl)

  if VP == 'V' or VP == 'P':
    Rtot = sqrt(fsub(power(Ztot,2),power(Xtot,2)))
    Rr = fsub(Rtot,Rl)

  if VP == 'V' or VP == 'R':
    Ptot = asin(fdiv(Xtot,Ztot))

  Vr = fmul(Ir, Rr)
 
  print("Ptot: {}, Ztot: {}, Rtot: {}, Xtot: {}".format(r2d(Ptot), Ztot, Rtot, Xtot))
  print("Pl: {}, Zl: {}, Rl: {}, Xtot: {}".format(r2d(Pl), Zl, Rl, Xl))
  print("Rr: {}".format(Rr))
  print("Vr: {}, Vl: {}".format(Vr, Vl))

if __name__ == "__main__":
  main()
