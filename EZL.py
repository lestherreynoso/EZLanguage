__author__ = 'root'

from Tkinter import *
import ttk
from tkFileDialog import asksaveasfilename, askopenfilename

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


def findHazards():
    tabs = StringVar()
    stalls = StringVar()
    tabs.set("")
    stalls.set("")
    pipeline.set("")
    linesOfCode = codeEditText.get('1.0', 'end')
    listOfLines = linesOfCode.split("\n")
    listOfLines = filter(None, listOfLines)

    #check for data hazards
    for instruction in Program:
        stalls.set("")
        if Program.index(instruction) == 0:
            pipeline.set("FD\tEXM\tWB\n")
            tabs.set("\t")
        s = instruction.split()
        if len(s) == 3 and Program.index(instruction) != 0: #type two check and make sure its not the first instruction
            # print Program[Program.index(instruction)-1].split()[1]
            #check a type two instruction destination is not yet written by a type one or type two instruction before it
            if s[1] == Program[Program.index(instruction)-1].split()[1]: #checks type two instruction against previous type one or type two instruction
                messages.set(messages.get() + "\nData Hazard between '" + listOfLines[Program.index(instruction)-1]+"' and '" +  listOfLines[Program.index(instruction)] + "'" )
                stalls.set(stalls.get() + "S\t")
                check = pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n"
                # pipeline.set(pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n")
                # if checkStructuralHazards(check):
                #     print "structural hazards"
                #     stalls.set(stalls.get() + "S\t")
                #     messages.set(messages.get() + "\nStructural Hazard between '" + listOfLines[Program.index(instruction)-1]+"' and '" +  listOfLines[Program.index(instruction)] + "'" )

                check = pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n"
                pipeline.set(check)
                tabs.set(tabs.get() + "\t\t")
                # print "type two hazard " + stalls.get()

            else:
                # print "type two no hazard" + stalls.get()
                check = pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n"
                # if checkStructuralHazards(check):
                #     print "structural hazards"
                    # stalls.set(stalls.get() + "S\t")
                    # messages.set(messages.get() + "\nStructural Hazard between '" + listOfLines[Program.index(instruction)-1]+"' and '" +  listOfLines[Program.index(instruction)] + "'" )

                check = pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n"
                pipeline.set(check)
                tabs.set(tabs.get() + "\t")
        elif len(s) == 4 and Program.index(instruction) != 0: #type one instruction check
            #check if a type one instrcution sources are not yet written by a previous type two  or type one instruction
            if s[2] == Program[Program.index(instruction)-1].split()[1] or s[3] == Program[Program.index(instruction)-1].split()[1]: # checks type one instruction following a type two
                # print "type one hazard" + stalls.get()

                messages.set(messages.get() + "\nData Hazard between '" + listOfLines[Program.index(instruction)-1]+"' and '" +  listOfLines[Program.index(instruction)] + "'" )
                stalls.set(stalls.get() + "S\t")
                check = pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n"
                # pipeline.set(pipeline.get() + tabs.get() + "S\tFD\tEXM\tWB\n")

                # if checkStructuralHazards(check):
                #     print "structural hazards"
                #
                #     # stalls.set(stalls.get() + "S\t")
                #     messages.set(messages.get() + "\nStructural Hazard between '" + listOfLines[Program.index(instruction)-1]+"' and '" +  listOfLines[Program.index(instruction)] + "'" )

                check = pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n"
                pipeline.set(check)
                tabs.set(tabs.get() + "\t\t")
            else:
                # print "type one no hazard" + stalls.get()
                check = pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n"
                # if checkStructuralHazards(check):
                #     print "structural hazards"
                #     # stalls.set(stalls.get() + "S\t")
                #     messages.set(messages.get() + "\nStructural Hazard between '" + listOfLines[Program.index(instruction)-1]+"' and '" +  listOfLines[Program.index(instruction)] + "'" )

                check = pipeline.get() + tabs.get() + stalls.get() + "FD\tEXM\tWB\n"
                pipeline.set(check)
                tabs.set(tabs.get() + "\t")


