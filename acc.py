#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot
import logging
import argparse

def main():
  parser = argparse.ArgumentParser(description='Analyse Common Collector (Voltage/Emitter Follower)')
  parser.add_argument('Vs', type=float, help='Source Voltage')
  parser.add_argument('Rs', type=float, help='Source resistor value (Ohms)')
  parser.add_argument('Rload', type=float, help='Load resistor value (Ohms)')
  parser.add_argument('Beta', type=float, nargs='?', default=300,  help='Transistor Beta value (default = 300)')
  parser.add_argument('Is', type=float, nargs='?', default=1e-12, help='Base-Emitter Saturation current in Amps (default = 1e-12)')
  parser.add_argument('N', type=float, nargs='?', default=1, help='Emission Coefficient (default = 1)')
  parser.add_argument('--Vt', type=float, default=0.026, help='Thermal Voltage in Volts (default = 0.026)')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  Vs = args.Vs
  Rs = args.Rs
  Rload = args.Rload
  Beta = args.Beta
  Is = args.Is
  N = args.N
  Vt = args.Vt
  nVt = N*Vt

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vs: {Vs}, Rs: {Rs}, Rload: {Rload}, Beta: {Beta}, Is: {Is}, N: {N}, Vt: {Vt}')

  x = fdiv(fmul(fmul(Is,fadd(Rs,fmul(Rload,fadd(Beta,1)))),exp(fdiv(Vs,nVt))),fmul(nVt,Beta))
  w = lambertw(x)
  Ib = fdiv(fmul(w,nVt),fadd(Rs,fmul(Rload,fadd(Beta,1))))
  Ic = fmul(Ib,Beta)
  Iload = Ie = fadd(Ib,Ic)
  Vbe = fmul(log(fdiv(fmul(Ib,Beta),Is)),nVt)
  Vload = fmul(Iload,Rload)
  Vr = fsub(Vs, fadd(Vbe,Vload))
  Ir = fdiv(Vr, Rs)
  Re = fdiv(Vt,Ie)
  gm = fdiv(Ic,Vt)
  Rpi = fdiv(Beta,gm) # or Re*(Beta+1) or Vt/Ib
  Rin = fadd(Rpi,fmul(Beta,Rload))
  Av = fdiv(fmul(Beta,Rload),Rin)
  Rout = fdiv(fmul(Rload,Re),fadd(Rload,Re))
  print("Vr: {}, Ir: {}".format(Vr, Ir))
  print("Vbe: {}, Ib: {}".format(Vbe, Ib))
  print("Vload: {}, Iload: {}".format(Vload, Iload))
  print("Av: {}, Rin: {}, Rout: {}".format(Av, Rin, Rout))
  print("Rpi: {}, gpi: {},  Re: {}, gm: {}".format(Rpi, fdiv(1,Rpi), Re, gm))
  print("Ic: {}, Ie: {}".format(Ic, Ie))
  if args.graph:
    plot([lambda x: fsub(Vs,fmul(x,R)), lambda x: fmul(nVt,log(fadd(fdiv(x,Is),1)))], [0, fdiv(Vs,R)], [0, Vs])

if __name__ == "__main__":
  main()
