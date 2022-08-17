#!/usr/bin/env python

from mpmath import exp, log, fsub, plot
import argparse
import logging

def main():
  parser = argparse.ArgumentParser(description='Analyse charge % vs cycles of tau')
  parser.add_argument('value', type=float, help='Value of cycles or Vratio (the value for which we are not solving)')
  parser.add_argument('-c', '--cycles', action='store_true', help='Solve for cycles (if the flag is not set, solve for Vratio)')
  parser.add_argument('-g', '--graph', action='store_true', help='Draw a graph')
  parser.add_argument('-v', '--verbose', action='store_true', help='Print debug')
  args = parser.parse_args()

  value = args.value
  cycles = args.cycles

  if args.verbose:
    logging.basicConfig(format='%(levelname)s|%(message)s', level=logging.INFO)
  logging.info(f'value: {value}, cycles: {cycles}')

  if cycles:
    Vratio = value
    cycles = fsub(0,log(fsub(1,Vratio)))
    print("cycles: {}".format(cycles))
  else:
    cycles = value
    Vratio = fsub(1,exp(fsub(0,cycles)))
    print("Vratio: {}".format(Vratio))
  
  if args.graph:
    plot([lambda x: fsub(1,exp(fsub(0,x)))], [0, cycles], [0, 1])

if __name__ == "__main__":
  main()
