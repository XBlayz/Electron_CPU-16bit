"""
Functionality:
    * Decode assembly instruction;
    * Automatic address allocation;
    * Variable system;
    * Label system;
"""

# Memory structure example
"""
|  DATA  |  ADDs  |      *PROGRAM Start*
| 0x---- | 0x0000 |             ↓
| 0x---- | 0x0001 |
| 0x---- | 0x0002 |
| 0x---- | 0x0003 |
...                       *PROGRAM End*
| 0x---- | 0x0ffc |     *VARIABLES Start*
| 0x---- | 0x0ffd |             ↓
| 0x---- | 0x0ffe |
| 0x---- | 0x0fff |
...                      *VARIABLES End*
| 0x---- | 0xfffe |
| 0x---- | 0xffff |
"""

# Program example
"""
;comment

section .data
    var1:   15      ;variable (word) with value 0x000f
    var2:   0xffff  ;variable (word) with value 0xffff
    array1: [3]     ;array (word[3]) with [0x0000, 0x0000, 0x0000, 0x0000]
    array2: [5]

section .text

"""