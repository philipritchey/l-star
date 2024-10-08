from my_types import Alphabet, State
from teacher import Teacher
from helpers import compact
from acceptor import Acceptor

Row = dict[str, bool]

class ObservationTable:
  '''
  information about a finite collection of strings over A,
  classfiying them as members or non-members of an unknown regular set
  '''
  def __init__(self, A: Alphabet):
    self.A = A
    self.S: set[str] = {'λ'}
    self.E: set[str] = {'λ'}
    self.T: dict[str, bool] = {}

  def init(self, teacher: Teacher) -> None:
    for symbol in f'λ{self.A}':
      self.T[symbol] = teacher.membership_query(symbol)

  def row(self, s: str) -> Row:
    '''
    the finite function f: E -> {0,1} defined by f(e) = T(s*e)
    '''
    r: Row = {}
    for e in self.E:
      t = compact(f'{s}{e}')
      if t in self.T:
        r[e] = self.T[t]
    return r

  def closed(self) -> bool:
    '''
    An observation table is called _closed_ provided that
      for each t in S*A there exists an s in S such that row(t) = row(s)

    Returns:
        bool: True iff table is closed
    '''
    for s in self.S:
      for a in self.A:
        t = compact(f'{s}{a}')
        # print(f'[DEBUG] {t=}')
        row_t = self.row(t)
        # print(f'[DEBUG] row({t}) = {row_t}')
        good = False
        for r in self.S:
          if row_t == self.row(r):
            good = True
            # print(f'[DEBUG] row({t}) = row({r})')
            break
        if not good:
          # print(f'[DEBUG] no s such that row({t}) = row(s)')
          return False
      return True
    # return all(any(row(t, table) == row(s, table) for s in table.S) for t in (compact(f'{s}{a}') for s in table.S for a in A))

  def consistent(self) -> bool:
    '''
    An observation table is called _consistent_ provided that
      whenever s1 and s2 are elements of S such that row(s1) = row(s2),
      for all a in A, row(s1*a) = row(s2*a)

    Returns:
        bool: True iff table is consistent
    '''
    for s1 in self.S:
      for s2 in self.S:
        if self.row(s1) == self.row(s2):
          if not all(self.row(compact(f'{s1}{a}')) == self.row(compact(f'{s2}{a}')) for a in self.A):
            return False
    return True

  def find_not_consistent(self) -> str:
    '''
    find s1, s2 in S, a in A, and e in E such that
      row(s1) = row(s2) and T(s1*a*e) != T(s2*a*e)

    Returns:
        str: ae that improves consistency

    '''
    for s1 in self.S:
      for s2 in self.S:
        if self.row(s1) == self.row(s2):
          for a in self.A:
            for e in self.E:
              t1 = compact(f'{s1}{a}{e}')
              t2 = compact(f'{s2}{a}{e}')
              if self.T[t1] != self.T[t2]:
                return compact(f'{a}{e}')
    raise ValueError('failed to find s1,s2,a,e to increase consistency')

  def find_not_closed(self) -> str:
    '''
    find s1 in S and a in A such that
      row(s1*a) is different from row(s) for all s in S

    Returns:
        str: s1, a that improves closure
    '''
    for s1 in self.S:
      for a in self.A:
        t = compact(f'{s1}{a}')
        r = self.row(t)
        if all(r != self.row(s) for s in self.S):
          return t
    raise ValueError('failed to find s1,a to increase closure')

  def add_to_S(self, s: str) -> None:
    if len(s) == 0:
      s = 'λ'
    self.S.add(s)

  def add_to_E(self, e: str) -> None:
    if len(e) == 0:
      e = 'λ'
    self.E.add(e)

  def extend(self, teacher: Teacher) -> None:
    '''
    extend T to (S U S*A) * E using membership queries for missing elements

    Args:
        teacher (Teacher): a minimally adequate teacher
    '''
    for u in self.S.union(set(compact(f'{s}{a}') for s in self.S for a in self.A)):
      for e in self.E:
        t = compact(f'{u}{e}')
        if t not in self.T:
          self.T[t] = teacher.membership_query(t)

  def to_acceptor(self) -> Acceptor:
    Q: set[State] = set()
    q0: State = -1
    F: set[State] = set()
    d: dict[(State, str), State] = {}

    list_e = list(self.E)
    for s in self.S:
      r = self.row(s)
      state = 0
      for e in list_e:
        state *= 2
        if r[e]:
          state += 1
      Q.add(state)
      if s == 'λ':
        q0 = state
      if self.T[s]:
        F.add(state)
      for a in self.A:
        r2 = self.row(f'{s}{a}')
        next_state = 0
        for e in list_e:
          next_state *= 2
          if r2[e]:
            next_state += 1
        d[(state, a)] = next_state
    return Acceptor(Q, q0, F, d)

  def print_table(self) -> None:
    '''
    An observation table can be visualized as a two-dimensional array with
    rows labelled by elements of (S U S*A) and columns labelled by elements
    of E, with the entry for row s and column e equal to T(s*e),
    '''
    print(f'A: {self.A}')
    print(f'S: {self.S}')
    print(f'E: {self.E}')
    width = max(len(t) for t in self.T)
    print(f' T{" "*(width-1)}', end='')
    for e in self.E:
      print(f' | {e}{" "*(5-len(e))}', end='')
    print()
    print('-'*(width+2+8*len(self.E)))
    v: set[str] = set()
    for s in self.S:
      print(f' {s}' + ' '*(width-len(s)), end ='')
      for e in self.E:
        t = compact(f'{s}{e}')
        if t in self.T:
          f = str(self.T[t])
          print(f' | {f}{" "*(5-len(f))}', end='')
          v.add(t)
        else:
          print(' |   ?  ', end='')
      print()
    print('-'*(width+2+8*len(self.E)))
    for t, f in self.T.items():
      if t not in v:
        print(f' {t}{" "*(width-len(t))} | {f}')
    print()
