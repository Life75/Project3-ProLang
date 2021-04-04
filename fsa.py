import sys
#TODO PARSE ARGUMENTS FOR FILEREADING INPUT AT THE END 
import tkinter
import time
from tkinter import *
from tkinter import ttk


fileName = sys.argv[1]
stringFileName = sys.argv[2]

print(fileName)
print(stringFileName)
class FmaData:
    def __init__(self, amountOfStates, alphabet, stateTransisitions, startState, acceptStates):
        self.amountOfStates = amountOfStates.strip()
        self.alphabet = alphabet.strip()
        self.stateTransisitions = stateTransisitions.strip()
        self.startState = startState.strip()
        self.acceptStates = acceptStates.strip()
    
    def getAmountOfStates(self):
        return self.amountOfStates

    def getAlphabet(self):
        alphaList = self.alphabet.split(',')
        return alphaList
    
    def getStateTransitions(self):
        transitionsList = self.stateTransisitions.split(',')
        return transitionsList

    def getStartState(self):
        return self.startState

    def getAcceptState(self):
        acceptStateList = self.acceptStates.split(',')
        return acceptStateList

class Parser:
    def __init__(self, fileName):
        self.fileName = fileName

    def parseData(self):
        currentFile = open(self.fileName,"r+")
        data = currentFile.readline()

        parserList = data.split(';')
        return parserList
    


        

#Parse the data and create the different transitions states with thier connected pathways 
parser = Parser(fileName)
parserList = parser.parseData() 

fmaData = FmaData(parserList[0], parserList[1], parserList[2], parserList[3],  parserList[4])

#setting up window 
root=Tk()
myCanvas = tkinter.Canvas(root, bg="white", height=900, width=900)
scroll = Scrollbar(root, orient='vertical')
scroll.pack(side= RIGHT, fill = Y)



class Transition:
    def __init__(self, transition):
        self.transition = transition
        holder = []
        for i in transition: 
            if i.isalpha() or i.isdigit():
                holder.append(i)
            
        self.start = holder[0]
        self.finish = holder[1]
        self.key = holder[2]

    def getStart(self):
        return self.start
    def getFinish(self):
        return self.finish
    def getKey(self):
        return self.key

