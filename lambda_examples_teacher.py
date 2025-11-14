'''
LambdaExamplesTeacher
'''

from collections.abc import Callable
from typing import Optional
from teacher import Teacher
from acceptor import Acceptor

class LambdaExamplesTeacher(Teacher):
  '''
  A teacher with a membership function and examples that accepts the first conjecture
  '''
  def __init__(self, membership: Callable[[str], bool], examples: dict[str, set[str]]):
    self.membership = membership
    self.positive_examples: set[str] = examples['P']
    self.negative_examples: set[str] = examples['N']
    self._query_history: list[str] = []

  def membership_query(self, string: str) -> bool:
    answer = self.membership(string)
    self._query_history.append(string)
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
    # accept
    return None
  
  def query_history(self) -> list[str]:
    return self._query_history