def checkStructuralHazards(chk):
    # check for structural hazards
    # break apart the pipeline
    match = False
    pipelineLines = chk.replace("\t", " /t ").split("\n") #sumalate the tabs since \t isnt read as a string element
    for line in pipelineLines:
        line.strip(" ")
        if pipelineLines.index(line) !=0:
            p = line.split() #split the lines into the individual stages
            # print p
            for stage in p:
                if stage != "S" and stage != "/t": # no need to check these
                    print str(p.index(stage)) + " and " + str(len(pipelineLines[pipelineLines.index(line)-1].split()))
                    print stage
                    if not int(p.index(stage)) < len(pipelineLines[pipelineLines.index(line)-1].split()):
                        print "prev too short"
                    if p.index(stage) < len(pipelineLines[pipelineLines.index(line)-1].split()) and stage == pipelineLines[pipelineLines.index(line)-1].split()[p.index(stage)+ 1]:
                        print "true " + stage + " = " + pipelineLines[pipelineLines.index(line)-1].split()[p.index(stage)+ 1]
                        match = True
                        break
    return match

def assemble():
    global assembled
    global entry
    if entry != codeEditText.get('1.0', 'end'):
        assembled = False
    if not assembled :
        getInstructions()
        findHazards()
        assembled = True
    else:
        messages.set(messages.get() + "\nProgram has already been assembled")
    # print "assemble"


def forwardingUnit():
    pass


def isNumber(param):
    try:
        float(param)
        return True
    except ValueError:
        return False


def verifyFormat(instrComponents):
    if instrComponents[0] == "j" and len(instrComponents) == 2:
        return True
    elif (len(instrComponents) == 3 and isNumber(instrComponents[2]))\
            or (len(instrComponents) == 4):
        return True
    elif len(instrComponents) == 3:
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
    if instrComponents[0] == "j":
        instrucBinary = getInstrBinary(instrComponents[0]) + " 1111 1111 1111"
    elif  instrComponents[0] == "b=" or instrComponents[0] == "bn=" or instrComponents[0] == "b>" or instrComponents[0] == "b<":
        instrucBinary = getInstrBinary(instrComponents[0]) + " " +\
                        getRegisterBinary(instrComponents[1]) + " " +\
                        getRegisterBinary(instrComponents[2]) + " 1111"
    else:
        instrucBinary = getInstrBinary(instrComponents[0]) + " " +\
                        getRegisterBinary(instrComponents[1]) + " " +\
                        getRegisterBinary(instrComponents[2]) + " " +\
                        getRegisterBinary(instrComponents[3])
    return instrucBinary


def getImmediateBinary(immed):
    return '{0:08b}'.format(int(immed))


def getTypeII(instrComponents):
    if instrComponents[0] != "move":
        instrucBinary = getInstrBinary(instrComponents[0]) + " " +\
                    getRegisterBinary(instrComponents[1]) + " " +\
                    getImmediateBinary(instrComponents[2])
    else:
        instrucBinary = getInstrBinary(instrComponents[0]) + " " +\
                    getRegisterBinary(instrComponents[1]) + " " +\
                    getRegisterBinary(instrComponents[2]) + " 0000"
    return instrucBinary


def generateInstruction(instrComponents):
    if len(instrComponents) == 2:
        Instruction = getTypeI(instrComponents)
    elif len(instrComponents) == 3:
        Instruction =getTypeII(instrComponents)
    elif len(instrComponents) == 4:
        Instruction =getTypeI(instrComponents)
    return Instruction

def getInstructions():
    global entry
    global entryLines
    global Labels

    instructions.set("")
    linesOfCode = codeEditText.get('1.0', 'end')
    entry = linesOfCode
    linesOfCode = linesOfCode.replace(":", ":\n")
    listOfLines = linesOfCode.split("\n")

    for lineOfInstruction in listOfLines:

        lineOfInstruction = lineOfInstruction.lower()
        if len(lineOfInstruction) > 0:
            if lineOfInstruction.find(":") != -1:
                labelArray = lineOfInstruction.split(":")
                Labels.append(labelArray[0])
            else:
                entryLines.append(lineOfInstruction)
                lineOfInstruction = lineOfInstruction.replace(",", "")
                instrComponents = lineOfInstruction.split(" ")
                print instrComponents
                instr = instrComponents[0]
                if instructionExists(instr):
                    if verifyFormat(instrComponents):
                        if isBranch(instrComponents):
                            pass
                        Program.append(generateInstruction(instrComponents))
                        instructions.set(instructions.get() + generateInstruction(instrComponents) + "\t" + lineOfInstruction + "\n")
                    else:
                        messages.set(messages.get() + "\n'" + lineOfInstruction + "' is not properly formatted")
                        # print "'" + lineOfInstruction + "' is not properly formatted"
                        break
                else:
                    messages.set(messages.get() + "\n" + instr + " does not exists")
                    # print instr + " does not exists"
                    break


