'''
HumanExamplesTeacher
'''

from typing import Optional
from teacher import Teacher
from acceptor import Acceptor
from human_teacher import HumanTeacher

class HumanExamplesTeacher(Teacher):
  '''
  A minimally adequate teacher with examples, backed up by a humn
  '''
  def __init__(self, P: set[str], N: set[str]):
    self.P: set[str] = set(P)
    self.N: set[str] = set(N)
    self.human = HumanTeacher()
    self.query_history: list[str] = []

  def membership_query(self, string: str) -> bool:
    self.query_history.append(string)
    if string in self.P:
      # print(f'[DEBUG] query: {string} -> accept')
      return True
    if string in self.N:
      # print(f'[DEBUG] query: {string} -> reject')
      return False
    answer = self.human.membership_query(string)
    if answer:
      self.P.add(string)
    else:
      self.N.add(string)
    return answer

  def respond_to_conjecture(self, conjecture: Acceptor) -> Optional[str]:
    # conjecture.print_acceptor()
    for n in self.N:
      if conjecture.accepts(n):
        # print(f'[DEBUG] conjecture rejected: failed to reject {n}')
        return n
    for p in self.P:
      if conjecture.rejects(p):
        # print(f'[DEBUG] conjecture rejected: failed to accept {p}')
        return p
    return self.human.respond_to_conjecture(conjecture)
