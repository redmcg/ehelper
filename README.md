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
- 350 µH inductance
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
- 350 µH inductance
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
- 350 µH inductance

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
- 350 µH inductance

```
./dprlc.py 774000 10000 L .00035
```

##### Design a transformer circuit

The transformer circuit is a input resistor in series with the primary of the transformer.

On the secondary side is a single resistor providing the load.
```
usage: dt.py [-h] [-v] [-m] [-o] Vs Vf Vout Rout TR Lout
```

Example of a circuit with:
- 1V max input supply at 774 ㎑
- 0.25V max output desired
- 2000Ω resistor output load
- 2:1 turns ratio
- 87.5 µH inductance on the secondary

```
./dt.py -m 1 774e3 -o .25 2000 2 87.5e-6
```

##### Analyse a transformer circuit
```
usage: at.py [-h] [-v] [-m] Vsrc Vf Vs Vin Vout Rs Rrin Rrout Rload
```

Example of a circuit with:
- Input supply of 0.707107 Vrms at 195 Hz
- 0.469346 Vrms measured over input resistor
- 0.391846 Vrms measured over primary inductor
- 0.256941 Vrm measured over secondary inductor
- 1kΩ input resistor
- 256Ω resistance measured on the primary inductor
- 137Ω resistance measured on the secondary inductor
- 10kΩ output resistor

```
./at.py -v 0.707107 195.3125 0.469346 0.391846 0.256941 1000 256 137 10000
```


