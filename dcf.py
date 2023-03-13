#!/usr/bin/env python

from mpmath import sin, cos, fadd, fsub, fmul, fdiv, power, sqrt, exp, log10, pi, mpc, cplot, fabs, sinh, asinh, cosh, log, coth, plot, polyval, acosh
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
    f.write("{}{} {} {} {}\n".format(self.letter,self.number,innode,outnode,self.value.real))

def write_ngspice(f, c, R, current):
  if current:
    source = "I"
  else:
    source = "V"

  f.write("Passive Chebyshev\n")
  f.write("\n")
  f.write("{}in in 0 DC 0 AC 1\n".format(source))

  if len(c) == 3 and c[0].letter == "C":
    nextinnode = "out"
  else:
    nextinnode = "in"
    nextnode = 1

  i = 1
  for v in c:
    innode = nextinnode
    if v.letter == "C" or v.letter == "R" and i > 1:
      outnode = 0
    else:
      if i < len(c) - 2:
        outnode = nextnode
        nextinnode = nextnode
        nextnode = nextnode + 1
      else:
        outnode = nextinnode = "out"
      
    v.write_ngspice(f,innode,outnode)
    i = i + 1

  f.write("\n")
  f.write(".AC DEC 100 0.01 1GIG\n")
  f.write(".control\n")
  f.write("run\n")
  f.write("plot mag(out)/.5\n")
  f.write(".endc\n")
  f.write(".END\n")


def main():
  parser = argparse.ArgumentParser(description='Design Chebyshev Filter')
  parser.add_argument('fc', type=float, help='Frequency Cut-off')
  parser.add_argument('N', type=int, help='Order of filter')
  parser.add_argument('R', type=float, help='Resistance of load')
  parser.add_argument('e', type=float, nargs='?', default=1, help='The ripple factor')
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
  e = args.e

  if args.radians:
    wc = fc
    fc = fdiv(wc,fmul(2,pi))
  else:
    wc = fmul(fc,fmul(2,pi))

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'fc: {fc}, N: {N}, R: {R}, e: {e}, radians: {args.radians}, current: {args.current}, ngspice: {args.ngspice}, force: {args.force}')

  w0 = fdiv(wc,cosh(fdiv(acosh(fdiv(1,e)),N)))
  logging.info(f'wc: {wc}, w0: {w0}')

  ed = fmul(log10(fadd(power(e,2),1)),10) # ripple in decibles
  beta = log(coth(fdiv(ed,fdiv(40,log(10)))))
  y = sinh(fdiv(beta,fmul(2,N)))

  a = []
  b = []

  for k in range(1,N+1):
    ak = sin(fdiv(fmul(fsub(fmul(2,k),1),pi),fmul(2,N)))
    bk = fadd(power(y,2),power(sin(fdiv(fmul(k,pi),N)),2))
    a.append(ak)
    b.append(bk)

  g = [1, fdiv(fmul(2,a[0]),y)]

  for k in range(1,N):
    gk = fdiv(fmul(4,fmul(a[k-1],a[k])),fmul(b[k-1],g[k]))
    g.append(gk)

  if N % 2 == 1:
    g.append(1)
  else:
    g.append(power(coth(fdiv(beta,4)),2))

  c = []

  i = 0
  for v in g:
    v = fdiv(v,w0)
    if i == 0:
      comp = "R"
      v = R
    elif i == len(g)-1:
      Rl = g[len(g)-1]
      if c[len(c)-1].letter == "L":
        Rl = fdiv(1,Rl)

      Rl = fmul(Rl,R)

      comp = "R"
      v = Rl
    elif i % 2 == 0 and not args.current or i % 2 == 1 and args.current:
      comp = "L"
      v = fmul(v,R)
    else:
      comp = "C"
      v = fdiv(v,R)

    v = Component(comp,i,v)
    v.print()
    c.append(v)
    i = i + 1

  if args.ngspice:
    if args.force:
      try:
        remove(args.ngspice)
      except:
        print(f"\nWARNING: Couldn't force removal of {args.ngspice}")
    try:
      with open("/dev/stdout", "w") if args.ngspice == "-" else open(args.ngspice, "x") as f:
        write_ngspice(f, c, R, args.current)
    except FileExistsError:
      print("\nCouldn't create {} as the file already exists. Use '-f' if you wish to replace it".format(args.ngspice))

  logging.info(f'Poles ({N}):')
  sp = []
  for m in range(1,N+1):
    thetam = fmul(fdiv(pi,2),fdiv(fsub(fmul(2,m),1),N))        
    spm = mpc(fmul(sinh(fmul(fdiv(1,N),asinh(fdiv(1,e)))),sin(thetam)),fmul(cosh(fmul(fdiv(1,N),asinh(fdiv(1,e)))),cos(thetam)))
    sp.append(fmul(w0,spm))
    logging.info(f'sp[{m}]: {sp[m-1]*-1}')

  poly = [fmul(power(2,fsub(N,1)),e)]
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
      if v != 1.0 or i == 0:
        poly_s = poly_s + f"{v}".replace("j","i")

      poly_s = poly_s + (poly_suffix[i] if i < len(poly_suffix) else f"s^{i}")

    return poly_s

  normalised_poly = []
  for i in range(0,len(poly)):
    normalised_poly.append(fdiv(poly[i],power(wc,i)))

  Rtot = fadd(R,Rl)
  component_poly = []
  for i in range(0,len(normalised_poly)):
    k = len(normalised_poly) - 1 - i
    component_poly.append(fdiv(fmul(Rtot,normalised_poly[i]),fmul(normalised_poly[len(normalised_poly)-1],power(wc,k))))

  logging.info(f"Product of poles: {poly_string(poly)}")
  logging.info(f"Normalised: {poly_string(normalised_poly)}")
  logging.info(f"Component Poly: {poly_string(component_poly)}")

  alt_comp_poly = f"{Rtot} * "
  for p in sp:
    mod = power(normalised_poly[len(normalised_poly)-1],fdiv(1,N))
    alt_comp_poly = alt_comp_poly + f"({poly_string([fdiv(mod,wc), fdiv(fmul(mod,p),wc)], False)}) "
  logging.info(f"Alternate form: {alt_comp_poly}")

  if args.graph:
    cplot(lambda x: fabs(fdiv(Rl,polyval(component_poly,x))), re=[float(-2*wc), float(2*wc)], im=[float(-2*wc), float(2*wc)], points=100000, verbose=True)

if __name__ == "__main__":
  main()