def isBranch(inst):
    if inst[0] == "b=" or inst[0] == "bn=" or inst[0] == "b>" or inst[0] == "b<" or inst[0] == "j":
        return True;

def getReg(r):
    global r1, r2, r3, r4, r5, r6, r7, r8, r9, r10
    if r == "r1":
        return r1.get()
    elif r == "r2":
        return r2.get()
    elif r == "r3":
        return r3.get()
    elif r == "r4":
        return r4.get()
    elif r == "r5":
        return r5.get()
    elif r == "r6":
        return r6.get()
    elif r == "r7":
        return r7.get()
    elif r == "r8":
        return r8.get()
    elif r == "r9":
        return r9.get()
    elif r == "r10":
        return r10.get()

def setReg(r, val):
    global r1, r2, r3, r4, r5, r6, r7, r8, r9, r10
    if r == "r1":
        r1.set(val)
    elif r == "r2":
        r2.set(val)
    elif r == "r3":
        r3.set(val)
    elif r == "r4":
        r4.set(val)
    elif r == "r5":
        r5.set(val)
    elif r == "r6":
        r6.set(val)
    elif r == "r7":
        r7.set(val)
    elif r == "r8":
        r8.set(val)
    elif r == "r9":
        r9.set(val)
    elif r == "r10":
        r10.set(val)

def findReg(guess):
    for register, binary in RegisterSet.items():
        if binary == guess:
            return register

