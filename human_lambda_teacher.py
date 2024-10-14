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
  A minimally adequate teacher with a membership function, backed up by a humn
  '''
  def __init__(self, membership: Callable[[str], bool]):
    self.membership = membership
    self.human = HumanTeacher()

  def membership_query(self, string: str) -> bool:
    answer = self.membership(string)
    # print(f'[DEBUG] query: {string} -> {"accept" if answer else "reject"}')
    return answer

  def respond_to_conjecture(self, conjecture: Acceptor) -> Optional[str]:
    return self.human.respond_to_conjecture(conjecture)
