# Instruction Register
Doble word register (*32bit*) subdivided in 2 reg. (**IRx**, **IRi**).

## IRx
***Data*** and ***memory address*** of the executing instruction.
## IRi
***Instruction code*** with **RF** *indexes*.
- **i**: 0-2 (*3bit*)
- **j**: 3-5 (*3bit*)
- **INS**: 6-15 (*10bit*)

## TIR
**INS** bit *9* (bit *15* of the **TIR**) is used for identify if the loaded instruction need to ***load data*** in the **IRx**.