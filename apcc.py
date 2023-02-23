#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot
import logging
import argparse

def main():
  parser = argparse.ArgumentParser(description='Analyse Parallel Biased (voltage divider) Common Collector (Voltage/Emitter Follower)')
  parser.add_argument('Vs', type=float, help='Source Voltage')
  parser.add_argument('R1', type=float, help='Source resistor value for Resistor 1 (Ohms)')
  parser.add_argument('R2', type=float, help='Source resistor value for Resistor 2 (Ohms)')
  parser.add_argument('Rload', type=float, help='Load resistor value (Ohms)')
  parser.add_argument('Beta', type=float, nargs='?', default=300,  help='Transistor Beta value (default = 300)')
  parser.add_argument('Is', type=float, nargs='?', default=1e-12, help='Base-Emitter Saturation current in Amps (default = 1e-12)')
  parser.add_argument('N', type=float, nargs='?', default=1, help='Emission Coefficient (default = 1)')
  parser.add_argument('--Vt', type=float, default=0.026, help='Thermal Voltage in Volts (default = 0.026)')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  Vs = args.Vs
  R1 = args.R1
  R2 = args.R2
  Rload = args.Rload
  Beta = args.Beta
  Is = args.Is
  N = args.N
  Vt = args.Vt
  nVt = N*Vt

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vs: {Vs}, R1: {R1}, R2: {R2}, Rload: {Rload}, Beta: {Beta}, Is: {Is}, N: {N}, Vt: {Vt}')

  Beta1 = fadd(Beta,1) # Beta plus 1
  rrp1 = fadd(fdiv(R1,R2),1) # R ratio plus 1
  vt_rrp1 = fmul(Vt,rrp1) # vt * rrp1
  y = fadd(R1,fmul(Beta1,fmul(Rload,rrp1)))
  x = fdiv(fmul(Is,fmul(y,exp(fdiv(Vs,vt_rrp1)))),fmul(Beta,fmul(Vt,rrp1)))
  w = lambertw(x)
  Ib = fdiv(fmul(w,vt_rrp1),y)
  Ic = fmul(Ib,Beta)
  Iload = Ie = fadd(Ib,Ic)
  Vbe = fmul(log(fdiv(fmul(Ib,Beta),Is)),nVt)
  Vload = fmul(Iload,Rload)
  Vr2 = Vb = fadd(Vbe,Vload)
  Ir2 = fdiv(Vr2,R2)
  Vr1 = fsub(Vs,Vr2)
  Ir1 = fdiv(Vr1,R1)
  Re = fdiv(Vt,Ie)
  gm = fdiv(Ic,Vt)
  Rpi = fdiv(Beta,gm) # or Re*(Beta+1) or Vt/Ib
  Rin = fadd(Rpi,fmul(Beta,Rload))
  Av = fdiv(fmul(Beta,Rload),Rin)
  Rout = fdiv(fmul(Rload,Re),fadd(Rload,Re))
  print("Vr1: {}, Ir1: {}".format(Vr1, Ir1))
  print("Vr2: {}, Ir2: {}".format(Vr2, Ir2))
  print("Vb: {}, Vbe: {}, Ib: {}".format(Vb, Vbe, Ib))
  print("Vload: {}, Iload: {}".format(Vload, Iload))
  print("Av: {}, Rin: {}, Rout: {}".format(Av, Rin, Rout))
  print("Rpi: {}, gpi: {},  Re: {}, gm: {}".format(Rpi, fdiv(1,Rpi), Re, gm))
  print("Ic: {}, Ie: {}".format(Ic, Ie))

  vb = lambda x: fadd(fmul(log(fdiv(fmul(x,Beta),Is)),nVt),fmul(fmul(x,Beta1),Rload)) # give x as Ib, what is Vb?
  if args.graph:
    plot([lambda x: fsub(Vs,fmul(fadd(x,fdiv(vb(x),R2)),R1)), lambda x: vb(x)], [0, fdiv(Vs,fadd(R1,R2))], [0, Vs])

if __name__ == "__main__":
  main()
