'''
LambdaTeacher
'''

from collections.abc import Callable
from typing import Optional
from teacher import Teacher
from acceptor import Acceptor

class LambdaTeacher(Teacher):
  '''
  A teacher with a membership function that accepts the first conjecture
  '''
  def __init__(self, membership: Callable[[str], bool]):
    self.membership = membership
    self._query_history: list[str] = []

  def membership_query(self, string: str) -> bool:
    answer = self.membership(string)
    self._query_history.append(string)
    # print(f'[DEBUG] query: {string} -> {"accept" if answer else "reject"}')
    return answer

  def respond_to_conjecture(self, conjecture: Acceptor) -> Optional[str]:
    return None
  
  def query_history(self) -> list[str]:
    return self._query_history
