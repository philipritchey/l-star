'''
acceptor.py
'''
from my_types import State
from helpers import compact
from brzozowski import brzozowski, opt

class Acceptor:
  '''
  a DFA
  '''
  def __init__(self, Q: set[State], q0: State, F: set[State], d: dict[tuple[State, str], State]):
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
    print('DFA')
    print('===')
    alphabet_set = set()
    for state_str, _ in self.d.items():
      _, a = state_str
      alphabet_set.add(a)
    alphabet = str(''.join(sorted(alphabet_set)))
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
    print('REGEX')
    print('=====')
    ans = brzozowski(
      len(self.Q),
      alphabet,
      self.F,
      self.d)
    print(opt(ans).pretty())
