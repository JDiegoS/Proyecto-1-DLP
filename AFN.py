from Node import Node
class AFN(object):
    # Clase para construir AFN

    def __init__(self, arr, alphabet):
        self.arr = arr
        self.nodes = []
        self.alphabet = alphabet
        self.state = 1
        self.operaciones = ['(', ')', '+', '|', '*']

    def changeState(self, state):
        self.state = state

    def orOp(self, state, position, accepted):
        self.nodes.append(Node(str(state), [[str(state-1), 'epsilon']], False))

        self.nodes.append(Node(str(state+1), [[str(state), 'epsilon']], False))
        self.nodes.append(Node(str(state+2), [[str(state+1), self.arr[position-1]]], False))

        self.nodes.append(Node(str(state+3), [[str(state), 'epsilon']], False))
        self.nodes.append(Node(str(state+4), [[str(state+3), self.arr[position+1]]], False))

        self.nodes.append(Node(str(state+5), [[str(state+2), 'epsilon'], [state+4, 'epsilon']], False))
        self.nodes.append(Node(str(state+6), [[str(state+5), 'epsilon']], accepted))

    def concatOp(self, state, accepted, i):
        self.nodes.append(Node(str(state), [[str(state-1), i]], accepted))

    def kleeneOp(self, first):
        for i in self.nodes:
            if i.state == str(first) or i.state == first:
                i.transitions.append([str(self.nodes[-2].state), 'epsilon'])

        self.nodes[-1].transitions.append([str(first-1), 'epsilon'])
    
    def positiveOp(self, first):
        for i in self.nodes:
            if i.state == str(first) or i.state == first:
                i.transitions.append([str(self.nodes[-2].state), 'epsilon'])
        
    def parenthesisOp(self, state, position, accepted):
        operacionP = []
        searching = True
        fKleene = False
        fPositive = False
        start = state
        while searching and position <= len(self.arr):
            if self.arr[position] == ')':
                if position+1 == len(self.arr):
                    accepted = True
                elif self.arr[position+1] == '*':
                    if position+2 == len(self.arr):
                        accepted = True
                    fKleene = True
                elif self.arr[position+1] == '+':
                    if position+2 == len(self.arr):
                        accepted = True
                    fPositive = True
                searching = False

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
        elif fPositive:
            self.positiveOp(start)

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
                        # Seguido por Or
                        if next == '|' and self.arr[position+1] in self.alphabet:
                            if position+2 == len(self.arr):
                                accepted = True
                            self.orOp(self.state, position, accepted)
                            self.state += 7
                        # Seguido por paretnesis
                        elif next == '(' and self.arr[position-2] != '|':
                            self.concatOp(self.state, accepted, i)
                            self.state += 1
                        # Seguido por Kleene
                        elif next == '*':
                            self.nodes.append(Node(str(self.state), [[str(self.state-1), 'epsilon']], False))
                            if position+1 == len(self.arr):
                                accepted = True
                            self.concatOp(self.state+1, False, i)
                            self.nodes.append(Node(str(self.state+2), [[str(self.state+1), 'epsilon']], accepted))
                            self.kleeneOp(self.state)
                            self.state += 3
                        # Seguido por positiva
                        elif next == '+':
                            self.nodes.append(Node(str(self.state), [[str(self.state-1), 'epsilon']], False))
                            if position+1 == len(self.arr):
                                accepted = True
                            self.concatOp(self.state+1, False, i)
                            self.nodes.append(Node(str(self.state+2), [[str(self.state+1), 'epsilon']], accepted))
                            self.positiveOp(self.state)
                            self.state += 1
                    # Concatenacion 
                    elif self.arr[position-2] != '|': 
                        self.concatOp(self.state, accepted, i)
                        self.state += 1
            # Parentesis
            elif i == '(' and self.arr[position] in self.alphabet:
                self.parenthesisOp(self.state, position, accepted)
            elif i not in self.operaciones:
                print('Hay un error en la expresion (' + i + ')')
                break
            position += 1
        #Regresar nodos generados
        return self.nodes