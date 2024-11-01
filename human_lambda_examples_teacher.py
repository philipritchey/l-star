'''
HumanLambdaExamplesTeacher
'''

from collections.abc import Callable
from typing import Optional
from teacher import Teacher
from acceptor import Acceptor
from human_teacher import HumanTeacher

class HumanLambdaExamplesTeacher(Teacher):
  '''
  A minimally adequate teacher with a membership function and examples, backed up by a human
  '''
  def __init__(self, membership: Callable[[str], bool], positive_examples: set[str], negative_examples: set[str]):
    self.membership = membership
    self.positive_examples: set[str] = set(positive_examples)
    self.negative_examples: set[str] = set(negative_examples)
    self.human = HumanTeacher()
    self.query_history: list[str] = []

  def membership_query(self, string: str) -> bool:
    answer = self.membership(string)
    self.query_history.append(string)
    # print(f'[DEBUG] query: {string} -> {"accept" if answer else "reject"}')
    return answer

  def respond_to_conjecture(self, conjecture: Acceptor) -> Optional[str]:
    for n in self.negative_examples:
      if conjecture.accepts(n):
        print(f'[DEBUG] conjecture rejected: failed to reject {n}')
        return n
    for p in self.positive_examples:
      if conjecture.rejects(p):
        print(f'[DEBUG] conjecture rejected: failed to accept {p}')
        return p
    return self.human.respond_to_conjecture(conjecture)
