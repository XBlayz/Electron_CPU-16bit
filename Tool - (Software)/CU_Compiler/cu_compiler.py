import sys

from tqdm import tqdm

from instruction_graph import Node
from instruction_graph import InsGraph



# CU ROM
CU_ADD  = 24            # CU ROM Address size
N_CU_ADD = 2**CU_ADD    # Number of CU Addresses
CU_DATA = 64            # CU ROM Word size

# Instruction
INS = 10            # Instruction size
INS_ID_POS   = 2**0 # ID position multiplier
INS_TYPE_POS = 2**9 # Type position multiplier
# Beta signals
BETA = 5        # Beta signals size
BETA_POS = {    # Beta signals positions (relative position, absolute position multiplier)
    "OF": (0, 2**10),
    "SF": (1, 2**11),
    "CF": (2, 2**12),
    "ZF": (3, 2**13),
    "Ins_t": (4, 2**14)
}
# empty
EMPTY_ADD = 4           # empty CU Address size
EMPTY_ADD_POS = 2**15   # empty CU Address positions multiplier
# uInstruction
UINS = 5            # uInstruction Address size
UINS_POS = 2**19    # uInstruction Address positions multiplier


# Alpha signal
# Control signal
eW = 2**0
eR = 2**1

aMAR = 2**2
kMAR = 2**3

kALU = 2**4
ALU_OP = {
    "A+B": 0*kALU,
    "A-B": 1*kALU,
    "B+1": 2*kALU,
    "-B": 3*kALU,
    "!B": 4*kALU,
    "A&B": 5*kALU,
    "A|B": 6*kALU,
    "A^B": 7*kALU
}

aRF = 2**7

aIRx = 2**8
aIRi = 2**9
zIRi = 2**10
aTIR = 2**11

aPC = 2**12
kPC = 2**13

HLT = 2**14

# BUS signal
BUS_1_in = 2**15
BUS_1_out = 2**18
BUS_1_IN = {
    "BUS_ADD": 0*BUS_1_in,
    "RAM": 1*BUS_1_in,
    "R": 2*BUS_1_in,
    "IRx": 3*BUS_1_in
}
BUS_1_OUT = {
    "BUS_ADD": 0*BUS_1_out,
    "RAM": 1*BUS_1_out,
    "RF_i": 2*BUS_1_out,
    "IRx": 3*BUS_1_out,
    "TIR": 4*BUS_1_out,
    "IO": 5*BUS_1_out
}

BUS_2_in = 2**21
BUS_2_out = 2**24
BUS_2_IN = {
    "BUS_ADD": 0*BUS_2_in,
    "RAM": 1*BUS_2_in,
    "RF_j": 2*BUS_2_in,
    "IRx": 3*BUS_2_in
}
BUS_2_OUT = {
    "BUS_ADD": 0*BUS_2_out,
    "RAM": 1*BUS_2_out,
    "A": 2*BUS_2_out,
    "IRx": 3*BUS_2_out,
    "TIR": 4*BUS_2_out
}

BUS_3_in = 2**27
BUS_3_out = 2**30
BUS_3_IN = {
    "BUS_ADD": 0*BUS_3_in,
    "RAM": 1*BUS_3_in,
    "R": 2*BUS_3_in,
    "RF_i": 3*BUS_3_in,
    "IRx": 4*BUS_3_in,
    "IO": 5*BUS_3_in
}   
BUS_3_OUT = {
    "BUS_ADD": 0*BUS_3_out,
    "RAM": 1*BUS_3_out,
    "B": 2*BUS_3_out,
    "IRx": 3*BUS_3_out,
    "TIR": 4*BUS_3_out
}

BUS_add_in = 2**33
BUS_add_out = 2**36
BUS_ADD_IN = {
    "BUS_DATA": 1*BUS_add_in,
    "MAR": 2*BUS_add_in,
    "IRx": 3*BUS_add_in,
    "PC": 4*BUS_add_in
}
BUS_ADD_OUT = {
    "BUS_DATA": 1*BUS_add_out,
    "MAR": 2*BUS_add_out,
    "PC": 3*BUS_add_out
}

