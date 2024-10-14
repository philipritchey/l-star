'''
acceptor.py
'''
from my_types import State
from helpers import compact

class Acceptor:
  '''
  a DFA
  '''
  def __init__(self, Q: set[State], q0: State, F: set[State], d: dict[(State, str), State]):
    self.Q = Q
    self.q0 = q0
    self.F = F
    self.d = d

  def accepts(self, string: str) -> bool:
    '''
    runs the acceptor on the string to test for acceptance

    Args:
        string (str): string to test

    Returns:
        bool: True iff this DFA accepts the string
    '''
    q = self.q0
    for a in compact(string):
      if a != 'λ':
        if (q,a) not in self.d:
          # transition doesn't exist -> reject
          return False
        q = self.d[(q,a)]
    return q in self.F

  def rejects(self, string: str) -> bool:
    '''
    runs the acceptor on the string to test for rejection

    Args:
        string (str): string to test

    Returns:
        bool: True iff this DFA does NOT accept the string
    '''
    return not self.accepts(string)

  def print_acceptor(self) -> None:
    '''
    print this DFA to standard output
    '''
    alphabet = set()
    for t, _ in self.d.items():
      _, a = t
      alphabet.add(a)
    print('state |', end='')
    for a in alphabet:
      print(f'| {a} ', end='')
    print()
    print('------++---+---')
    for q in self.Q:
      t = ''
      if q == self.q0:
        # initial state
        t += '->'
      else:
        t += '  '
      t += f'{q}'
      if q in self.F:
        # accepting state
        t += '*'
      print(f'{t:5s} |', end='')
      for a in alphabet:
        # next state
        print(f'| {self.d[(q, a)]} ', end='')
      print()
