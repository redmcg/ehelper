#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot, pi, atan, cos, power, sqrt, sin
import argparse
import logging

def main():
  parser = argparse.ArgumentParser(description='Design Transformer')
  parser.add_argument('Vs', type=float, help='Voltage supply (RMS by default)')
  parser.add_argument('Vf', type=float, help='Voltage frequency')
  parser.add_argument('Vout', type=float, help='Desired output Voltage (RMS by default)')
  parser.add_argument('Rout', type=float, help='Resistance over the output')
  parser.add_argument('TR', type=float, help='Turns Ratio of the transformer (Primary/Secondary)')
  parser.add_argument('Lout', type=float, help='Secondary Inductance (in henries)')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  parser.add_argument('-m', '--max', action='store_true', help='Use maximum voltage for supply instead of RMS')
  parser.add_argument('-o', '--maxout', action='store_true', help='Use maximum voltage for desired output voltage instead of RMS')
  args = parser.parse_args()

  Vs = args.Vs
  Vf = args.Vf
  Vout = args.Vout
  Rout = args.Rout
  TR = args.TR
  Lout = args.Lout

  if args.max:
    Vs = fdiv(Vs,sqrt(2)) 

  if args.maxout:
    Vout = fdiv(Vout,sqrt(2)) 

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vs: {Vs}, Vf: {Vf}, Vout: {Vout}, Rout: {Rout}, TR: {TR}, Lout: {Lout}')

  Iout = fdiv(Vout,Rout)
  Vin = fmul(Vout,TR)
  P = fmul(Vout,Iout)
  Xout = fmul(2,fmul(pi,fmul(Vf,Lout)))
  phase = fsub(fdiv(pi,2),atan(fdiv(Xout,Rout)))
  Iin = fdiv(P,fmul(Vin,cos(phase)))
  Zin = fdiv(Vin,Iin)
  ZinR = fmul(Zin,cos(phase))
  ZinX = fmul(Zin,sin(phase))
  Zs = fdiv(Vs,Iin)
  ZsR = sqrt(fsub(power(Zs,2),power(ZinX,2)))
  Rin = fsub(ZsR,ZinR)
  Vrin = fmul(Rin,Iin)
  Lin = fmul(power(TR,2),Lout)
  print("P: {}, Iout: {}".format(P, Iout))
  print("Vrin: {}, Vin: {}, Iin: {}, Rin: {}, Lin: {}".format(Vrin, Vin, Iin, Rin, Lin))
  print("Zin: {}, phase: {}°".format(Zin, fdiv(fmul(phase,180),pi)))
  print("Xout: {}".format(Xout))

if __name__ == "__main__":
  main()
