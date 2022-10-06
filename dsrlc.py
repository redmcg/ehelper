#!/usr/bin/env python

from mpmath import sqrt, fmul, fdiv, pi, plot, power, fadd, log10, fsub
import argparse
import logging

def main():
  parser = argparse.ArgumentParser(description='Design a serial RLC circuit')
  parser.add_argument('f0', type=float, help='Value of resonant frequency (in Hertz)')
  parser.add_argument('bw', type=float, help='Value of the bandwidth (in Hertz)')
  parser.add_argument('component', choices=['R','L','C'], help='Which component value represents (R, L or C)')
  parser.add_argument('value', type=float, help='Value of specified component (in Ohms for R, Henries for L or Farads for C')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  f0 = args.f0
  bw = args.bw
  component = args.component
  value = args.value

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'f0: {f0}, bw: {bw}, component: {component}, value: {value}')

  w0 = fmul(2,fmul(pi,f0))
  dw = fmul(2,fmul(pi,bw))
  a = fdiv(dw,2)
  q = fdiv(w0,dw)
  d = fdiv(a,w0)

  match component:
    case "L":
      l = value
      c = fdiv(1,fmul(power(w0,2),l))
      r = fmul(a, fmul(2, l))
    case "C":
      c = value
      l = fdiv(1,fmul(power(w0,2),c))
      r = fmul(a, fmul(2, l))
    case "R":
      r = value
      l = fdiv(r,fmul(2,a))
      c = fdiv(1,fmul(power(w0,2),l))

  xl = lambda w: fmul(l,w)
  xc = lambda w: fdiv(1,fmul(c,w))
  z = lambda w: sqrt(fadd(power(fsub(xl(w),xc(w)),2),power(r,2)))

  w0pow10 = lambda n: fmul(w0,power(10,n))
  ratio2db = lambda r: fmul(20,log10(r))

  print("R: {}, L: {}, C: {}".format(r, l, c))
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
