# Electron CPU (16bit)

## CPU *(16bit)* architecture made using [Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution) for learning how do CPU works on the hardware level.

A simple 16bit, 8 register, multi BUS **CPU** created using [Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution) for testing and playing around by setting up different **instruction set** and executing **programs**, that can be made using *customs tools* (simple Python programs). The CPU uses a simple **Register File** architecture with a **direct BUS I/O** interface, used for connecting different *peripherals*.
The project provides:
* **CPU logic diagram**;
* **Logisim-evolution project**;
* *Datasheets* for all the different *components*:
  * **CU** (Control Unit);
  * **IR** (Instruction Register);
  * **Memory**;
  * **PC** (Program Counter);
  * **RF** (Register File);
* *Programming tools*:
  * **CU compiler** (CPU *instruction set* compiler);
* *Programs examples*:
  * **Addition**
  * **Greater**

### CPU diagram
<img src=".img\CPU diagram.svg">

### Logisim preview (v1.0)
<img src=".img\Logisim CPU.png">

---

## (How to use)
### How to use the [Logisim-evolution project](CPU%20-%20(Architecture)/Electron_CPU_16bit.circ) :

For opening the [**Logisim-evolution project**](CPU%20-%20(Architecture)/Electron_CPU_16bit.circ) you need to download [Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution) from the GitHub page I linked [<u>here</u>](https://github.com/logisim-evolution/logisim-evolution/releases).

The project is created on the `v3.8.0`, but I think it wil work with all the future versions.

### How to load programs in the CPU :

For loading a **program** in the CPU you need to *compile* the source code in *binari* using the loaded **instruction set** of the CPU, and then load the file in the **RAM** (you can load a text file like the ones in the [Example - (Programs)](Example%20-%20(Programs)/Addition/Addition_data.txt) using the *`Edit content/Open`* functionality of [Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution)).

### How to use the [**CU compiler**](Tool%20-%20(Software)/CU_Compiler/cu_compiler.py) :

If you want to add **instruction** to the *instruction set* of the CPU what you need to do is:
1. Add the **RTL code** (**R**egister **T**ransfer **L**anguage) of the instruction to add to this [file](Tool%20-%20(Software)/CU_Compiler/CU_Instructions/CU_Instructions-RTL%20(v1.0).md);
2. Add the new **μ-instruction** (*micro* instruction) to the `UINS_SET` dictionary (line 137 of the [**CU compiler**](Tool%20-%20(Software)/CU_Compiler/cu_compiler.py)) with the relative **alpha signal**;
3. Recompile the `CU_data.txt` file by *running* the Python script;
4. Put the new `CU_data.txt` file in the **CU ROM** in ***Logisim***;

You might need to install the `tqdm` package, used for displaying progress bas in the terminal during the compilation process. You can use this command in your shell:

    pip install tqdm

More info [<u>here</u>](https://github.com/tqdm/tqdm).

## -Find a bug?-

If you found an *issue* or would like to submit an *improvement* to this project, please submit an issue using the **issues tab** above. If you would like to submit a **PR** with a *fix*, reference the *issue* you are referring to.

If you want any *additional information* about the **project**, post an **issue** and I will help you as soon as it's possible.

## -Known issues- (Work in progress)

List of things to **add** or **improve** *(Checked means **W.I.P**)*:
- [X] Machine code compiler;
- [ ] Fix name of misleading μ-instruction;
- [ ] I/O functionality (+datasheet);
- [ ] ...

---

#### NOTE :

Take in consideration that some of the *μ-instruction* in the [CU_Instructions-RTL (v1.0)](Tool%20-%20(Software)/CU_Compiler/CU_Instructions/CU_Instructions-RTL%20(v1.0).md) file, relative to **ALU operation** that use *2 inputs*, have *misleading names* because the order of the operation is actually **reversed**!

This is due to an **error** occurred during the naming of the *μ-instruction* and dose not falls back on the actual **implementation**.

This is only a problem for ***non commutativity operation***, like the *subtraction*, where the actual order of operation can change the **results**.

The things you need to remember is that the **Ri** register can only be *directly put* in the ***B*** space of the **ALU**, and the **Rj** register can only be *directly put* in the ***A*** space of the **ALU**.

This will be solved in a *future update*, and when it happens this note will be ***removed***.