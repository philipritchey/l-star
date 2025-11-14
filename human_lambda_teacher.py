'''
HumanLambdaTeacher
'''

from collections.abc import Callable
from typing import Optional
from teacher import Teacher
from acceptor import Acceptor
from human_teacher import HumanTeacher

class HumanLambdaTeacher(Teacher):
  '''
  A minimally adequate teacher with a membership function, backed up by a human
  '''
  def __init__(self, membership: Callable[[str], bool]):
    self.membership = membership
    self.human = HumanTeacher()
    self._query_history: list[str] = []

  def membership_query(self, string: str) -> bool:
    answer = self.membership(string)
    self._query_history.append(string)
    # print(f'[DEBUG] query: {string} -> {"accept" if answer else "reject"}')
    return answer

  def respond_to_conjecture(self, conjecture: Acceptor) -> Optional[str]:
    return self.human.respond_to_conjecture(conjecture)

  def query_history(self) -> list[str]:
    return self._query_history