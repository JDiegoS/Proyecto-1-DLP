from distutils.command.build import build
from AFN import AFN
from Node import Node
from Subconjuntos import Subconjuntos

class AFDe(object):
    def __init__(self, arr, alphabet):
        self.arr = arr
        self.arbol = [['state'], ['char'], ['c1'], ['c2'], ['anulable'], ['primerap'], ['ultimap']]
        self.nodes = []
        self.tableS = [['state'], ['char'], ['siguientep']]
        
        self.alphabet = alphabet
        self.state = 1
        self.operaciones = ['(', ')', '+', '|', '*', '.']
        self.tableT = [['posiciones'], ['estado']]
        for i in self.alphabet:
            self.tableT.append([i])
        self.newAccepted = []

    def siguientePosicion(self, op, n):
        if op == '*':
            cPrimerasPosiciones = self.arbol[5][n-1]
            for i in cPrimerasPosiciones:
                indx = self.tableS[0].index(i)
                for i in cPrimerasPosiciones:
                    self.tableS[2][indx].append(i)
        elif op == '.':
            
            c1UlltimaPosicion = self.arbol[6][n-2]
            c2PrimeraPosicion = self.arbol[5][n-1]
            if isinstance(c1UlltimaPosicion, int):
                indx = self.tableS[0].index(c1UlltimaPosicion)
                self.tableS[2][indx].append(c2PrimeraPosicion)
            else:
                for i in c1UlltimaPosicion:
                    indx = self.tableS[0].index(i)
                    self.tableS[2][indx] += [c2PrimeraPosicion]



    def addTreeChar(self, state, n, c1, c2, nullable, first, last):
        self.arbol[0].append(state)
        self.arbol[1].append(n)
        self.arbol[2].append(c1)
        self.arbol[3].append(c2)
        self.arbol[4].append(nullable)
        self.arbol[5].append(first)
        self.arbol[6].append(last)

    def addState(self, conj, state):
        # Agregar nuevo estado a la tabla
        self.tableT[0].append(conj)
        self.tableT[1].append('s'+str(state))

    def getNodes(self):
        # Genera los nodos del AFD
        num = 0
        for i in self.tableT[1]:
            if i[0] == 's':
                accepted = i in self.newAccepted
                self.nodes.append(Node(i, [], accepted))
                letter = 2
                for a in self.alphabet:
                    state = -1
                    for j in self.tableT[letter]:
                        if j == i:
                            self.nodes[num].transitions.append(['s'+str(state), a])
                        state+=1
                    letter += 1
                num += 1

    def generateAFD(self):
        # Aumentar expresion 
        self.arr.append('#')
        self.alphabet.append('#')
        position = 0
        iteracion = 0
        # Crear arbol
        for i in self.arr:
            keep = True
            if position == iteracion:
                if i == '#':
                    # Ultimo caracter
                    previous = self.arr[position - 1]
                    if self.arbol[4][-1]:
                        primerap = self.arbol[5][-1] + [self.state]
                    else:
                        primerap = self.arbol[5][-1]

                    
                    self.addTreeChar(self.state, i, '', '', False, self.state, self.state)
                    ultimap = self.arbol[6][-1]
                    self.addTreeChar('', '.', previous, i, False, primerap, ultimap)
                    self.state+=1
                elif i != '(' and i != ')':
                    if position > 0:
                        # Caracter previo
                        previous = self.arr[position - 1]
                    if position+1 < len(self.arr):
                        # Caracter que sigue
                        next = self.arr[position+1]

                    if position > 0 and next not in self.operaciones and previous != '|':
                        # Concatenacion con caracter previo
                        if previous != ')':
                            if self.arbol[4][-1]:
                                primerap = self.arbol[5][-1] + [self.state]
                            else:
                                primerap = self.arbol[5][-1]
                            self.addTreeChar(self.state, i, '', '', False, self.state, self.state)
                            ultimap = self.arbol[6][-1]
                            self.addTreeChar('', '.', previous, i, False, primerap, ultimap)
                            self.state+=1
                        elif i in self.operaciones:
                            if i == '*':
                                op = '*'
                            elif i == '+':
                                op = '+'
                            self.addTreeChar('', op, self.arbol[0][-1], '', True, self.arbol[5][-1], self.arbol[6][-1])
                        keep = False
                    
                    if i in self.alphabet and keep:
                        if next in self.alphabet:
                            # Concatenacion dos letras
                            self.addTreeChar(self.state, i, i, i, False, self.state, self.state)
                            self.addTreeChar(self.state+1, next, next, next, False, self.state+1, self.state+1)
                            self.addTreeChar('', '.', i, next, False, self.state, self.state+1)
                            position+=1
                            self.state += 2
                        elif next == '|' and self.arr[position+2] in self.alphabet:
                            # Or
                            self.addTreeChar(self.state, i, '', '', False, self.state, self.state)
                            self.addTreeChar(self.state+1, self.arr[position+2], '', '', False, self.state+1, self.state+1)
                            self.addTreeChar('', '|', i, self.arr[position+2], False, [self.state, self.state+1], [self.state, self.state+1])
                            self.state += 2
                            position+=3
                        elif next == '*':
                            # Kleene
                            self.addTreeChar(self.state, i, '', '', False, self.state, self.state)
                            self.addTreeChar('', '*', i, '', True, self.state, self.state)
                            self.state += 1
                            position+=1
                        elif next == '+':
                            # Positiva
                            self.addTreeChar(self.state, i, '', '', False, self.state, self.state)
                            self.addTreeChar('', '+', i, '', False, self.state+1, self.state+1)
                            self.state += 1
                            position+=1

                position += 1
            iteracion += 1

        # Funcion Siguiente Posicion
        index = 0
        for i in self.arbol[0]:
            if isinstance(i, int):
                self.tableS[0].append(i)
                self.tableS[1].append(self.arbol[1][index])
                self.tableS[2].append([])
            index+=1
        index = 0
        for i in self.arbol[1]:
            if i == '*':
                self.siguientePosicion('*', index)
            elif i == '.':
                self.siguientePosicion('.', index)
            index+=1
        
        # Tabla de transicion
        self.tableT[0].append(self.tableS[2][1])
        self.tableT[0][1].sort()
        self.tableT[1].append('s0')

        building = True
        state = 1
        self.alphabet.pop()
        currents = 1

        while building:

            letra = 2
            for i in self.alphabet:
                trans = []
                for j in self.tableT[0][currents]:
                    if self.tableS[1][j] == self.alphabet[letra-2]:
                        trans += self.tableS[2][j]
                trans.sort()

                if trans not in self.tableT[0]:
                    self.addState(trans, state)
                    self.tableT[letra].append('s'+str(state))
                    state+=1

                else:
                    # Agregar transicion
                    indx = self.tableT[0].index(trans)
                    self.tableT[letra].append('s'+str(indx-1))
                letra +=1
                
            currents +=1
            if len(self.tableT[0]) == len(self.tableT[-1]):
                # Se lleno la tabla
                building = False

        acceptedIndex = self.tableS[1].index('#')
        newI = 0
        for i in self.tableT[0]:
            if newI > 0:
                if acceptedIndex in i:
                    self.newAccepted.append(self.tableT[1][newI])
            newI+=1


        self.getNodes()

        return self.nodes



                