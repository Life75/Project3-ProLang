import sys
#TODO PARSE ARGUMENTS FOR FILEREADING INPUT AT THE END 
import tkinter
from tkinter import *
from tkinter import ttk



class FmaData:
    def __init__(self, amountOfStates, alphabet, stateTransisitions, startState, acceptStates):
        self.amountOfStates = amountOfStates
        self.alphabet = alphabet
        self.stateTransisitions = stateTransisitions
        self.startState = startState
        self.acceptStates = acceptStates
    
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
        print(self.fileName)
        currentFile = open(self.fileName,"r+")
        data = currentFile.readline()

        parserList = data.split(';')
        return parserList
        #print(parserList[1])
    


        

#Parse the data and create the different transitions states with thier connected pathways 
parser = Parser('test.txt')
parserList = parser.parseData() 

fmaData = FmaData(parserList[0], parserList[1], parserList[2], parserList[3],  parserList[4])

#print(fmaData.getAmountOfStates())
#print(fmaData.getAlphabet())
#print(fmaData.getStateTransitions())
#print(fmaData.getStartState())
#print(fmaData.getAcceptState())
#setting up window 
root=Tk()
myCanvas = tkinter.Canvas(root, bg="white", height=900, width=900)


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
        #TODO make a list to hold the transitions that pertain to this state
        #print(transition.getStart())
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
            #print("here")
            state.placeTransition(transition)
    return stateList



transitionsList = createTransitions(fmaData.getStateTransitions())
stateList = createStatesList(fmaData.getAmountOfStates())
stateList = placingData(transitionsList, stateList)

#checking the values to make sure they're all there 
#for state in stateList:
#    for transition in state.getTransitions():
#        print(str(transition.getStart()) + " State:" + str(state.getState()) +" "+ str(transition.getFinish()))





class DisplayFma:
    def __init__(self):
        self.amountOfCircles = fmaData.getAmountOfStates()
        #displayCircles()

    def displayCircles(self):
        i =0
        x1 = 100+25
        y1 = 120+50
        x2 = 200
        y2 = 250
        offset = 150

        myCanvas.pack()
       # myCanvas.create_oval(x1, y1, 200, 100)
       # myCanvas.create_oval(x1, y1+150, 200, 250)
       # myCanvas.create_oval(x1, y1+150+150, 200, 250+150)
        amount = int(self.amountOfCircles)
        self.hiddenCircles = []
        while i < amount:
            circleID = myCanvas.create_oval(x1+30, y1, x2+30, y2, outline='#fff')
           # print(str(circleID)+ "here")
            self.hiddenCircles.append(circleID)
            myCanvas.create_oval(x1, y1, x2, y2, fill="#fff")
            myCanvas.create_text(x1+32, y1+40, anchor=W, font="pursia", text=str(i))
            stateList[i].setCoordinates(x1, y1, x2, y2)
            
            y1 += offset
            y2 += offset
            i += 1
    
    def displayTransitions(self):
        #TODO display whatever transition lines 
        currentState =0
        for state in stateList:
            transit = state.getTransitions()
            currentState += 1 
            #print(state.getState())

            currentCoordinates = state.getCoordinates()
            print(currentCoordinates)
            for transition in transit:


                start = int(transition.getStart())
                finish = int(transition.getFinish())

                #drawing a straight line for transition
                if start == finish-1:
                    myCanvas.create_line(currentCoordinates[0]+38,currentCoordinates[3], currentCoordinates[0]+38, currentCoordinates[3]+75, arrow=LAST)
                    print(state.getState())
                    myCanvas.itemconfigure(self.hiddenCircles[state.getState()], outline="#000000") #unhides the circles if they go into each other

                #looping into itself 
                #if start == finish:
                    #myCanvas.create_arc(currentCoordinates[0], currentCoordinates[1], currentCoordinates[2]-150, currentCoordinates[3], style="arc")
                    

                    


        

        
    
    #def displayCircles():

display = DisplayFma()
display.displayCircles()
display.displayTransitions()

root.mainloop()


  