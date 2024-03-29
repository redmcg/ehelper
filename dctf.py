#!/usr/bin/env python

from mpmath import sin, cos, fadd, fsub, fmul, fdiv, power, sqrt, exp, log10, pi, mpc, cplot, fabs, sinh, asinh, cosh, log, coth, plot, polyval, acosh, polyroots
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

  f.write("Cauer Topology Filter\n")
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
  parser = argparse.ArgumentParser(description='Design Cauer Topology Filter')
  parser.add_argument('C', type=float, nargs='+', help="List of coefficients from the filter's normalised transfer function (highest order first)")
  parser.add_argument('-c', '--current', action='store_true', help='Input is a current source instead of voltage source')
  parser.add_argument('-n', '--ngspice', metavar="filename", help='Write an ngspice file')
  parser.add_argument('-f', '--force', action='store_true', help='Force creation of an ngfile by deleting an existing file')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  parser.add_argument('-g', '--graph', action='store_true', help='Display the complex output of the transfer function')
  parser.add_argument('-w', '--wc', type=float, default=1, help='Set the cutoff value for the output components (in radians)')
  parser.add_argument('-r', '--rs', type=float, default=1, help='Set the value of the source resistor')
  args = parser.parse_args()

  C = args.C

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'C: {C}, current: {args.current}, ngspice: {args.ngspice}, force: {args.force}')

  c = []
  R = args.rs
  wc = args.wc
  g = [R]
  R0 = Rs = 1.0

  i = len(C)
  s = [0]*i
  for v in C:
    i = i -1
    s[i] = v

  match len(C):
    case 1:
      parser.print_usage()
      print("\nerror: at least two coefficients [C] must be specified")
      exit(1)
    case 2:
      R2 = R0
      Rtot = fadd(R0,R2)
      mod = fdiv(Rtot,s[0])
      C1 = fmul(s[1],mod)
      g.append(C1)
      g.append(R2)
      component_poly_f = lambda c: [fmul(c[0].value,fmul(c[1].value,c[2].value)),fadd(c[0].value,c[2].value)]
    case 3:
      C1 = fdiv(fmul(2,s[2]),s[1])
      Rtot = fdiv(fmul(-s[0],fmul(power(C1,2),R0)),fsub(s[2],fmul(s[0],power(C1,2))))
      R3 = Rl = fsub(Rtot,R0)
      L2 = fmul(C1,R3)
      g.append(C1)
      g.append(L2)
      g.append(R3)
      component_poly_f = lambda c: [fmul(c[0].value,fmul(c[1].value,c[2].value)),fadd(fmul(c[0].value,fmul(c[1].value,c[3].value)),c[2].value),fadd(c[0].value,c[3].value)]
    case 4:
      a = fmul(s[0],power(s[3],2))
      b = fmul(fmul(s[1],fmul(s[2],s[3])),-1)
      coeffs = [a,b,fmul(3,a),fadd(power(s[2],3),fmul(2,b)),fmul(3,a),b,a]
      roots = polyroots(coeffs)
      # TODO: take the largest real root and give the user the option to choose alternatives
      Rl = R4 = roots[1]
      Rtot = fadd(R0,R4)
      mod = fdiv(Rtot,s[0])
      C3 = fdiv(fmul(s[3],fadd(1,power(R4,2))),fmul(s[2],R4))
      C1 = fdiv(C3,R4)
      L2 = fdiv(fmul(s[3],mod),power(fmul(C1,R4),2))
      g.append(C1)
      g.append(L2)
      g.append(C3)
      g.append(R4)
      component_poly_f = lambda c: [fmul(c[0].value,fmul(c[1].value,fmul(c[2].value,fmul(c[3].value,c[4].value)))),fadd(fmul(c[0].value,fmul(c[1].value,c[2].value)),fmul(c[2].value,fmul(c[3].value,c[4].value))),fadd(fmul(fmul(c[0].value,c[4].value),fadd(c[1].value,c[3].value)),c[2].value),fadd(c[0].value,c[4].value)]
    case 5:
      Rtot = fdiv(fmul(16,fmul(s[0],fmul(s[4],fsub(2,power(s[4],2))))),fadd(fmul(32,fmul(s[0],s[4])),fsub(fmul(4,fmul(s[2],fmul(power(s[3],2),s[4]))),fadd(fmul(8,fmul(s[1],s[3])),fadd(fmul(16,fmul(s[0],power(s[4],3))),power(s[3],4))))))
      C1 = fdiv(fmul(2,s[4]),s[3])

      nnn = fadd(fmul(16,fmul(s[0],fmul(power(s[4],3),fsub(Rtot,1)))),fsub(fmul(power(s[3],4),Rtot),fmul(4,fmul(s[2],fmul(power(s[3],2),fmul(s[4],Rtot))))))
      ddd = fmul(16,fmul(s[0],fmul(s[3],fmul(power(s[4],2),fsub(Rtot,1)))))
      eee = fmul(64,fmul(s[0],fmul(power(s[3],4),fmul(power(s[4],2),Rtot))))

      C3 = fdiv(fsub(sqrt(fsub(power(nnn,2),eee)),nnn),ddd)
      L4 = fdiv(fmul(2,fmul(s[4],fsub(Rtot,1))),s[3])
      R5 = fsub(Rtot,1)
      mod = fdiv(Rtot,s[0])
      L2 = fdiv(fmul(s[4],mod),fmul(C1,fmul(C3,L4)))

      g.append(C1.real)
      g.append(L2.real)
      g.append(C3.real)
      g.append(L4.real)
      g.append(R5.real)
      component_poly_f = lambda c: [fmul(c[0].value,fmul(c[1].value,fmul(c[2].value,fmul(c[3].value,c[4].value)))),fadd(fmul(c[0].value,fmul(c[1].value,fmul(c[2].value,fmul(c[3].value,c[5].value)))),fmul(c[2].value,fmul(c[3].value,c[4].value))),fadd(fmul(c[0].value,fmul(c[1].value,c[2].value)),fadd(fmul(c[0].value,fmul(c[1].value,c[4].value)),fadd(fmul(c[0].value,fmul(c[3].value,c[4].value)),fmul(c[2].value,fmul(c[3].value,c[5].value))))),fadd(fmul(c[0].value,fmul(c[1].value,c[5].value)),fadd(fmul(c[0].value,fmul(c[3].value,c[5].value)),fadd(c[2].value,c[4].value))),fadd(c[0].value,c[5].value)]
    case _:
      parser.print_usage()
      print("\nerror: more than five coefficients [C] is not currently supported")
      exit(1)

  i = 0
  for v in g:
    v = fdiv(v,wc)
    if i == 0:
      comp = "R"
      v = R
    elif i == len(g)-1:
      Rl = g[len(g)-1]
      comp = "R"
      Rl = v = fmul(Rl,R)
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

  component_poly = component_poly_f(c)
  logging.info(f"Normalised: {poly_string(C)}")
  logging.info(f"Component Poly: {poly_string(component_poly)}")

  if args.graph:
    cplot(lambda x: fabs(fdiv(Rl,polyval(component_poly,x))), re=[float(-2*wc), float(2*wc)], im=[float(-2*wc), float(2*wc)], points=100000, verbose=True)

if __name__ == "__main__":
  main()
