# building assembler in python
asm_file="C:\\amrita uni\\s2\\EOC-2\\Assembler\\test.asm"
binary_file="C:\\amrita uni\\s2\\EOC-2\\Assembler\\test-1.txt"
symbol_table={"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R15":15,"SCREEN":16384,"KBD":24576,"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4}
c_inst_tabel={"0": "0101010", 
              "1": "0111111",
              "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101",}
def format_dest(dest):
    dest_mapping = {
        "": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }
    return dest_mapping.get(dest, "000")#for default values
def format_comp(comp):
    comp_mapping = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101",
    }
    return comp_mapping.get(comp, "0000000")#for default values

def format_jump(jump):
    jump_mapping = {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }
    return jump_mapping.get(jump, "000") #for default values
#first pass
with open(asm_file, "r") as viewer:
    pointing_address=0
    for line in viewer:
        line=line.strip()#to remove empty spaces after or before string of line
        if not line or line.startswith("//"):
            continue
        #labels
        if line.startswith("(") and line.endswith(")"):
            label=line[1:-1]
            symbol_table[label]=pointing_address
        else:
            pointing_address+=1
#second pass
with open (asm_file,"r") as reader , open(binary_file,"w") as writer:
    pointing_address=16
    for line in reader:
        line = line.strip()
        if not line or line.startswith("//") :
            continue
        if line.startswith("(") or line.endswith(")"):
            continue
        if line.startswith("@"):
            symbol=line[1:]
            if symbol[0].isdigit(): #numeric
                value=int(symbol)
            else:#symbol or label
                if symbol not in symbol_table:
                    symbol_table[symbol]= pointing_address
                    pointing_address+=1
                value=symbol_table[symbol]
            binary_code=format(value, "016b")
            writer.write(binary_code + "\n")
        else:
            dest,comp,jump="","",""
            if "=" in line:
                dest,comp=line.split("=")
            if ";" in line:
                comp,jump=line.split(";")
            dest_binary=format_dest(dest)
            comp_binary=format_comp(comp)
            jump_binary=format_jump(jump)

            binary_code="111"+ comp_binary+dest_binary+jump_binary
            writer.write(binary_code+"\n")
            print("binary output is written succussfully to ",binary_file)
            print("\nsymbol table")
            for symbol,address in  symbol_table.items():
                print(f"{symbol} {address}")   

            with open (binary_file,"r") as reader:
                for line in reader:
                    line=line.strip()
                    if line.startswith("111"):
                        comp_binary=line[3:10]
                        if comp_binary not in c_inst_tabel.values():
                            print(f"warning:unknown c binary code -{comp_binary}")     

                    



            
            


