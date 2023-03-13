#!/usr/bin/env python

from mpmath import sin, cos, fadd, fsub, fmul, fdiv, power, sqrt, exp, log10, pi, mpc, cplot, fabs, polyval
from os import remove
import argparse
import logging

class Component:
  def __init__(self, letter, number, value):
    self.letter = letter
    self.number = number
    self.value = value

  def print(self):
    print("{}{}: {}".format(self.letter,self.number,self.value))
    
  def write_ngspice(self, f, innode, outnode):
    f.write("{}{} {} {} {}\n".format(self.letter,self.number,innode,outnode,self.value))

def write_ngspice(f, c, wc, R, Rs, current):
  if current:
    source = "I"
  else:
    source = "V"

  f.write("Passive Butterworth\n")
  f.write("\n")
  f.write("{}in in 0 DC 0 AC 1\n".format(source))

  if Rs:
    if len(c) == 1 and c[0].letter == "C":
      nextinnode = "out"
    else:
      nextinnode = 1
      nextnode = 2
    f.write("Rs in {} {}\n".format(nextinnode,R))
  else:
    nextinnode = "in"
    nextnode = 1

  i = 1
  for v in c:
    innode = nextinnode
    if v.letter == "C":
      outnode = 0
    else:
      if i < len(c) - 1:
        outnode = nextnode
        nextinnode = nextnode
        nextnode = nextnode + 1
      else:
        outnode = nextinnode = "out"
      
    v.write_ngspice(f,innode,outnode)
    i = i + 1

  f.write("R{} {} 0 {}\n".format(len(c)+1,nextinnode,R))

  f.write("\n")
  f.write(".AC DEC 100 0.01 1GIG\n")
  f.write(".control\n")
  f.write("run\n")
  if Rs and not current:
    f.write("plot vdb(out)+6\n")
  else:
    f.write("plot vdb(out)\n")
  f.write(".endc\n")
  f.write(".END\n")


def main():
  parser = argparse.ArgumentParser(description='Design Butterfield Filter')
  parser.add_argument('fc', type=float, help='Frequency Cut-off')
  parser.add_argument('N', type=int, help='Order of filter')
  parser.add_argument('R', type=float, help='Resistance of load')
  parser.add_argument('-s', '--source', action='store_true', help='Add source resistance (same ohms as load)')
  parser.add_argument('-r', '--radians', action='store_true', help='Use radians instead of frequency for cut-off')
  parser.add_argument('-c', '--current', action='store_true', help='Input is a current source instead of voltage source')
  parser.add_argument('-n', '--ngspice', metavar="filename", help='Write an ngspice file')
  parser.add_argument('-f', '--force', action='store_true', help='Force creation of an ngfile by deleting an existing file')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  parser.add_argument('-g', '--graph', action='store_true', help='Display the complex output of the transfer function')
  args = parser.parse_args()

  fc = args.fc
  N = args.N
  R = args.R

  if args.radians:
    wc = fc
    fc = fdiv(wc,fmul(2,pi))
  else:
    wc = fmul(fc,fmul(2,pi))

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'fc: {fc}, N: {N}, R: {R}, source: {args.source}, radians: {args.radians}, current: {args.current}, ngspice: {args.ngspice}, force: {args.force}')
  logging.info(f'wc: {wc}')

  a = []
  c = []
  g = []

  for j in range(1,N+1):
    v = sin(fdiv(fmul(fsub(fmul(2,j),1),pi),fmul(2,N)))
    if args.source:
      g.append(v)
    else:
      a.append(v)
      c.append(power(cos(fdiv(fmul(j,pi),fmul(2,N))),2))

  if not args.source:
    g.append(a[0])

    for j in range(2,N+1):
      g.append(fdiv(fmul(a[j-1],a[j-2]),fmul(c[j-2],g[j-2])))

  c = []

  if args.source:
    Rtot = fmul(R,2)
  else:
    Rtot = R

  i = 1
  for v in reversed(g):
    v = fdiv(v,wc)
    if i % 2 == 1 and not (args.current or args.source) or i % 2 == 0 and (args.current or args.source):
      comp = "L"
      v = fmul(v,Rtot)
    else:
      if args.source:
        Rt = fdiv(R,2)
      else:
        Rt = R

      comp = "C"
      v = fdiv(v,Rt)

    v = Component(comp,i,v)
    v.print()
    c.append(v)
    i = i + 1

  if args.ngspice:
    if args.force:
      try:
        remove(args.ngspice)
      except:
        pass
    try:
      with open("/dev/stdout", "w") if args.ngspice == "-" else open(args.ngspice, "x") as f:
        write_ngspice(f, c, wc, R, args.source, args.current)
    except FileExistsError:
      print("\nCouldn't create {} as the file already exists. Use '-f' if you wish to replace it".format(args.ngspice))

  logging.info(f'Poles ({N}):')
  sp = []
  for k in range(1,N+1):
    sp.append(fmul(-wc,exp(fdiv(fmul(mpc(0,fsub(fadd(fmul(2,k),N),1)),pi),fmul(2,N)))))
    logging.info(f'sp[{k}]: {sp[k-1]*-1}')

  poly = [1]
  for p in sp:
    add = []
    for c in poly:
      add.append(fmul(c,p))
    poly.insert(0,0)
    for i in range(len(add)):
      poly[i] = fadd(poly[i], add[i])

  poly.reverse()

  def poly_string(poly, real_only = True):
    poly_suffix = ["", "s", "s²", "s³"]

    poly_s = ""
    sep = ""
    for i in range(len(poly)-1,-1,-1):
      poly_s = poly_s + sep
      sep = " + "
      v = poly[len(poly)-1-i]
      if real_only:
        v = v.real
      if v != 1 or i == 0:
        poly_s = poly_s + f"{v}".replace("j","i")

      poly_s = poly_s + (poly_suffix[i] if i < len(poly_suffix) else f"s^{i}")

    return poly_s

  normalised_poly = []
  for i in range(0,len(poly)):
    normalised_poly.append(fdiv(poly[i],power(wc,i)))

  component_poly = []
  for i in range(0,len(normalised_poly)):
    k = len(normalised_poly) - 1 - i
    component_poly.append(fdiv(fmul(normalised_poly[i],Rtot),power(wc,k)))

  logging.info(f"Product of poles: {poly_string(poly)}")
  logging.info(f"Normalised: {poly_string(normalised_poly)}")
  logging.info(f"Component Poly: {poly_string(component_poly)}")

  alt_comp_poly = f"{Rtot} * "
  for p in sp:
    alt_comp_poly = alt_comp_poly + f"({poly_string([fdiv(1,wc), fdiv(p,wc)], False)}) "
  logging.info(f"Alternate form: {alt_comp_poly}")

  if args.graph:
    cplot(lambda x: fabs(fdiv(R,polyval(component_poly,x))), re=[float(wc*-2), float(wc*2)], im=[float(wc*-2), float(wc*2)], points=100000, verbose=True)

if __name__ == "__main__":
  main()
