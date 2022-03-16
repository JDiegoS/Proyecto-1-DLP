# Juan Diego Solorzano 18151
# Proyecto 1 Automatas

from PySimpleAutomata import automata_IO
import os
import json

class Node(object):
    def __init__(self, state, transitions, accepted):
        self.state = state
        #self.previous = previous
        self.transitions = transitions
        self.accepted = accepted

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

expresion = input("\nIngrese la expresion regular: ")
print("Entendido! Generando automatas...")

# Identificar alfabeto
operaciones = ['(', ')', '+', '|', '*']

arr = list(expresion)
alphabet = []
for i in arr:
    if i not in operaciones and i not in alphabet:
        alphabet.append(i)

# Crear nodos
nodes = []
nodes.append(Node(0, [], False))
state = 1
position = 1
accepted = False
for i in arr:
    if i in alphabet:
        if position == len(arr):
            accepted = True
        else:
            next = arr[position]
            if next in operaciones:
                if next == '|' and arr[position+1] in alphabet:
                    nodes.append(Node(state, [[state-1, 'epsilon']], accepted))
                    nodes.append(Node(state + 1, [[state, arr[position-1]]], accepted))

                    nodes.append(Node(state + 2, [[state-1, 'epsilon']], accepted))
                    nodes.append(Node(state + 3, [[state+2, arr[position+1]]], accepted))

                    nodes.append(Node(state + 4, [[state+1, 'epsilon'], [state+3, 'epsilon']], accepted))
                    state += 5
            else:      
                nodes.append(Node(state, [[state-1, i]], accepted))
                state += 1
    position+=1
        
graph = {
    "alphabet": alphabet,
    "states": [],
    "initial_states": "0",
    "accepting_states": [],
    "transitions": [],
}
for i in nodes:
    graph['states'].append(str(i.state))
    if i.accepted == True:
        graph['accepting_states'].append(str(i.state))
    for t in i.transitions:
        graph['transitions'].append([t[0], t[1], str(i.state)])

with open('digraph.json', 'w') as outfile:
    json.dump(graph, outfile)
dfa_example = automata_IO.nfa_json_importer('./digraph.json')
automata_IO.nfa_to_dot(dfa_example, 'resultado', './')