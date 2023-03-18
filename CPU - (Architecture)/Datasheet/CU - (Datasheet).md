# Control Unit
ROM (Add:*20bit* (**24bit**), Data:*39bit* (**64bit**))

## ADDRESS
- **Instruction**:   0-9   (*10bit*)
  - Ins. ID:   0-8  (*9bit*)
  - Ins. Type:  9   (*1bit*)
- **Beta**:         10-14  (*5bit*)
  - OF:   0(10)
  - SF:   1(11)
  - CF:   2(12)
  - ZF:   3(13)
  - Ins. Type: 4(14)
- *empty*:          15-18  (*4bit*)
- **uIns**:         19-23  (*5bit*)
## DATA
### Ram
- **eW**:       0   (*1bit*)
- **eR**:       1   (*1bit*)

### MAR
- **aMAR**:     2   (*1bit*)
- **kMAR**:     3   (*1bit*)

### ALU
- **kALU**:    4-6  (*3bit*)

### Register File
- **aRF**:      7   (*1bit*)

### IR
- **aIRx**:     8   (*1bit*)

- **aIRi**:     9   (*1bit*)
- **zIRi**:    10   (*1bit*)

- **aTIR**:    11   (*1bit*)

### PC
- **aPC**:     12   (*1bit*)
- **kPC**:     13   (*1bit*)

### Clock
- **HLT**:     14   (*1bit*)


### BUS DATA 1
- **In_1**:    15-17     (*3bit*)
- **Out_1**:   18-20     (*3bit*)
### BUS DATA 2
- **In_2**:    21-23     (*3bit*)
- **Out_2**:   24-26     (*3bit*)
### BUS DATA 3
- **In_3**:    27-29     (*3bit*)
- **Out_3**:   30-32     (*3bit*)

### BUS ADD
- **In_Add**:  33-35     (*3bit*)
- **Out_Add**: 36-38     (*3bit*)


- *empty*:     39-57     (*19bit*)


### Next uIns
- **Next uIns**: 58-62   (*5bit*)


- *empty*:     63        (*1bit*)