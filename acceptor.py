'''
acceptor.py
'''
from my_types import State
from helpers import compact
from brzozowski import brzozowski, opt, pretty

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

  def get_alphabet(self) -> str:
    '''
    get the input alphabet

    Returns:
        str: input alphabet
    '''
    alphabet_set = set()
    for state_str, _ in self.d.items():
      _, a = state_str
      alphabet_set.add(a)
    return str(''.join(sorted(alphabet_set)))

  def print_acceptor(self) -> None:
    '''
    print this DFA to standard output
    '''
    print('DFA')
    print('===')
    alphabet: str = self.get_alphabet()
    # TODO(pcr): map states to 1..n before printing
    states: list[int] = list(sorted(self.Q))
    i = states.index(self.q0)
    if i != 0:
      # make initial state at index 0
      states[0], states[i] = states[i], states[0]
    initial_state = 0
    accepting_states: set[int] = {states.index(state) for state in self.F}
    transition_function: dict[tuple[int, str], set[int]] = {}
    print('state |', end='')
    for a in alphabet:
      print(f'| {a} ', end='')
    print()
    print('------++---+---')
    for q in states:
      q_i = states.index(q)
      t = ''
      if q_i == initial_state:
        # initial state
        t += '->'
      else:
        t += '  '
      # print the _index_ of the state
      t += f'{q_i}'
      if q_i in accepting_states:
        # accepting state
        t += '*'
      print(f'{t:5s} |', end='')
      for a in alphabet:
        # next state (print the _index_)
        print(f'| {states.index(self.d[(q, a)])} ', end='')
        key = (q_i, a)
        if key not in transition_function:
          transition_function[key] = set()
        transition_function[key].add(states.index(self.d[(q, a)]))
      print()
    print('REGEX')
    print('=====')
    ans = brzozowski(
      len(states),
      alphabet,
      accepting_states,
      transition_function)
    print(pretty(opt(ans)))
