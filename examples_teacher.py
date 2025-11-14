'''
ExamplesTeacher
'''

from typing import Optional
from teacher import Teacher
from acceptor import Acceptor
from human_teacher import HumanTeacher

class ExamplesTeacher(Teacher):
  '''
  A teacher with examples
  '''
  def __init__(self, examples: dict[str, set[str]]):
    self.positives: set[str] = examples['P']
    self.negatives: set[str] = examples['N']
    self._query_history: list[str] = []
    self.human = HumanTeacher()

  def membership_query(self, string: str) -> bool:
    self._query_history.append(string)
    if string in self.positives:
      print(f'[DEBUG] query: {string} -> accept')
      return True
    if string in self.negatives:
      print(f'[DEBUG] query: {string} -> reject')
      return False
    # not in the examples -> don't know -> {yes, no, random, ask a human}
    # answer = choice((True, False))
    # ask a human to indicate that the example set is inadequate
    answer = self.human.membership_query(string)
    if answer:
      self.positives.add(string)
    else:
      self.negatives.add(string)
    return answer

  def respond_to_conjecture(self, conjecture: Acceptor) -> Optional[str]:
    # conjecture.print_acceptor()
    for n in self.negatives:
      if conjecture.accepts(n):
        print(f'[DEBUG] conjecture rejected: failed to reject {n}')
        return n
    for p in self.positives:
      if conjecture.rejects(p):
        print(f'[DEBUG] conjecture rejected: failed to accept {p}')
        return p
    # accepts all p in P, rejects all n in N -> "correct"
    return None  # None -> no counterexample -> "correct"

  def query_history(self) -> list[str]:
    return self._query_history
