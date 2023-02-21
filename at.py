#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot, pi, tan, cos, power, sqrt, acos, sin
import argparse
import logging

def r2d(rads):
  return fdiv(fmul(rads,180),pi)

def main():
  parser = argparse.ArgumentParser(description='Analyse Transformer')
  parser.add_argument('Vsrc', type=float, help='Measured Voltage from the source (RMS by default)')
  parser.add_argument('Vf', type=float, help='Voltage frequency')
  parser.add_argument('Vs', type=float, help='Measured voltage over the source resistor (RMS by default)')
  parser.add_argument('Vin', type=float, help='Measured voltage over the primary (RMS by default)')
  parser.add_argument('Vout', type=float, help='Measured Voltage over the secondary (RMS by default)')
  parser.add_argument('Rs', type=float, help='Resistance of the source resistor')
  parser.add_argument('Rrin', type=float, help='Resistance of the primary inductor')
  parser.add_argument('Rrout', type=float, help='Resistance of the secondary inductor')
  parser.add_argument('Rload', type=float, help='Resistance of the load')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  parser.add_argument('-m', '--max', action='store_true', help='Use maximum voltage for all measured voltages instead of RMS')
  args = parser.parse_args()

  Vf = args.Vf
  Vsrc = args.Vsrc
  Vs = args.Vs
  Vin = args.Vin
  Vout = args.Vout
  Rs = args.Rs
  Rrin = args.Rrin
  Rrout = args.Rrout
  Rload = args.Rload

  if args.max:
    Vsrc = fdiv(Vsrc,sqrt(2)) 
    Vs = fdiv(Vs,sqrt(2)) 
    Vin = fdiv(Vin,sqrt(2)) 
    Vout = fdiv(Vout,sqrt(2)) 

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vsrc: {Vsrc}, Vf: {Vf}, Vs: {Vs}, Vin: {Vin}, Vout: {Vout}, Rs: {Rs}, Rrin: {Rrin}, Rrout: {Rrout}, Rload: {Rload}')

  Vload = Vout
  Ilout = Irout = Iout = Iload = fdiv(Vload,Rload)

  Irin = Ilin = Iin = Is = Isrc = Itot = fdiv(Vs,Rs)
  Ztot = fdiv(Vsrc,Isrc)
  Vtot = fmul(Itot,Ztot)
  Zin = fdiv(Vin,Iin)

  Pin = acos(fdiv(fsub(fsub(power(Ztot,2),power(Rs,2)),power(Zin,2)),fmul(2,fmul(Rs,Zin))))
  Rin = fmul(Zin,cos(Pin))
  Rtot = Rs + Rin
  Ptot = acos(fdiv(Rtot,Ztot))
  Xin = Xlin = Xtot = fmul(Zin,sin(Pin))

  Rlin = fsub(Rin,Rrin)
  Zlin = sqrt(fadd(power(Rlin,2),power(Xlin,2)))
  Plin = acos(fdiv(Rlin,Zlin))

  Vlin = fmul(Ilin,Zlin)
  Vrin = fmul(Irin,Rrin)

  va = fmul(fmul(Vlin,Ilin),cos(Plin))

  Xout = fdiv(fadd(Rload,Rrout),tan(Plin))
  Lout = fdiv(Xout,fmul(2,fmul(pi,Vf)))
  Vrout = fmul(Irout,Rrout)
  Vlout = fadd(Vrout,Vload)
  TR = fdiv(Vlin,Vlout)
  Lin = fmul(power(TR,2),Lout)

  watts = fmul(Vlout,Ilout)

  print("Iin: {}, Iout: {}".format(Iin, Iout))
  print("Ptot: {}°, Ztot: {}, Rtot: {}, Xtot: {}".format(r2d(Ptot), Ztot, Rtot, Xtot))
  print("Pin: {}°, Zin: {}, Rin: {}, Xin: {}".format(r2d(Pin), Zin, Rin, Xin))
  print("Plin: {}°, Zlin: {}, Rlin: {}, Xlin: {}".format(r2d(Plin), Zlin, Rlin, Xlin))
  print("Vtot: {}, Vs: {}, Vin: {}, Vrin: {}, Vlin: {}, Vout: {}, Vlout: {}, Vload: {}".format(Vtot, Vs, Vin, Vrin, Vlin, Vout, Vlout, Vload))
  print("Xout: {}, Lout: {}, Lin: {}, TR: {}".format(Xout, Lout, Lin, TR))
  print("va: {}, watts: {}".format(va, watts))

if __name__ == "__main__":
  main()
