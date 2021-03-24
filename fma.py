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

print(fmaData.getAmountOfStates())
print(fmaData.getAlphabet())
print(fmaData.getStateTransitions())
print(fmaData.getStartState())
print(fmaData.getAcceptState())
#setting up window 
root=Tk()
myCanvas = tkinter.Canvas(root, bg="white", height=300, width=300)
myCanvas.create_oval(15, 25, 200, 25)
myCanvas.pack(fill=BOTH, expand=True)





class DisplayFma:
    def __init__(self):
        self.amountOfCircles = fmaData.getAmountOfStates

       # ttk.Button(root,text="Hello Universe").grid()        
        

        
    
    #def displayCircles():


display = DisplayFma()

root.mainloop()


  