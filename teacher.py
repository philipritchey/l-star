'''
Teacher
'''

from typing import Optional
from abc import ABC, abstractmethod
from acceptor import Acceptor

class Teacher(ABC):
  '''
  Abstract base class for minimally adequate teachers
  '''
  @abstractmethod
  def membership_query(self, string: str) -> bool:
    '''
    ask the teacher whether the given string is in the language

    Args:
        string (str): string in question

    Returns:
        bool: _description_
    '''

  @abstractmethod
  def respond_to_conjecture(self, conjecture: Acceptor) -> Optional[str]:
    '''
    ask the teacher to verify a conjectured acceptor

    Args:
        conjecture (Acceptor): the acceptor in question

    Returns:
        Optional[str]: a counterexample if the conjecture is incorrect or None otherwise
    '''
