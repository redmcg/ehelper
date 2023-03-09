#!/usr/bin/env python

from mpmath import sin, cos, fadd, fsub, fmul, fdiv, power, sqrt, exp, log10, pi, mpc, cplot, fabs, sinh, asinh, cosh, log, coth, plot, polyval
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

def write_ngspice(f, c, wc, R, current):
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
    v = fdiv(v,wc)
    if i == 0:
      Rt = R

      comp = "R"
      v = Rt
    elif i == len(g)-1:
      Rt = g[len(g)-1]
      if c[len(c)-1].letter == "L":
        Rt = fdiv(1,Rt)

      Rt = fmul(Rt,R)

      comp = "R"
      v = Rt
    elif i % 2 == 0 and not args.current or i % 2 == 1 and args.current:
      Rt = fmul(R,2)
      Rt = R

      comp = "L"
      v = fmul(v,Rt)
    else:
      Rt = fdiv(R,2)
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
        write_ngspice(f, c, wc, R, args.current)
    except FileExistsError:
      print("\nCouldn't create {} as the file already exists. Use '-f' if you wish to replace it".format(args.ngspice))

  sp = []
  for m in range(1,N+1):
    thetam = fmul(fdiv(pi,2),fdiv(fsub(fmul(2,m),1),N))        
    spm = mpc(fmul(sinh(fmul(fdiv(1,N),asinh(fdiv(1,e)))),sin(thetam)),fmul(cosh(fmul(fdiv(1,N),asinh(fdiv(1,e)))),cos(thetam)))
    if spm.real > 0:
      sp.append(fmul(wc,spm))

  poly = [fmul(power(2,fsub(N,1)),e)]
  for p in sp:
    add = []
    for c in poly:
      add.append(fmul(c,p))
    poly.insert(0,0)
    for i in range(len(add)):
      poly[i] = fadd(poly[i], add[i])

  poly_suffix = ["", "s", "s²", "s³"]

  poly_s = ""
  sep = ""
  for i in range(len(poly)-1,-1,-1):
    poly_s = poly_s + sep
    sep = " + "
    v = poly[i].real
    if v != 1 or i == 0:
      poly_s = poly_s + f"{v}"

    poly_s = poly_s + (poly_suffix[i] if i < len(poly_suffix) else f"s^{i}")

  print()
  print(poly_s)

  if args.graph:
    poly.reverse()
    cplot(lambda x: fabs(fdiv(power(wc,N),polyval(poly,x))), re=[float(-2*wc), float(2*wc)], im=[float(-2*wc), float(2*wc)], points=100000, verbose=True)

if __name__ == "__main__":
  main()
