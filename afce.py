#!/usr/bin/env python

from mpmath import mp, mpf, exp, log, lambertw, fmul, fdiv, fsub, fadd, plot
import logging
import argparse

def main():
  parser = argparse.ArgumentParser(description='Analyse Shunt Feedback Common Emitter (Source Amplifier)')
  parser.add_argument('Vs', type=float, help='Source Voltage')
  parser.add_argument('Rload', type=float, help='Load resistor value (Ohms)')
  parser.add_argument('Rf', type=float, help='Feedback resistor value (Ohms)')
  parser.add_argument('Rs', type=float, nargs='?', default=-1, help='Source resistor value (Ohms) (default = -1; which means it is not present)')
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
  Rf = args.Rf
  Beta = args.Beta
  Is = args.Is
  N = args.N
  Vt = args.Vt
  nVt = N*Vt

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'Vs: {Vs}, Rs: {Rs}, Rload: {Rload}, Rf: {Rf}, Beta: {Beta}, Is: {Is}, N: {N}, Vt: {Vt}')

  Beta1 = fadd(Beta,1) # Beta plus 1
  if Rs == -1:
    RsMod = 1
  else:
    RsMod = fadd(fdiv(fadd(Rload,Rf),Rs),1) # will be just 1 if Rs is open

  Radd = fadd(fmul(Rload,Beta1),Rf)
  x = fdiv(fmul(fmul(Is,Radd),exp(fdiv(Vs,fmul(nVt,RsMod)))),fmul(fmul(nVt,Beta),RsMod))
  w = lambertw(x)
  Ib = fdiv(fmul(fmul(w,nVt),RsMod),Radd)
  Ic = fmul(Ib,Beta)
  Ie = fadd(Ib,Ic)
  Vbe = Vrs = fmul(log(fdiv(Ic,Is)),nVt)
  if Rs == -1:
    Irs = 0
  else:
    Irs = fdiv(Vrs,Rs)
  Irf = fadd(Irs,Ib)
  Iload = fadd(Irf,Ic)
  Vload = fmul(Iload,Rload)
  Vrf = fmul(Irf,Rf)
  gm = fdiv(Ic,Vt)
  Rpi = fdiv(Beta,gm) # or Vt/Ib
  Av = fdiv(fmul(Rload,fsub(1,fmul(gm,Rf))),fadd(Rload,Rf))
  Rmo = fdiv(fmul(Av,Rf),fsub(Av,1))
  Rleq = fdiv(fmul(Rload,Rmo),fadd(Rload,Rmo))
  Rmi = fdiv(Rf,fsub(1,Av))
  Rbase = fdiv(fmul(Rmi,Rpi),fadd(Rmi,Rpi))
  if Rs != -1:
    gain = fdiv(fmul(Rbase,Av),fadd(Rs,Rbase))
  print("Vload: {}, Iload: {}".format(Vload, Iload))
  print("Vrf: {}, Irf: {}".format(Vrf, Irf))
  if Rs != -1:
    print("Vrs: {}, Irs: {}".format(Vrs, Irs))
  print("Vbe: {}, Ib: {}".format(Vbe, Ib))
  print("Rpi: {}, gpi: {}, gm: {}".format(Rpi, fdiv(1,Rpi), gm))
  print("Av: {}, Rmo: {}, Rleq: {}".format(Av, Rmo, Rleq))
  print("Rmi: {}, Rbase: {}".format(Rmi, Rbase))
  if Rs != -1:
    print("gain: {}".format(gain))
  print("Ic: {}, Ie: {}".format(Ic, Ie))
  if args.graph:
    def Vbe(x):
      return fmul(log(fdiv(fmul(x,Beta),Is)),nVt)

    if Rs == -1:
      Irs = lambda x: 0
    else:
      Irs = lambda x: fdiv(Vbe(x),Rs)
      
    plot([lambda x: fsub(Vs,fmul(fadd(fmul(x,Beta1),Irs(x)),Rload)), lambda x: fadd(fmul(fadd(Irs(x),x),Rf),Vbe(x))], [0, fdiv(Vs,fmul(Beta1,Rload))], [0, Vs])

if __name__ == "__main__":
  main()