UINS_DATA_POS = 2**58

# uInstruction set
UINS_SET = {
    "PC->MAR": BUS_ADD_IN["PC"]+BUS_ADD_OUT["MAR"]+aMAR,
    "M[MAR]-1->TIR": eR+BUS_1_IN["RAM"]+BUS_1_OUT["TIR"]+aTIR,
    "Inc(PC)": aPC+kPC,
    "M[MAR]-1->IRx": eR+BUS_1_IN["RAM"]+BUS_1_OUT["IRx"]+aIRx,
    "TIR->IRi": aIRi,
    "IRx->MAR": BUS_ADD_IN["IRx"]+BUS_ADD_OUT["MAR"]+aMAR,

    "Ri+M[MAR]->Ri": eR+BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RAM"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A+B"],
    "Ri+IRx->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["IRx"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A+B"],
    "Rj+IRx->MAR": BUS_3_IN["IRx"]+BUS_3_OUT["B"]+BUS_2_IN["RF_j"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["BUS_ADD"]+BUS_ADD_IN["BUS_DATA"]+BUS_ADD_OUT["MAR"]+aMAR+ALU_OP["A+B"],
    "Ri+Rj->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RF_j"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A+B"],

    "Ri-M[MAR]->Ri": eR+BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RAM"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A-B"],
    "Ri-IRx->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["IRx"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A-B"],
    "Ri-Rj->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RF_j"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A-B"],

    "Ri&M[MAR]->Ri": eR+BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RAM"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A&B"],
    "Ri&IRx->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["IRx"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A&B"],
    "Ri&Rj->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RF_j"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A&B"],

    "Ri|M[MAR]->Ri": eR+BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RAM"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A|B"],
    "Ri|IRx->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["IRx"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A|B"],
    "Ri|Rj->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RF_j"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A|B"],

    "Ri^M[MAR]->Ri": eR+BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RAM"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A^B"],
    "Ri^IRx->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["IRx"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A^B"],
    "Ri^Rj->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_2_IN["RF_j"]+BUS_2_OUT["A"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["A^B"],

    "Inc(M[MAR])->Ri": eR+BUS_3_IN["RAM"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["B+1"],
    "Inc(Ri)->M[MAR]": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RAM"]+eW+ALU_OP["B+1"],
    "Inc(Ri)->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["B+1"],

    "Inv(M[MAR])->Ri": eR+BUS_3_IN["RAM"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["-B"],
    "Inv(Ri)->M[MAR]": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RAM"]+eW+ALU_OP["-B"],
    "Inv(Ri)->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["-B"],

    "Neg(M[MAR])->Ri": eR+BUS_3_IN["RAM"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["!B"],
    "Neg(Ri)->M[MAR]": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RAM"]+eW+ALU_OP["!B"],
    "Neg(Ri)->Ri": BUS_3_IN["RF_i"]+BUS_3_OUT["B"]+BUS_1_IN["R"]+BUS_1_OUT["RF_i"]+aRF+ALU_OP["!B"],

    "M[MAR]->Ri": eR+BUS_1_IN["RAM"]+BUS_1_OUT["RF_i"]+aRF,
    "IRx->Ri": BUS_1_IN["IRx"]+BUS_1_OUT["RF_i"]+aRF,
    "Rj->Ri": BUS_2_IN["RF_j"]+BUS_2_OUT["BUS_ADD"]+BUS_ADD_IN["BUS_DATA"]+BUS_ADD_OUT["BUS_DATA"]+BUS_1_IN["BUS_ADD"]+BUS_1_OUT["RF_i"]+aRF,
    "Ri->M[MAR]": BUS_3_IN["RF_i"]+BUS_3_OUT["RAM"]+eW,
    "IRx->PC": BUS_ADD_IN["IRx"]+BUS_ADD_OUT["PC"]+aPC,

    "HLT": HLT,
    "EXT": zIRi+aIRi,

    "NUL": 0
}


# Beta signals combination
def bit_field(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:].zfill(5)]

N_BETA_COMB = 2**BETA   # Number of combination of beta signal
BETA_COMB = []
for i in range(N_BETA_COMB):
    BETA_COMB.append(bit_field(i))



# Creation dictionary of instruction
def ins_dict(lines:list[str]) -> dict[int, list[list[str]]]:
    results = {}
    invalid = set()
    
    ins_id = 0
    print("Creation of Instruction list:")
    for line in tqdm(lines):
        # First clean line
        line = line.replace("\n", "")
        # Skip empty line
        if len(line) == 0: continue

        # Check instruction ID line
        if "#" in line:
            line = line.replace(" ", "")
            ins_id = decode_ins_id(line.split("-")[1].split("|")[0])
            results[ins_id] = []
            continue
        
        # Second clean line
        line = line.replace(" ", "")
        rtl = line.split(",")

        # Check list of RTL if they are valid
        check_rtl(rtl, invalid)

        # Set RTL
        results[ins_id].append(rtl)

    return results

def decode_ins_id(line:str) -> int:
    global INS_TYPE_POS


    line = line.replace("}", "")
    ins_id = line.split("{")                            # Extract the Instruction type
    return int(ins_id[0]) + int(ins_id[1])*INS_TYPE_POS # Calculate the Instruction

# Micro instruction decoder
def ins_dict_decoder(ins_dict:dict[int, list[list[str]]], print_data=False):
    global N_CU_ADD, BETA_POS, UINS_POS


    # Initialization of the CU ROM list
    results = []
    print("Creation ROM list:")
    for _ in tqdm(range(N_CU_ADD)):
        results.append(0)

    # Decoding each instructions
    print("Decoding Instruction:")
    for ins_id in tqdm(ins_dict):
        rtl_list = ins_dict[ins_id] # List of line of the RTL code of the instruction {ins_id}

        rtl_graph = create_graph(rtl_list)  # Create the instruction graph of the instruction {ins_id}
        node_set = rtl_graph.set_of_node()  # Set of Node of the instruction graph of {ins_id}
        for node in node_set:
            if node.info == "-ROOT-":   # Skipping the Node root of the graph
                continue
            if len(node.next_l) == 0:           # Node with no next
                beta_list = list_of_beta({})    # All beta combination

                for beta in beta_list:
                    add = calculate_add(ins_id, beta, node)
                    data = calculate_data(node, Node({"Ins_N": 0})) # Next Node is set to 0
                    results[add[0]] = data[0]   # Adding (RTL + Next_uIns) at the address (Ins_ID + Beta + uIns_N)

                    if print_data:
                        print(f"{add[1]}: {data[1]} - {data[2]}")   # Print of the added data

            for next_node in node.next_l:   # Node with next >= 1
                next_node:Node
                # All beta combination in the branch with the beta signal of {next_node}
                beta_list = list_of_beta(next_node.info["Beta"])

                for beta in beta_list:
                    add = calculate_add(ins_id, beta, node)
                    data = calculate_data(node, next_node)
                    results[add[0]] = data[0]   # Adding (RTL + Next_uIns) at the address (Ins_ID + Beta + uIns_N)

                    if print_data:
                        print(f"{add[1]}: {data[1]} - {data[2]}")   # Print of the added data
                
    return results

# Create instruction graph from RTL
def create_graph(rtl_list:list[list[str]]) -> InsGraph:
    graph = InsGraph()
    last_nodes = [graph.root]   # List of node how have as next the current line
    branches_node = []          # List of branches: [start_node_branching, end_1_branch, beta_signal]

    fixed_beta = {}

    ins_c = 0
    for rtl_line in rtl_list:
        if "if" in rtl_line[0]:
            try:
                b = extract_beta(rtl_line[0])   # Extract beta signal of the branch
                fixed_beta[b] = 1               # Set the beta signal {b} to 1
            except KeyError:
                print(f"Invalid beta: {rtl_line[0]}")
                print("Compilation failed.")
                sys.exit()

            branches_node.append([last_nodes.copy(), None, b])  # Add the new branching
        elif "else" == rtl_line[0]:
            fixed_beta[branches_node[-1][2]] = 0    # Set the beta signal {b} to 0

            branches_node[-1][1] = last_nodes.copy()    # Add the end of the 1° branch
            last_nodes = branches_node[-1][0].copy()    # Update the last node with the start node of the branching
        elif "end" == rtl_line[0]:
            fixed_beta.pop(branches_node[-1][2])    # Set the beta signal {b} to all the value by removing it

            last_nodes.extend(branches_node.pop()[1])   # Update the last node with the end node of the 1° branch
        else:
            try:
                # NODE(Ins_data, Ins_number, Beta_fixed)
                current_node = Node({"Ins": decode_rtl_line(rtl_line), "Ins_N": ins_c, "Beta": fixed_beta.copy()})
            except KeyError:
                print(f"Invalid RTL: {rtl_line}")
                print("Compilation failed.")
                sys.exit()

            for last_node in last_nodes:
                last_node.next_l.append(current_node)   # Add the current node as the next for all the last node
            last_nodes = [current_node]                 # Update the last node as the current

            ins_c += 1  # Increment instruction counter
    
    return graph

def extract_beta(string:str):
    return string.replace(")", "").split("(")[1]

def decode_rtl_line(rtl_line:list[str]) -> int:
    global UINS_SET


    results = 0
    for rtl in rtl_line:
        results += UINS_SET[rtl]    # Adding all the alpha signal of the relative uIns {rtl}
    return results

# List of all beta combination with {fixed_beta_d} fixed value
def list_of_beta(fixed_beta_d:dict[str, int]) -> list[int]:
    global BETA_POS, BETA_COMB, N_BETA_COMB, BETA


    r = []
    remove_index = set()
    # Find all the index of the combination not valid for the fixed value
    for fixed_beta in fixed_beta_d:
        pos = BETA - BETA_POS[fixed_beta][0] - 1    # Bit position to validate
        set_value = fixed_beta_d[fixed_beta]        # Value to validate
        for i in range(N_BETA_COMB):
            if i in remove_index or BETA_COMB[i][pos] != set_value:
                remove_index.add(i) # Adding the index of the element than the combination[{pos}] != {set_value}
    
    # Adding at the results only the valid combination
    for i in range(N_BETA_COMB):
        if i in remove_index:
            continue
        r.append(0)

        # Reconstruct the number from the array of bit
        for j in range(BETA):
            r[-1] += BETA_COMB[i][j] * (2**(BETA-j-1))
    
    return r

def calculate_add(ins_id, beta, node:Node):
    add = ins_id + beta*BETA_POS["OF"][1] + node.info["Ins_N"]*UINS_POS

    add_str = bin(add)[2:].zfill(24)
    add_str = add_str[:5]+'|'+add_str[5:9]+'|'+add_str[9:14]+'|'+add_str[14:]

    return (add, add_str)

def calculate_data(node:Node, next_node:Node):
    global UINS_DATA_POS


    data_rtl = node.info["Ins"]
    data_next = next_node.info["Ins_N"]

    data = data_rtl + data_next*UINS_DATA_POS

    return (data, data_rtl, data_next)

# Check list of RTL if they are valid
def check_rtl(rtl_list:list[str], invalid:set):
    global UINS_SET


    for rtl in rtl_list:
        valid = rtl.find("if") != -1 or rtl.find("else") != -1 or rtl.find("end") != -1 or rtl in UINS_SET
        if not valid and rtl not in invalid:
            invalid.add(rtl)
            print(f"WARNING: {rtl} not decoded")



# COMPILATION
if __name__ == "__main__":
    ins_set_file = ".\CU_Instructions\CU_Instructions-RTL (v1.0).md"
    data_file = ".\CU_Instructions\CU_data.txt"

    CU_rom = []
    print("Start compiling...")
    with open(ins_set_file) as f:
        CU_rom = ins_dict_decoder(ins_dict(f.readlines()))
    print("Compilation completed successfully.")

    print("---")

    # WRITING ON FILE
    print("Start writing on file...")
    with open(data_file , "w") as f:
        f.write("v2.0 raw\n")

        i = 0
        for data in tqdm(CU_rom):
            f.write(hex(data)[2:])
            i += 1

            if i == 8:
                i = 0
                f.write("\n")
            else:
                f.write(" ")
    print("Writing completed successfully.")