def processInstruction(instruction):
    global entryLines
    global entry
    processed = instruction.split()

    #instruction fetch
    for name, binary in InstructionSet.items():
        if binary == processed[0]:
            #instruction decode
            i = name

    if i == "load":
        print "loading"
        r = findReg(processed[1])
        setReg(r, str(int(processed[2], 2)))
        # reg = getReg(r)

    elif i == "store":
        print "storing"
        r = findReg(processed[1])
        setReg(r, str(int(processed[2], 2)))

    elif i == "+":
        print "adding"
        des = findReg(processed[1])
        s1 = findReg(processed[2])
        s2 = findReg(processed[3])
        setReg(des, str(int(getReg(s1)) + int(getReg(s2))))

    elif i == "-":
        print "subtracting"
        des = findReg(processed[1])
        s1 = findReg(processed[2])
        s2 = findReg(processed[3])
        setReg(des, str(int(getReg(s1)) - int(getReg(s2))))

    elif i == "*":
        print "multiplication"
        des = findReg(processed[1])
        s1 = findReg(processed[2])
        s2 = findReg(processed[3])
        setReg(des, str(int(getReg(s1)) * int(getReg(s2))))

    elif i == "/":
        print "division"
        des = findReg(processed[1])
        s1 = findReg(processed[2])
        s2 = findReg(processed[3])
        setReg(des, str(int(getReg(s1)) / int(getReg(s2))))

    elif i == "b=":
        if getReg(findReg(processed[1])) == getReg(findReg(processed[2])):
            print instruction
            print entryLines
            entry = entry.lower()
            entry = entry.replace(":", ":\n")
            el = entry.split("\n")
            for thing in el:
                if thing.find(i +  findReg(processed[1]) + ", " + findReg(processed[2])+ ", ") != 0:
                    thing = thing.replace(",", "")
                    ell = thing.split(" ")
                    # print "ell = "
                    # print ell
                    if Labels.index(ell[3]) == -1:
                        messages.set(messages.get() + "\nThe label'" + ell[3] +"' does not exists")
                    else:
                        for labelsearch in el:
                            # print "looking for label search in the list of liens"
                            # print labelsearch
                            if labelsearch == ell[3]+":":
                                runOneCount = el.index(labelsearch) + 1#label position
                                print runOneCount
                                l = runOneCount
                                while el[l] == "":
                                    l = l+1
                                print el[l]
                                branchTo(el[l])
                                break
                        break

        #     Program.index(instruction)
        #     branchTo(processed[3])
    elif i == "bn=":
        if getReg(findReg(processed[1])) != getReg(findReg(processed[2])):
            print instruction
            print entryLines
            entry = entry.lower()
            entry = entry.replace(":", ":\n")
            el = entry.split("\n")
            for thing in el:
                if thing.find(i +  findReg(processed[1]) + ", " + findReg(processed[2])+ ", ") != 0:
                    thing = thing.replace(",", "")
                    ell = thing.split(" ")
                    # print "ell = "
                    # print ell
                    if Labels.index(ell[3]) == -1:
                        messages.set(messages.get() + "\nThe label'" + ell[3] +"' does not exists")
                    else:
                        for labelsearch in el:
                            # print "looking for label search in the list of liens"
                            # print labelsearch
                            if labelsearch == ell[3]+":":
                                runOneCount = el.index(labelsearch) + 1#label position
                                print runOneCount
                                l = runOneCount
                                while el[l] == "":
                                    l = l+1
                                print el[l]
                                branchTo(el[l])
                                break
                        break
    elif i == "b>":
        if getReg(findReg(processed[1])) > getReg(findReg(processed[2])):
            print instruction
            print entryLines
            entry = entry.lower()
            entry = entry.replace(":", ":\n")
            el = entry.split("\n")
            for thing in el:
                if thing.find(i +  findReg(processed[1]) + ", " + findReg(processed[2])+ ", ") != 0:
                    thing = thing.replace(",", "")
                    ell = thing.split(" ")
                    # print "ell = "
                    # print ell
                    if Labels.index(ell[3]) == -1:
                        messages.set(messages.get() + "\nThe label'" + ell[3] +"' does not exists")
                    else:
                        for labelsearch in el:
                            # print "looking for label search in the list of liens"
                            # print labelsearch
                            if labelsearch == ell[3]+":":
                                runOneCount = el.index(labelsearch) + 1#label position
                                print runOneCount
                                l = runOneCount
                                while el[l] == "":
                                    l = l+1
                                print el[l]
                                branchTo(el[l])
                                break
                        break
    elif i == "b<":
        if getReg(findReg(processed[1])) < getReg(findReg(processed[2])):
            print instruction
            print entryLines
            entry = entry.lower()
            entry = entry.replace(":", ":\n")
            el = entry.split("\n")
            for thing in el:
                if thing.find(i +  findReg(processed[1]) + ", " + findReg(processed[2])+ ", ") != 0:
                    thing = thing.replace(",", "")
                    ell = thing.split(" ")
                    # print "ell = "
                    # print ell
                    if Labels.index(ell[3]) == -1:
                        messages.set(messages.get() + "\nThe label'" + ell[3] +"' does not exists")
                    else:
                        for labelsearch in el:
                            # print "looking for label search in the list of liens"
                            # print labelsearch
                            if labelsearch == ell[3]+":":
                                runOneCount = el.index(labelsearch) + 1#label position
                                print runOneCount
                                l = runOneCount
                                while el[l] == "":
                                    l = l+1
                                print el[l]
                                branchTo(el[l])
                                break
                        break
    elif i == "j":
        # print instruction
        # print entryLines
        print i
        entry = entry.lower()
        entry = entry.replace(":", ":\n")
        el = entry.split("\n")
        for thing in el:
            if thing.find("j ") == 0:
                ell = thing.split(" ")
                print "ell = "
                print ell
                if Labels.index(ell[1]) == -1:
                    messages.set(messages.get() + "\nThe label'" + ell[1] +"' does not exists")
                else:
                    for labelsearch in el:
                        # print "looking for label search in the list of liens"
                        # print labelsearch
                        if labelsearch == ell[1]+":":
                            runOneCount = el.index(labelsearch) + 1#label position + 1 makes it the next line
                            print runOneCount
                            l = runOneCount
                            while el[l] == "":
                                l = l+1
                            print el[l]
                            branchTo(el[l])
                            break
                    break
    elif i == "sll":
        r = findReg(processed[1])
        e = getReg(r)
        # print e
        i = 0
        zeros = ""
        while i != int(processed[2], 2):
            zeros = zeros + "0"
            i= i+1
        bin = "{0:08b}".format(int(e))
        print bin
        after = bin + zeros
        print "after is " + str(int(after, 2))
        # af = "{0:08b}".format(str(int(after, 2)))
        # print af
        setReg(r, str(int(after, 2)))
    elif i == "slr":
        r = findReg(processed[1])
        e = getReg(r)
        # print e
        i = 0
        zeros = ""
        while i != int(processed[2], 2):
            zeros = zeros + "0"
            i= i+1
        bin = "{0:08b}".format(int(e))
        print bin
        after = zeros + bin
        print "after is " + str(int(after, 2))
        # af = "{0:08b}".format(str(int(after, 2)))
        # print af
        setReg(r, str(int(after, 2)))
    elif i == "move":
        print "moving"
        setReg(findReg(processed[2]), getReg(findReg(processed[1])))

