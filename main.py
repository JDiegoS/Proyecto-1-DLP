# Juan Diego Solorzano 18151
# Proyecto 1 Automatas

from PySimpleAutomata import automata_IO
import os
import json
from Node import Node
from AFN import AFN
from Subconjuntos import Subconjuntos

os.environ["PATH"] += os.pathsep + 'C:/Program Files/graphviz/bin'

expresion = input("\nIngrese la expresion regular: ")
print("Analizando expresion...")

# Identificar alfabeto
operaciones = ['(', ')', '+', '|', '*']

arr = list(expresion)
alphabet = []
for i in arr:
    if i not in operaciones and i not in alphabet:
        alphabet.append(i)


# Construir AFN
print("Generando AFN (Thompson)...")

afn = AFN(arr, alphabet)
afn_nodes = afn.generateAFN()
graph = {
    "alphabet": alphabet,
    "states": [],
    "initial_states": "0",
    "accepting_states": [],
    "transitions": [],
}
for i in afn_nodes:
    if i.state not in graph['states']:
        graph['states'].append(str(i.state))
        if i.accepted == True:
            graph['accepting_states'].append(str(i.state))
        for t in i.transitions:
            graph['transitions'].append([str(t[0]), t[1], str(i.state)])

with open('digraph.json', 'w') as outfile:
    json.dump(graph, outfile)
dfa_example = automata_IO.nfa_json_importer('./digraph.json')
automata_IO.nfa_to_dot(dfa_example, 'thompsonAFN', './')

print("Generando AFD (Construccion de subconjuntos)...")
afd_sub = Subconjuntos(graph['states'], graph['transitions'], alphabet, graph['accepting_states'])
afd_snodes = afd_sub.generateAFD()
graph = {
    "alphabet": alphabet,
    "states": [],
    "initial_state": "s0",
    "accepting_states": [],
    "transitions": [],
}
for i in afd_snodes:
    if i.state not in graph['states']:
        graph['states'].append(str(i.state))
        if i.accepted == True:
            graph['accepting_states'].append(str(i.state))
        for t in i.transitions:
            graph['transitions'].append([str(t[0]), t[1], str(i.state)])

with open('digraph2.json', 'w') as outfile:
    json.dump(graph, outfile)
dfa_example = automata_IO.dfa_json_importer('./digraph2.json')
automata_IO.dfa_to_dot(dfa_example, 'subconjuntosAFD', './')

print("Generando AFD desde expresion regular...")
