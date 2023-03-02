#!/usr/bin/env python

from mpmath import sin, cos, fsub, fmul, fdiv, power, pi
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
    f.write("Rs in 1 {}\n".format(R))
    nextinnode = 1
    nextnode = 2
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
  f.write(".AC DEC 100 0.01 1MEG\n")
  f.write(".control\n")
  f.write("run\n")
  if Rs:
    f.write("plot vdb(out)-vdb(1)\n")
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

  if args.source:
    Rt = fmul(R,2)
  else:
    Rt = R

  c = []

  i = 1
  for v in reversed(g):
    v = fdiv(v,wc)
    if i % 2 == 0 and not args.current or i % 2 == 1 and args.current:
      comp = "C"
      v = fdiv(v,Rt)
    else:
      comp = "L"
      v = fmul(v,Rt)
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
      with open(args.ngspice, "x") as f:
        write_ngspice(f, c, wc, R, args.source, args.current)
    except FileExistsError:
      print("\nCouldn't create {} as the file already exists. Use '-f' if you wish to replace it".format(args.ngspice))

if __name__ == "__main__":
  main()
