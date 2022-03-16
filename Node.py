class Node(object):
    def __init__(self, state, transitions, accepted):
        self.state = state
        #self.previous = previous
        self.transitions = transitions
        self.accepted = accepted