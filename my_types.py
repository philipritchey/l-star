'''
types
'''

Alphabet = str
Row = dict[str, bool]
State = int
Symbol = str
TransitionFunction = dict[tuple[Symbol, Symbol], State]

