from Node import Node
class AFN(object):
    # Clase para construir AFN

    def __init__(self, arr, alphabet):
        self.arr = arr
        self.nodes = []
        self.alphabet = alphabet
        self.state = 1
        self.operaciones = ['(', ')', '+', '|', '*']
        self.lastOpenP = 0
        self.lastCloseP = 0

    def changeState(self, state):
        self.state = state

    def orOp(self, state, position, accepted):
        self.nodes.append(Node(str(state), [[str(state-1), 'epsilon']], False))
        self.nodes.append(Node(str(state+1), [[str(state), self.arr[position-1]]], False))

        self.nodes.append(Node(str(state+2), [[str(state-1), 'epsilon']], False))
        self.nodes.append(Node(str(state+3), [[str(state+2), self.arr[position+1]]], False))

        self.nodes.append(Node(str(state+4), [[str(state+1), 'epsilon'], [state+3, 'epsilon']], accepted))

    def concatOp(self, state, accepted, i):
        self.nodes.append(Node(str(state), [[str(state-1), i]], accepted))

    def kleeneOp(self, first):
        for i in self.nodes:
            if i.state == first:
                i.transitions.append([str(self.nodes[-1].state), 'epsilon'])

        self.nodes[-1].transitions.append([str(first), 'epsilon'])
        
    def parenthesisOp(self, state, position, accepted):
        operacionP = []
        searching = True
        fKleene = False
        start = state-1
        while searching and position <= len(self.arr):
            if self.arr[position] == ')':
                if position+1 == len(self.arr):
                    accepted = True
                elif self.arr[position+1] == '*':
                    if position+2 == len(self.arr):
                        accepted = True
                    fKleene = True
                searching = False
                self.lastCloseP = position - 1
            else:
                operacionP.append(self.arr[position])
            position += 1
        if searching == True:
            print('No se encontro el final del parentesis')
            return
        tempAFN = AFN(operacionP, self.alphabet)
        tempAFN.changeState(self.state)
        pNodes = tempAFN.generateAFN()
        pNodes[-1].accepted = accepted
        for j in pNodes:
            self.nodes.append(j)
        if fKleene:
            self.kleeneOp(start)

    def generateAFN(self):
        # Crear nodos
        position = 1
        accepted = False
        self.nodes.append(Node(0, [], False))
        for i in self.arr:
            if i in self.alphabet:
                # Es el ultimo char?
                if position == len(self.arr):
                    accepted = True
                    if self.arr[position-2] != '|':
                        self.concatOp(self.state, accepted, i)
                else:
                    # Siguiente posicion
                    next = self.arr[position]
                    if next in self.operaciones:
                        # Or
                        if next == '|' and self.arr[position+1] in self.alphabet:
                            if position+2 == len(self.arr):
                                accepted = True
                            self.orOp(self.state, position, accepted)
                            self.state += 5
                        # Seguido por paretnesis
                        elif next == '(' and self.arr[position-2] != '|':
                            self.concatOp(self.state, accepted, i)
                            self.state += 1
                        elif next == '*':
                            if position+1 == len(self.arr):
                                accepted = True
                            self.concatOp(self.state, accepted, i)
                            self.kleeneOp(self.state-1)
                            self.state += 1
                    elif self.arr[position-2] != '|': 
                        # Concatenacion     
                        self.concatOp(self.state, accepted, i)
                        self.state += 1
            elif i == '(' and self.arr[position] in self.alphabet:
                # Parentesis
                self.lastOpenP = position-1
                self.parenthesisOp(self.state, position, accepted)
            position += 1
        #Regresar nodos generados
        return self.nodes