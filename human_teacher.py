'''
HumanTeacher
'''

from typing import Optional
from teacher import Teacher
from acceptor import Acceptor

class HumanTeacher(Teacher):
  '''
  A minimally adequate human teacher
  '''
  def __init__(self):
    self._query_history: list[str] = []

  def membership_query(self, string: str) -> bool:
    response = input(f'(y/n) is {string} in the language? ')
    self._query_history.append(string)
    return response.lower()[0] == 'y'

  def respond_to_conjecture(self, conjecture: Acceptor) -> Optional[str]:
    conjecture.print_acceptor()
    response = input('(y/n) is this acceptor correct? ')
    counterexample = None
    if response.lower()[0] != 'y':
      counterexample = input('give me a counterexample: ')
    return counterexample
  
  def query_history(self) -> list[str]:
    return self._query_history
  
