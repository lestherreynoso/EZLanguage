__author__ = 'root'

from Tkinter import *
import ttk
from tkFileDialog import asksaveasfilename, askopenfilename

def parrot(*args):
    print codeEditText.get('1.0', 'end')

def openFile():
    openFilePath = askopenfilename(defaultextension=".ezl", filetypes=mask)
    openf = open(openFilePath, 'r')
    codeEditText.insert('1.0', openf.read())
    print openFilePath

def saveFile():
    saveFilePath = asksaveasfilename(defaultextension=".ezl", filetypes=mask)
    save = open(saveFilePath, 'w')
    save.truncate()
    save.write(codeEditText.get('1.0', 'end'))
    print saveFilePath

def assemble():
    getInstructions()
    print "assemble"


def forwardingUnit():
    pass


def isNumber(param):
    try:
        float(param)
        return True
    except ValueError:
        return False


def verifyFormat(instrComponents):
    if (len(instrComponents) == 3 and isNumber(instrComponents[2]))\
            or (len(instrComponents) == 4):
        return True
    else:
        return False


def instructionExists(instr):
    return InstructionSet.has_key(instr)


def getInstrBinary(instr):
    return InstructionSet.get(instr)


def getRegisterBinary(register):
    return RegisterSet.get(register)


def getTypeI(instrComponents):
    instrucBinary = getInstrBinary(instrComponents[0]) + \
                    getRegisterBinary(instrComponents[1]) + \
                    getRegisterBinary(instrComponents[2]) + \
                    getRegisterBinary(instrComponents[3])
    return instrucBinary


def getImmediateBinary(immed):
    return '{0:08b}'.format(int(immed))


def getTypeII(instrComponents):
    instrucBinary = getInstrBinary(instrComponents[0]) + \
                getRegisterBinary(instrComponents[1]) + \
                getImmediateBinary(instrComponents[2])
    return instrucBinary


def generateInstruction(instrComponents):
    if len(instrComponents) == 3:
        Instruction =getTypeII(instrComponents)
    elif len(instrComponents) == 4:
        Instruction =getTypeI(instrComponents)
    return Instruction

def getInstructions():
    linesOfCode = codeEditText.get('1.0', 'end')
    listOfLines = linesOfCode.split("\n")

    for x in listOfLines:
        x = x.lower()
        if len(x) > 0:
            x = x.replace(",", "")
            instrComponents = x.split(" ")
            print instrComponents
            instr = instrComponents[0]
            if instructionExists(instr):
                if verifyFormat(instrComponents):
                     print generateInstruction(instrComponents)
                else:
                    print "'" + x + "' is not properly formatted"
                    break
            else:
                print instr + " does not exists"
                break


def run():
    # verifyFormat()
    print "run"

# List of instructions
instructionsList = ["load", "store", "+", "-", "*", "/", "b=", "bn=", "b>", "b<", "j", "sll", "slr", "move"]
# for x in instructionsList:
#     print '{0:04b}'.format(instructionsList.index(x)), x    # method for getting the corresponding binary

InstructionSet = {
    "load": "0000",
    "store": "0001",
    "+": "0010",
    "-": "0011",
    "*": "0100",
    "/": "0101",
    "b=": "0110",
    "bn=": "0111",
    "b>": "1000",
    "b<": "1001",
    "j": "1010",
    "sll": "1011",
    "slr": "1100",
    "move": "1101"
    }

RegisterSet = {
    "r1": "0000",
    "r2": "0001",
    "r3": "0010",
    "r4": "0011",
    "r5": "0100",
    "r6": "0101",
    "r7": "0110",
    "r8": "0111",
    "r9": "1000",
    "r10": "1001"
}
# for k in InstructionSet.keys():
#     print k + " : " + InstructionSet.get(k)

mask = [("EZL files","*.ezl"),
    ("Text files","*.txt"),
    ("All files","*.*")]

window = Tk()
window.title("EZL IDE")

content = ttk.Frame(window, padding="12 12 12 12")
content.grid(column=0, row=0, sticky=(N, W, E, S))
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)

codeEditLabel = StringVar()
codeEditLabel.set("Enter Code Here")

ttk.Button(content, text="Save", command=saveFile).grid(column=1, row=1, sticky=W)
ttk.Button(content, text="Open", command=openFile).grid(column=2, row=1, sticky=W)
ttk.Button(content, text="Assemble", command=assemble).grid(column=3, row=1, sticky=W)
ttk.Button(content, text="Run", command=run).grid(column=4, row=1, sticky=W)

ttk.Label(content, textvariable=codeEditLabel).grid(column=1, columnspan=4, row=2, sticky=(W, E))


codeEditText = Text(content, width=40, height=10)
codeEditText.grid(column=1, row=3, columnspan=4, rowspan=11, sticky=(W, E))
ttk.Label(content, text="Memory ").grid(column=1, row=13, columnspan=4, sticky=(W, E))


# ttk.Button(content, text="Repeat", command=parrot).grid(column=5, row=3, sticky=W)

ttk.Label(content, text="r1").grid(column=7, row=2, sticky=(W, E))
ttk.Label(content, text="r2").grid(column=7, row=3, sticky=(W, E))
ttk.Label(content, text="r3").grid(column=7, row=4, sticky=(W, E))
ttk.Label(content, text="r4").grid(column=7, row=5, sticky=(W, E))
ttk.Label(content, text="r5").grid(column=7, row=6, sticky=(W, E))
ttk.Label(content, text="r6").grid(column=7, row=7, sticky=(W, E))
ttk.Label(content, text="r7").grid(column=7, row=8, sticky=(W, E))
ttk.Label(content, text="r8").grid(column=7, row=9, sticky=(W, E))
ttk.Label(content, text="r9").grid(column=7, row=10, sticky=(W, E))
ttk.Label(content, text="r10").grid(column=7, row=11, sticky=(W, E))

r1 = StringVar()
r2 = StringVar()
r3 = StringVar()
r4 = StringVar()
r5 = StringVar()
r6 = StringVar()
r7 = StringVar()
r8 = StringVar()
r9 = StringVar()
r10 = StringVar()

r1.set("0")
r2.set("0")
r3.set("0")
r4.set("0")
r5.set("0")
r6.set("0")
r7.set("0")
r8.set("0")
r9.set("0")
r10.set("0")

ttk.Label(content, textvariable=r1).grid(column=8, row=2, sticky=(W, E))
ttk.Label(content, textvariable=r2).grid(column=8, row=3, sticky=(W, E))
ttk.Label(content, textvariable=r3).grid(column=8, row=4, sticky=(W, E))
ttk.Label(content, textvariable=r4).grid(column=8, row=5, sticky=(W, E))
ttk.Label(content, textvariable=r5).grid(column=8, row=6, sticky=(W, E))
ttk.Label(content, textvariable=r6).grid(column=8, row=7, sticky=(W, E))
ttk.Label(content, textvariable=r7).grid(column=8, row=8, sticky=(W, E))
ttk.Label(content, textvariable=r8).grid(column=8, row=9, sticky=(W, E))
ttk.Label(content, textvariable=r9).grid(column=8, row=10, sticky=(W, E))
ttk.Label(content, textvariable=r10).grid(column=8, row=11, sticky=(W, E))
content.bind('<Return>', parrot)




window.mainloop()