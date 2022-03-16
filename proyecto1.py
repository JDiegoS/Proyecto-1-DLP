# Juan Diego Solorzano 18151
# Proyecto 1 Automatas

from PySimpleAutomata import automata_IO
import os
import json
from Node import Node
from AFN import AFN

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



afn = AFN(arr, alphabet)
nodes = afn.generateAFN()
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