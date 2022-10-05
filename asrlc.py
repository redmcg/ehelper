#!/usr/bin/env python

from mpmath import sqrt, fmul, fdiv, pi, plot, power, fadd, log10, fsub
import argparse
import logging

def main():
  parser = argparse.ArgumentParser(description='Analyse a serial RLC circuit')
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

  xl = lambda w: fmul(l,w)
  xc = lambda w: fdiv(1,fmul(c,w))
  z = lambda w: sqrt(fadd(power(fsub(xl(w),xc(w)),2),power(r,2)))

  w0 = fdiv(1,sqrt(fmul(l,c)))
  f0 = fdiv(w0,fmul(2,pi))
  x0 = xc(w0)
  q = fdiv(x0,r)
  dw = fdiv(w0,q)
  a = fdiv(dw,2)
  bw = fdiv(dw,fmul(2,pi))
  d = fdiv(a,w0)


  w0pow10 = lambda n: fmul(w0,power(10,n))
  ratio2db = lambda r: fmul(20,log10(r))

  print("ω₀: {}, f₀: {} Hz".format(w0, f0))
  print("Δω: {}, Δf: {} Hz".format(dw, bw))
  print("Q: {}, ζ: {}".format(q, d))

  z0 = z(w0)
  lwco = fsub(w0,a)
  lzco = z(lwco)
  ldbco = ratio2db(fdiv(r,lzco))
  uwco = fadd(w0,a)
  uzco = z(uwco)
  udbco = ratio2db(fdiv(r,uzco))
  bwpower = power(10,fdiv(fadd(ldbco,udbco),20))
  logging.info(f'z0: {z0}')
  logging.info(f'lwco: {lwco}, lzco: {lzco}, ldbco: {ldbco}')
  logging.info(f'uwco: {uwco}, uzco: {uzco}, udbco: {udbco}')
  logging.info(f'bwpower: {bwpower}')

  if args.graph:
    plot([lambda x: ratio2db(fdiv(r,z(w0pow10(x))))], [-1,1], [ratio2db(fdiv(r,z(w0pow10(-1)))),1])

if __name__ == "__main__":
  main()
