# Fetch - 0{0}
PC->MAR
M[MAR]-1->TIR, Inc(PC)
if(Ins_t)
    PC->MAR
    M[MAR]-1->IRx, TIR->IRi, Inc(PC)
else
    TIR->IRi
end

# ADD_Add - 1{1} | (M[X] + Ri -> Ri)
IRx->MAR
Ri+M[MAR]->Ri
EXT

# ADD_Data - 2{1} | (X + Ri -> Ri)
Ri+IRx->Ri
EXT

# ADD_Index - 3{1} | (M[X + Rj] + Ri -> Ri)
Rj+IRx->MAR
Ri+M[MAR]->Ri
EXT

# ADD_Reg - 4{0} | (Rj + Ri -> Ri)
Ri+Rj->Ri
EXT

# SUB_Add - 5{1} | (M[X] - Ri -> Ri)
IRx->MAR
Ri-M[MAR]->Ri
EXT

# SUB_Data - 6{1} | (X - Ri -> Ri)
Ri-IRx->Ri
EXT

# SUB_Index - 7{1} | (M[X + Rj] - Ri -> Ri)
Rj+IRx->MAR
Ri-M[MAR]->Ri
EXT

# SUB_Reg - 8{0} | (Rj - Ri -> Ri)
Ri-Rj->Ri
EXT

# AND_Add - 9{1} | (Ri and M[X] -> Ri)
IRx->MAR
Ri&M[MAR]->Ri
EXT

# AND_Data - 10{1} | (Ri and X -> Ri)
Ri&IRx->Ri
EXT

# AND_Index - 11{1} | (Ri and M[X + Rj] -> Ri)
Rj+IRx->MAR
Ri&M[MAR]->Ri
EXT

# AND_Reg - 12{0} | (Ri and Rj -> Ri)
Ri&Rj->Ri
EXT

# OR_Add - 13{1} | (Ri or M[X] -> Ri)
IRx->MAR
Ri|M[MAR]->Ri
EXT

# OR_Data - 14{1} | (Ri or X -> Ri)
Ri|IRx->Ri
EXT

# OR_Index - 15{1} | (Ri or M[X + Rj] -> Ri)
Rj+IRx->MAR
Ri|M[MAR]->Ri
EXT

# OR_Reg - 16{0} | (Ri or Rj -> Ri)
Ri|Rj->Ri
EXT

# XOR_Add - 17{1} | (Ri xor M[X] -> Ri)
IRx->MAR
Ri^M[MAR]->Ri
EXT

# XOR_Data - 18{1} | (Ri xor X -> Ri)
Ri^IRx->Ri
EXT

# XOR_Index - 19{1} | (Ri xor M[X + Rj] -> Ri)
Rj+IRx->MAR
Ri^M[MAR]->Ri
EXT

# XOR_Reg - 20{0} | (Ri xor Rj -> Ri)
Ri^Rj->Ri
EXT

# INC_Mem - 21{1} | (M[X] + 1 -> Ri)
IRx->MAR
Inc(M[MAR])->Ri
EXT

# INC_Add - 22{1} | (Ri + 1 -> M[X])
IRx->MAR
Inc(Ri)->M[MAR]
EXT

# INC_Reg - 23{0} | (Ri + 1 -> Ri)
Inc(Ri)->Ri
EXT

# INV_Mem - 24{1} | (-M[X] -> Ri)
IRx->MAR
Inv(M[MAR])->Ri
EXT

# INV_Add - 25{1} | (-Ri -> M[X])
IRx->MAR
Inv(Ri)->M[MAR]
EXT

# INV_Reg - 26{0} | (-Ri -> Ri)
Inv(Ri)->Ri
EXT

# NEG_Mem - 27{1} | (!M[X] -> Ri)
IRx->MAR
Neg(M[MAR])->Ri
EXT

# NEG_Add - 28{1} | (!Ri -> M[X])
IRx->MAR
Neg(Ri)->M[MAR]
EXT

# NEG_Reg - 29{0} | (!Ri -> Ri)
Neg(Ri)->Ri
EXT

# LOAD_Add - 30{1} | (M[X] -> Ri)
IRx->MAR
M[MAR]->Ri
EXT

# LOAD_Data - 31{1} | (X -> Ri)
IRx->Ri
EXT

# LOAD_Index - 32{1} | (M[X + Rj] -> Ri)
Rj+IRx->MAR
M[MAR]->Ri
EXT

# LOAD_Reg - 33{0} | (Rj -> Ri)
Rj->Ri
EXT

# STORE_Reg - 34{1} | (Ri -> M[X])
IRx->MAR
Ri->M[MAR]
EXT

# STORE_Index - 35{1} | (Ri -> M[X + Rj])
Rj+IRx->MAR
Ri->M[MAR]
EXT

# JMP - 36{1}
IRx->PC
EXT

# J_OF - 37{1}
NUL
if(OF)
    IRx->PC
else
    NUL
end
EXT

# JN_OF - 38{1}
NUL
if(OF)
    NUL
else
    IRx->PC
end
EXT

# J_SF - 39{1}
NUL
if(SF)
    IRx->PC
else
    NUL
end
EXT

# JN_SF - 40{1}
NUL
if(SF)
    NUL
else
    IRx->PC
end
EXT

# J_CF - 41{1}
NUL
if(CF)
    IRx->PC
else
    NUL
end
EXT

# JN_CF - 42{1}
NUL
if(CF)
    NUL
else
    IRx->PC
end
EXT

# J_ZF - 43{1}
NUL
if(ZF)
    IRx->PC
else
    NUL
end
EXT

# JN_ZF - 44{1}
NUL
if(ZF)
    NUL
else
    IRx->PC
end
EXT

# STOP - 98{0}
HLT

# NONE - 99{0}
NUL
EXT