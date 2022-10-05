#!/usr/bin/env python

from mpmath import sqrt, fmul, fdiv, pi, plot, power, fadd, log10, fsub, fabs
import argparse
import logging

def main():
  parser = argparse.ArgumentParser(description='Analyse a parallel RLC circuit')
  parser.add_argument('R', type=float, help='Value of resistance in Ohms (Ωs)')
  parser.add_argument('L', type=float, help='Value of inductance in Henries')
  parser.add_argument('C', type=float, help='Value of capacitance in Farads')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  r = args.R
  l = args.L
  c = args.C

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'R: {r}, L: {l}, C: {c}')

  w0 = fdiv(1,sqrt(fmul(l,c)))
  f0 = fdiv(w0,fmul(2,pi))
  a = fdiv(1,fmul(2,fmul(r,c)))
  d = fdiv(a,w0)
  q = fmul(r,sqrt(fdiv(c,l)))
  dw = fmul(2,a)
  df = fdiv(dw,fmul(2,pi))

  xl = lambda w: fmul(l,w)
  xc = lambda w: fdiv(1,fmul(c,w))
  z = lambda w: fdiv(1,fadd(fabs(fsub(fdiv(1,xl(w)),fdiv(1,xc(w)))),fdiv(1,r)))
  z0 = z(w0)

  w0pow10 = lambda n: fmul(w0,power(10,n))
  ratio2db = lambda r: fmul(20,log10(r))

  print("ω₀: {}, f₀: {} Hz".format(w0, f0))
  print("Δω: {}, Δf: {} Hz".format(dw, df))
  print("Q: {}, ζ: {}".format(q, d))

  logging.info(f'z0: {z0}')

  if args.graph:
    plot([lambda x: ratio2db(fdiv(z(w0pow10(x)),r))], [-1,1], [ratio2db(fdiv(z(w0pow10(-1)),r)),1])

if __name__ == "__main__":
  main()