def branchTo(b):
    global runOneCount
    b = b.replace(",", "")
    runOneCount = Program.index(generateInstruction(b.split(" "))) -1
    # runOne()

def run():
    # verifyFormat()
    if len(Program) == 0:
        messages.set(messages.get() + "\nYou have not assembled anything")
        print "You have not assembled anything"
    else:
        print Program
        while runOneCount != len(Program):
            runOne()
        # for instruction in Program:
        #     processInstruction(instruction)
    print "run"

def runOne():
    global runOneCount
    runOneCount += 1
    # verifyFormat()
    if len(Program) == 0:
        messages.set(messages.get() + "\nYou have not assembled anything")
        print "You have not assembled anything"
    elif runOneCount < len(Program):
        instruction = Program[runOneCount]
        processInstruction(instruction)
    # print "runOne"

# List of instructions
# instructionsList = ["load", "store", "+", "-", "*", "/", "b=", "bn=", "b>", "b<", "j", "sll", "slr", "move"]
# for x in instructionsList:
#     print '{0:04b}'.format(instructionsList.index(x)), x    # method for getting the corresponding binary

Program = []
Labels = []
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

runOneCount = -1

mask = [("EZL files","*.ezl"),
    ("Text files","*.txt"),
    ("All files","*.*")]
assembled = False

window = Tk()
window.title("EZL IDE")

entry = StringVar()
entryLines = []
messages = StringVar()
messages.set("Information: \n")
instructions = StringVar()
instructions.set("")
pipeline = StringVar()
pipeline.set("")
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
ttk.Button(content, text="Run one", command=runOne).grid(column=5, row=1, sticky=W)

ttk.Label(content, textvariable=codeEditLabel).grid(column=1, columnspan=4, row=2, sticky=(W, E))


codeEditText = Text(content, width=40, height=10)
codeEditText.grid(column=1, row=3, columnspan=5, rowspan=11, sticky=(W, E))

ttk.Label(content, textvariable=messages).grid(column=1, row=14, rowspan = 15, columnspan=8, sticky=(W, E))
ttk.Label(content, text="Instructions").grid(column=7, row=14, sticky=(W, E))
ttk.Label(content, text="Pipeline").grid(column=16, row=14, sticky=(W, E))

ttk.Label(content, textvariable=instructions).grid(column=7, row=15, columnspan=8, sticky=(W, E))
ttk.Label(content, textvariable=pipeline).grid(column=16, row=15, columnspan=8, sticky=(W, E))


# ttk.Button(content, text="Repeat", command=parrot).grid(column=5, row=3, sticky=W)

ttk.Label(content, text="r1").grid(column=7, row=2, sticky=(W, E), padx=5)
ttk.Label(content, text="r2").grid(column=7, row=3, sticky=(W, E), padx=5)
ttk.Label(content, text="r3").grid(column=7, row=4, sticky=(W, E), padx=5)
ttk.Label(content, text="r4").grid(column=7, row=5, sticky=(W, E), padx=5)
ttk.Label(content, text="r5").grid(column=7, row=6, sticky=(W, E), padx=5)
ttk.Label(content, text="r6").grid(column=7, row=7, sticky=(W, E), padx=5)
ttk.Label(content, text="r7").grid(column=7, row=8, sticky=(W, E), padx=5)
ttk.Label(content, text="r8").grid(column=7, row=9, sticky=(W, E), padx=5)
ttk.Label(content, text="r9").grid(column=7, row=10, sticky=(W, E), padx=5)
ttk.Label(content, text="r10").grid(column=7, row=11, sticky=(W, E), padx=5)

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

ttk.Label(content, textvariable=r1).grid(column=8, row=2, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r2).grid(column=8, row=3, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r3).grid(column=8, row=4, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r4).grid(column=8, row=5, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r5).grid(column=8, row=6, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r6).grid(column=8, row=7, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r7).grid(column=8, row=8, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r8).grid(column=8, row=9, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r9).grid(column=8, row=10, sticky=(W, E), padx=5)
ttk.Label(content, textvariable=r10).grid(column=8, row=11, sticky=(W, E), padx=5)

window.mainloop()