class State: 
    def __init__(self, stateID):
        self.state = stateID
        self.transitions = []
    def getState(self):
        return self.state
    def placeTransition(self, transition):
        start = transition.getStart()
        if int(start) == self.state:
            self.transitions.append(transition)
    def getTransitions(self):
        return self.transitions
    def setCoordinates(self, x1, x2, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def getCoordinates(self):
        self.coordinates = [self.x1, self.y1, self.x2, self.y2]
        return self.coordinates
    def setID(self, ID):
        self.ID = ID
    def getID(self):
        return self.ID
    
        



#takes in all the transitions from the txt and returns a list of those transitions data types for extraction later by the function when the State classes are set up
def createTransitions(transitionsList):
    holder =[]
    for transition in transitionsList:
        data = Transition(transition)
        holder.append(data)
    return holder

def createStatesList(amountOfStates):
    stateList =[]
    i =0
    while (i < int(amountOfStates)):
        state = State(i)
        stateList.append(state)
        i+=1    
    return stateList


def placingData(transitionsList, stateList):
    for state in stateList:
        for transition in transitionsList:
            state.placeTransition(transition)
    return stateList



transitionsList = createTransitions(fmaData.getStateTransitions())
stateList = createStatesList(fmaData.getAmountOfStates())
stateList = placingData(transitionsList, stateList)


class DisplayFma:
    def __init__(self):
        self.amountOfCircles = fmaData.getAmountOfStates()

    def displayCircles(self):
        i =0
        x1 = 100+25
        y1 = 120+50
        x2 = 200
        y2 = 250
        offset = 150

        myCanvas.pack()
      
        amount = int(self.amountOfCircles)
        self.hiddenCircles = []
        while i < amount:
            circleID = myCanvas.create_oval(x1+30, y1, x2+30, y2, outline='#fff')

            self.hiddenCircles.append(circleID)
            circleID = myCanvas.create_oval(x1, y1, x2, y2, fill="#fff")
            stateList[i].setID(circleID)

            
            for acceptState in fmaData.getAcceptState():
                if i == int(acceptState):
                    myCanvas.create_oval(x1+10,y1+15,x2-10,y2-12)

            myCanvas.create_text(x1+32, y1+40, anchor=W, font="pursia", text=str(i))
            stateList[i].setCoordinates(x1, y1, x2, y2)
            
            y1 += offset
            y2 += offset
            i += 1
    
    def displayTransitions(self):
        currentState =0
        for state in stateList:
            transit = state.getTransitions()
            currentState += 1 

            currentCoordinates = state.getCoordinates()
            for transition in transit:


                start = int(transition.getStart())
                finish = int(transition.getFinish())

                #drawing a straight line for transition
                if start == finish-1:
                    myCanvas.create_line(currentCoordinates[0]+38,currentCoordinates[3], currentCoordinates[0]+38, currentCoordinates[3]+75, arrow=LAST)
                    key = transition.getKey()
                    myCanvas.create_text(currentCoordinates[0]+50, currentCoordinates[3]+20, anchor=W, font="pursia", text=str(key))                    
            
                #looping into itself 
                if start == finish:
                    myCanvas.itemconfigure(self.hiddenCircles[state.getState()], outline="#000000") #unhides the circles if they go into each other
                    key = transition.getKey()
                    myCanvas.create_text(currentCoordinates[0]+120, currentCoordinates[3]-50, anchor=W, font="pursia", text=str(key))


                #if transition is going backwards 
                diff = finish - start 
                if start > finish or diff > 1:
                    myCanvas.create_line(currentCoordinates[0], currentCoordinates[3]-30, currentCoordinates[0]-50, currentCoordinates[3]-30) #horiztonal from the start
                    endingState = stateList[finish]
                    endingCoordinates = endingState.getCoordinates()
                    myCanvas.create_line(currentCoordinates[0]-50, currentCoordinates[3]-30, currentCoordinates[0]-50, endingCoordinates[2]+30) #line goes to the length of wherever its destination is

                    #create the line that goes down from given line 
                    myCanvas.create_line(endingCoordinates[0], endingCoordinates[3]-50, endingCoordinates[0]-50, endingCoordinates[3]-50, arrow=FIRST )
                    #create the key 
                    key = transition.getKey()
                    myCanvas.create_text(endingCoordinates[0]-20, endingCoordinates[3], anchor=W, font="pursia", text=str(key))

                
    def startStateDisplay(self):
        state = stateList[int(fmaData.getStartState())]
        currentCoordinates = state.getCoordinates()
        myCanvas.create_line(currentCoordinates[0], currentCoordinates[3]-50, currentCoordinates[0]-40, currentCoordinates[3]-100, arrow=FIRST)

    

               
               
                    
def checkIfLegalValue(element):
    for value in fmaData.getAlphabet():
        if value == element:
            return True
    return False

def checkLegalTransistors(currentState, element):
    transitions = currentState.getTransitions()

    for path in transitions:
        if(path.getKey() == element):
            nextState = int(path.getFinish())
            return nextState
    return -1

def checkLegalAcceptState(currentState):
    
    for acceptState in fmaData.getAcceptState():
        if int(currentState.getState()) == int(acceptState):
            return True
    return False   

def stateActiveColor(currentState):
    myCanvas.itemconfigure(currentState.getID(), outline="#ffa500") 
    myCanvas.update()
    time.sleep(.5)
    myCanvas.itemconfigure(currentState.getID(), outline="#000000") 
    myCanvas.update()





def fmaLogic(fileName):
    fmaLogicParser = Parser(fileName)
    string = fmaLogicParser.parseData()

    currentState = stateList[int(fmaData.getStartState())]
    for i, element in enumerate(string[0]):
        if checkIfLegalValue(element):
            stateActiveColor(currentState) 
            nextState = checkLegalTransistors(currentState, element)
            #TODO change colors depending on the different tranisitions of states as if its going through the fma
            if nextState != -1:
                currentState =  stateList[nextState]
            else:
                return False
    if  checkLegalAcceptState(currentState):
        stateActiveColor(currentState)
        return True
    else:
        return False

display = DisplayFma()
display.displayCircles()
display.displayTransitions()
display.startStateDisplay()
if fmaLogic(stringFileName):
    print("legal statement")
else:
    print("illegal statement")



root.mainloop()


  