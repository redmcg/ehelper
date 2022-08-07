# ehelper
Electronic helper functions written in Python

Is ~= 1e-12A for silicon\
Is ~= 1e-6A for germanium\
nVt ~= 26mV @ 27°C 

Defaults are:\
Is = 1e-12 (a silicon diode); and\
nVt = .026

The serial circuit is for a simple resistor and diode in series.

The parallel circuit adds a second resistor (R2) to the series circuit,
in parallel with the diode.

##### Analyse existing circuit
- asd.py: Analyse a Serial Diode Circuit
```
Usage: asd <Vcc> <R> [<Is>] [<nVt>]
```
- apd.py: Analyse a Parallel Diode Circuit
```
Usage: apd <Vcc> <R1> <R2> [<Is>] [<nVt>]
```

Example of a 470Ω resistor in series with a silicon diode:
```
./asd.py 5 470
```

##### Design a new circuit
- dsd.py: Design a Serial Diode Circuit
```
Usage: dsd <Vcc> <Id> [<Is>] [<nVt>]
```
- dpd.py: Design a Parallel Diode Circuit
```
Usage: dpd <Vcc> <Id> <IR2> [<Is>] [<nVt>]
```

Example of which series resistor to use in a 5v circuit with 
a silicon diode to get 10mA:
```
./dsd.py 5 .01
```
