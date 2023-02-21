#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot, pi, atan, cos, power, sqrt, sin, acos
import argparse
import logging

def r2d(rads):
  return fdiv(fmul(rads,180),pi)

def main():
  parser = argparse.ArgumentParser(description='Design Transformer')
  parser.add_argument('Vsrc', type=float, help='Voltage supply (RMS by default)')
  parser.add_argument('Vf', type=float, help='Voltage frequency')
  parser.add_argument('Vout', type=float, help='Desired voltage over load (RMS by default)')
  parser.add_argument('Rrin', type=float, help='Resistance of primary inductor (in henries)')
  parser.add_argument('Rrout', type=float, help='Resistance of secondary inductor (in henries)')
  parser.add_argument('Rload', type=float, help='Resistance of the load')
  parser.add_argument('Lout', type=float, help='Secondary Inductance (in henries)')
  parser.add_argument('TR', type=float, help='Turns Ratio of the transformer (Primary/Secondary)')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  parser.add_argument('-m', '--max', action='store_true', help='Use maximum voltage for supply instead of RMS')
  parser.add_argument('-o', '--maxout', action='store_true', help='Use maximum voltage for desired output voltage instead of RMS')
  args = parser.parse_args()

  Vsrc = args.Vsrc
  Vf = args.Vf
  Vout = args.Vout
  Rrin = args.Rrin
  Rrout = args.Rrout
  Rload = args.Rload
  Lout = args.Lout
  TR = args.TR

  if args.max:
    Vsrc = fdiv(Vsrc,sqrt(2)) 

  if args.maxout:
    Vout = fdiv(Vout,sqrt(2)) 

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vsrc: {Vsrc}, Vf: {Vf}, Vout: {Vout}, Rrin: {Rrin}, Rrout: {Rrout}, Rload: {Rload}, Lout: {Lout}, TR: {TR}')

  Vload = Vout

  Irout = Ilout = Iout = Iload = fdiv(Vload,Rload)
  Vrout = fmul(Irout,Rrout)
  Vlout = fadd(Vout,Vrout)
  Vlin = fmul(Vlout,TR)
  watts = fmul(Vlout,Ilout)
  Xout = fmul(2,fmul(pi,fmul(Vf,Lout)))
  Plin = fsub(fdiv(pi,2),atan(fdiv(Xout,fadd(Rload,Rrout))))

  Ilin = Irin = Iin = Is = Itot = fdiv(watts,fmul(Vlin,cos(Plin)))
  Zlin = fdiv(Vlin,Ilin)
  Rlin = fmul(Zlin,cos(Plin))
  Xlin = Xin = Xtot = fmul(Zlin,sin(Plin))
  va = fmul(fmul(Ilin,Vlin),cos(Plin))

  Vrin = fmul(Irin, Rrin)
  Rin = fadd(Rlin,Rrin)
  Zin = sqrt(fadd(power(Rin,2),power(Xin,2)))
  Pin = acos(fdiv(Rin,Zin))
  Vin = fmul(Iin,Zin)
 
  Vtot = Vsrc
  Ztot = fdiv(Vtot,Itot)
  Rtot = sqrt(fsub(power(Ztot,2),power(Xtot,2)))
  Ptot = acos(fdiv(Rtot,Ztot))

  Rs = fsub(Rtot,Rin)
  Vs = fmul(Rs,Is)

  Lin = fmul(power(TR,2),Lout)

  print("Rs: {}".format(Rs))
  print("Iin: {}, Iout: {}".format(Iin, Iout))
  print("Ptot: {}°, Ztot: {}, Rtot: {}, Xtot: {}".format(r2d(Ptot), Ztot, Rtot, Xtot))
  print("Pin: {}°, Zin: {}, Rin: {}, Xin: {}".format(r2d(Pin), Zin, Rin, Xin))
  print("Plin: {}°, Zlin: {}, Rlin: {}, Xlin: {}".format(r2d(Plin), Zlin, Rlin, Xlin))
  print("Vtot: {}, Vs: {}, Vin: {}, Vrin: {}, Vlin: {}, Vout: {}, Vlout: {}, Vload: {}".format(Vtot, Vs, Vin, Vrin, Vlin, Vout, Vlout, Vload))
  print("Xout: {}, Lout: {}, Lin: {}, TR: {}".format(Xout, Lout, Lin, TR))
  print("va: {}, watts: {}".format(va, watts))

if __name__ == "__main__":
  main()
