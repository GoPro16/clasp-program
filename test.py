from tkinter import *
from Attribute import Attribute
from Constraint import Constraint
from Solution import Solution
import itertools
import os


def doNothing():
    print("Nothing to see here.")


"""
class MyButtons:

    def __init__(self,master):
        frame = Frame(master, width=600, height=400)
        frame.pack()

        self.printButton = Button(frame, text="Print Msg",command=self.printMessage)
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(frame,text="Quit", command=frame.quit)
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print("This is a message")
        
btns = MyButtons(root)
"""
"""
root = Tk()

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New Project...", command=doNothing)
subMenu.add_command(label="New...", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=menu.quit)

editMenu = Menu(menu)
menu.add_cascade(label="Edit",menu=editMenu)
editMenu.add_command(label="Undo", command=doNothing)

# Tool bar
toolbar = Frame(root,bg="blue",width=500,height=500)
insertButton = Button(toolbar,text="Insert",fg="green",command=doNothing)
insertButton.pack(side=LEFT,padx=2,pady=2)
printButton = Button(toolbar,text="Print",fg="green",command=doNothing)
printButton.pack(side=LEFT,padx=2,pady=2)

# Status bar
status = Label(root,text="Preparing to do nothing...", bd=1,relief=SUNKEN,anchor=W)
status.pack(side=BOTTOM,fill=X)

toolbar.pack(side=TOP, fill=X)


root.mainloop()
"""

attributeList = {}
constraintsList = []
preferencesList = []
filename = "attributes"

lines = tuple(open(filename, 'r'))

for index, line in enumerate(lines):
    attribute = Attribute(
        name=line.split(':')[0].strip(),
        index=index + 1,
        value=line.split(':')[1].split(',')[0].strip(),
        inverseValue=line.split(':')[1].split(',')[1].strip()
    )
    attributeList[attribute.value] = attribute
    attributeList[attribute.inverseValue] = attribute

filename = "constraints"
lines = tuple(open(filename, 'r'))
for index, line in enumerate(lines):
    tempLines = line.split(" ")
    for i in range(len(tempLines)):
        if tempLines[i] == "NOT":
            attribute = attributeList[(tempLines[i + 1].strip())]
            tempLines[i + 1] = attribute.getInverseAsIndex(value=tempLines[i + 1].strip())

    # Remove all NOT values now that we have inverted
    constraintsList.append(filter(lambda a: a != "NOT" and a != "OR", tempLines))

    # Now we have to construct all possible outcomes for the indicies
file = open("try.cnf", "w+")
file.write("p cnf " + str(len(attributeList) / 2) + " " + str(len(constraintsList) + len(attributeList) / 2) + "\n")
for constraint in constraintsList:
    file.write(str(constraint[0]) + " " + str(constraint[1]) + " " + str(0) + "\n")
file.close()


def getAttrFromIndex(list,index):
    for item in list:
        if(abs(index) == Attribute.getIndex(list[item])):
            if(index > 0):
                return Attribute.getValue(list[item])
            else:
                return Attribute.getInverseValue(list[item])


# Now we are done writing. Call clasp and review
lst =  filter(lambda b: b[0] == 'v',filter(lambda a: a != '' ,os.popen("clasp try.cnf -n 0").read().split("\n")))
solutionlist = []
for possibleSolution in lst:
    tempArr = filter(lambda a: a != 'v' and a != '0',possibleSolution.split(' '))
    for index,attr in enumerate(tempArr):
        tempArr[index] = getAttrFromIndex(attributeList,int(attr))
    sol = Solution(array=tempArr)
    solutionlist.append(sol)
    # print tempArr
# print lst

# Get the preferences
filename = "preferences"
lines = tuple(open(filename, 'r'))
for index, line in enumerate(lines):
    preference = line.split(",")[0]
    penalty = int(line.split(",")[1].strip())
    isAnd = True if preference.split(" ")[1] == "AND" else False
    for index,solution in enumerate(solutionlist):
        # Check and update solutions with penalties
        solutionlist[index] = Solution.checkAndUpdatePenalty(solution,penalty=penalty,isAnd=isAnd,leftValue=preference.split(" ")[0],rightValue=preference.split(" ")[2])
    # print tempLines

solutionlist.sort(key=lambda x: Solution.getPenalty(x))
for solution in solutionlist:
    print solution


# print attributeList["soup"]

# print call(["clasp","try1.cnf"])
