# ehelper
Electronic helper functions written in Python

Is ~= 1e-12A for silicon\
Is ~= 1e-6A for germanium\
N ~= 1\
Vt ~= 26mV @ 27°C

For a Red LED:\
Is ~= 1e-18A\
N ~= 1.8

Defaults are:\
Is = 1e-12 (a silicon diode); and\
nVt = .026

The serial circuit is for a simple resistor and diode in series.

The parallel circuit adds a second resistor (R2) to the series circuit,
in parallel with the diode.

##### Analyse existing circuit
- asd.py: Analyse a Serial Diode Circuit
```
usage: asd.py [-h] [--Vt VT] [-g] [-v] Vs R [Is] [N]
```
- apd.py: Analyse a Parallel Diode Circuit
```
usage: apd.py [-h] [--Vt VT] [-g] [-v] Vs R1 R2 [Is] [N]
```

Example of a 470Ω resistor in series with a silicon diode:
```
./asd.py 5 470
```

##### Design a new circuit
- dsd.py: Design a Serial Diode Circuit
```
usage: dsd.py [-h] [--Vt VT] [-g] [-v] Vs Id [Is] [N]
```
- dpd.py: Design a Parallel Diode Circuit
```
usage: dpd.py [-h] [--Vt VT] [-g] [-v] Vs Id IR2 [Is] [N]
```

Example of which series resistor to use in a 5v circuit with 
a silicon diode to get 10mA:
```
./dsd.py 5 .01
```

##### Analyse percentage of charge vs cycles of 𝜏
- apt.py: Analyse percentage of charge vs cycles of 𝜏
```
usage: apt.py [-h] [-c] [-g] [-v] value
```

Example of % of charge after 1 cycle of 𝜏:
```
./apt.py 1
```
##### Analyse a Serial RLC Circuit
```
usage: asrlc.py [-h] [-g] [-v] R L C
```

Example of a circuit with:
-  22  Ω resistance
-  35 µH inductance
- 120 ㎊ capacitance 

```
./asrlc.py 22 .00035 120e-12
```

##### Analyse a Parallel RLC Circuit
```
usage: aprlc.py [-h] [-g] [-v] R L C
```

Example of a circuit with: 
- 130 kΩ resistance
-  35 µH inductance
- 120 ㎊ capacitance

```
./aprlc.py 130000 .00035 120e-12
```

##### Design a Serial RLC Circuit
```
usage: dsrlc.py [-h] [-g] [-v] f0 bw {R,L,C} value
```

Example of a circuit with:
- 774 ㎑ resonance
-  10 ㎑ bandwidth
-  35 µH inductance

```
./dsrlc.py 774000 10000 L .00035
```

##### Design a Parallel RLC Circuit
```
usage: dprlc.py [-h] [-g] [-v] f0 bw {R,L,C} value
```

Example of a circuit with:
- 774 ㎑ resonance
-  10 ㎑ bandwidth
-  35 µH inductance

```
./dprlc.py 774000 10000 L .00035
```
