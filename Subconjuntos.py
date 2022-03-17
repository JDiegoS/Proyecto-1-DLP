from tkinter import N
from AFN import AFN
from Node import Node

class Subconjuntos(object):
    def __init__(self, states, transitions, alphabet, accepted):
        self.states = states
        self.transitions = transitions
        self.alphabet = alphabet
        self.table = [['Conjunto de estados'],['Estado del AFD']]
        self.state = 0
        self.accepted = accepted
        self.newAccepted = []
        self.nodes = []
        for i in alphabet:
            self.table.append([i])

    def cerraduraEpsilon(self, states):
        conjunto = []
        for s in states:
            if s not in conjunto:
                conjunto.append(s)
        for i in self.transitions:
            if i[2] not in conjunto and i[0] in states and i[1] == 'epsilon':
                conjunto.append(i[2])        
        return conjunto

    def mover(self, states, value):
        conjunto = []
        for i in self.transitions:
            if i[2] not in conjunto and i[0] in states and i[1] == value:
                conjunto.append(i[2])        
        return conjunto

    def addState(self, conj):
        self.table[0].append(conj)
        self.table[1].append('s'+str(self.state))

    def getNodes(self):
        num = 0
        #print(self.newAccepted)
        for i in self.table[1]:
            if i[0] == 's':
                accepted = i in self.newAccepted
                self.nodes.append(Node(i, [], accepted))
                letter = 2
                for a in self.alphabet:
                    state = -1
                    for j in self.table[letter]:
                        if j == i:
                            self.nodes[num].transitions.append(['s'+str(state), a])
                        state+=1
                    letter += 1
                num += 1

    def generateAFD(self):
        building = True
        currentC = '0'
        cIndex = 1
        while building:
            conj = self.cerraduraEpsilon(currentC)
            searching = True
            while searching:
                nConjunto = self.cerraduraEpsilon(conj)
                if nConjunto == conj:
                    searching = False
                else:
                    conj = nConjunto
            conj.sort()
            if conj not in self.table[0]:
                self.addState(conj)
                for i in self.accepted:
                    if i in conj:
                        self.newAccepted.append('s'+str(self.state))
                self.state += 1
            nChar = 2
            for i in self.alphabet:
                trans = self.mover(conj, i)
                trans.sort()

                conj2 = self.cerraduraEpsilon(trans)
                searching = True
                while searching:
                    nConjunto = self.cerraduraEpsilon(conj2)
                    if nConjunto == conj2:
                        searching = False
                    else:
                        conj2 = nConjunto
                conj2.sort()
                if conj2 not in self.table[0]:
                    self.addState(conj2)
                    self.table[nChar].append('s'+str(self.state))
                    for i in self.accepted:
                        if i in conj2:
                            self.newAccepted.append('s'+str(self.state))
                    self.state += 1
                else:
                    indx = self.table[0].index(conj2)
                    self.table[nChar].append('s'+str(indx-1))
                nChar += 1
            cIndex += 1
            if len(self.table[0]) == len(self.table[-1]):
                building = False
            else:
                currentC = self.table[0][cIndex]
  
        self.getNodes()
        #print(self.table)

        return self.nodes

