#!/usr/bin/env python

from mpmath import mpc, fmul, fdiv, fsub, fadd, exp, power, log, sqrt, pi, plot
import argparse
import logging

def main():
  parser = argparse.ArgumentParser(description='Analyse serial RC circuit')
  parser.add_argument('R', type=float, help='Resistor value (in Ohms)')
  parser.add_argument('C', type=float, help='Capacitor value (in Farads)')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph (in time domain by default)')
  parser.add_argument('-f', '--frequency', action='store_true', help='Use frequency domain (logarithmic scale) instead of time for graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  R = args.R
  C = args.C

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'R: {R}, C: {C}')

  twopi = fmul(2,pi)
  tc = fmul(R,C)
  nepers = fdiv(1,tc)
  cutoff = fmul(nepers,fdiv(1,twopi))

  print("tc: {}, nepers: {}, cutoff: {}".format(tc, nepers, cutoff))

  def H(x):
    if x > 0:
      return 1
    return 0

  def pow10(x):
    return fmul(power(10,x),twopi)

  def mag(x):
    return sqrt(fadd(power(x.real,2),power(x.imag,2)))

  def db(x):
    return fmul(20,log(x,10))

  if args.graph:
    if args.frequency:
      plot(lambda f: db(mag(fdiv(1,fadd(1,fmul(mpc(0, pow10(f)),tc))))), [0,12])
    else:
      plot([lambda t: fsub(H(t),fmul(exp(fdiv(-t,tc)),H(t))), lambda t: fmul(exp(fdiv(-t,tc)),H(t))], [-tc, fmul(6,tc)], [0, 1])

if __name__ == "__main__":
  main()
