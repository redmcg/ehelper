#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot, pi, tan, cos, power, sqrt, acos
import argparse
import logging

def main():
  parser = argparse.ArgumentParser(description='Analyse Transformer')
  parser.add_argument('Vs', type=float, help='Voltage supply (RMS by default)')
  parser.add_argument('Vf', type=float, help='Voltage frequency')
  parser.add_argument('Vrin', type=float, help='Measured voltage over the input resistor (RMS by default)')
  parser.add_argument('Vin', type=float, help='Measured voltage over the primary (RMS by default)')
  parser.add_argument('Vout', type=float, help='Measured Voltage over the secondary (RMS by default)')
  parser.add_argument('Rin', type=float, help='Resistance in series with primary')
  parser.add_argument('Rout', type=float, help='Resistance over the output')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  parser.add_argument('-m', '--max', action='store_true', help='Use maximum voltage for all measured voltages instead of RMS')
  args = parser.parse_args()

  Vs = args.Vs
  Vf = args.Vf
  Vrin = args.Vrin
  Vin = args.Vin
  Vout = args.Vout
  Rin = args.Rin
  Rout = args.Rout

  if args.max:
    Vs = fdiv(Vs,sqrt(2)) 
    Vrin = fdiv(Vrin,sqrt(2)) 
    Vin = fdiv(Vin,sqrt(2)) 
    Vout = fdiv(Vout,sqrt(2)) 

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vs: {Vs}, Vf: {Vf}, Vrin: {Vrin}, Vin: {Vin}, Vout: {Vout}, Rin: {Rin}, Rout: {Rout}')

  Iout = fdiv(Vout,Rout)
  P = fmul(Vout,Iout)
  phase = fmul(2,acos(fdiv(Vs,fadd(Vrin,Vin))))
  Iin = fdiv(P,fmul(Vin,cos(phase)))
  Zin = fdiv(Vin,Iin)
  Xout = Rout/tan(phase)
  Lout = fdiv(Xout,fmul(2,fmul(pi,Vf)))
  TR = fdiv(Vin,Vout)
  Lin = fmul(power(TR,2),Lout)

  print("P: {}, Iin: {}, Iout: {}".format(P, Iin, Iout))
  print("Lin: {}, Lout: {}, TR: {}".format(Lin, Lout, TR))
  print("Zin: {}, phase: {}°".format(Zin, fdiv(fmul(phase,180),pi)))
  print("Xout: {}".format(Xout))

if __name__ == "__main__":
  main()
