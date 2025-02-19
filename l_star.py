'''
The Learner L*
from Learning Regular Sets from Queries and Counterexamples
by Dana Angluin
'''

from sys import argv
from teacher import Teacher
from human_teacher import HumanTeacher
from my_types import Alphabet
from obervation_table import ObservationTable
from acceptor import Acceptor
from helpers import prefixes

def l_star(A: Alphabet, teacher: Teacher) -> Acceptor:
  '''
  learn a regular language
  '''

  # construct the initial obervation table (S,E,T)
  #   (T is a finite function mapping (S U S*A) * E) to {0,1})
  # initialize S and E to {λ}
  table = ObservationTable(A)

  # ask membership queries for λ and each a in A
  table.init(teacher)
  # print(f'[DEBUG] table.T = {table.T}')

  # repeat until Teacher replies yes to conjecture m
  M = None
  while M is None:
    # table.print_table()
    is_closed = table.closed()
    is_consistent = table.consistent()
    while not is_closed or not is_consistent:
      if not is_consistent:
        # print('[INFO] is NOT consistent')
        # find s1, s2 in S, a in A, and e in E such that
        #   row(s1) = row(s2) and T(s1*a*e) != T(s2*a*e)
        ae = table.find_not_consistent()
        # add ae to E
        # print(f'add {ae} to E')
        table.add_to_E(ae)
        # extend T to (S U S*A) * E using membership queries
        table.extend(teacher)
      # else:
        # print('[INFO] is consistent')
      if not is_closed:
        # print('[INFO] is NOT closed')
        # find s1 in S and a in A such that
        #   row(s1*a) is different from row(s) for all s in S
        s1a = table.find_not_closed()
        # print(f'[INFO] row({s1a}) is different from all row(s)')
        # add s1a to S
        # print(f'add {s1a} to S')
        table.add_to_S(f'{s1a}')
        # extend T to (S U S*A) * E using membership queries
        table.extend(teacher)
      # else:
        # print('[INFO] is closed')
      # table.print_table()
      is_closed = table.closed()
      is_consistent = table.consistent()

    # (S,E,T) is now closed and consistent
    # make the conjecture
    M = table.to_acceptor()
    t = teacher.respond_to_conjecture(M)
    # if the teacher replies with a counterexample t, then
    if t is not None:
      # add t and all its (non-empty) prefixes to S
      for p in prefixes(t):
        # print(f'[DEBUG] add {p} to S')
        table.add_to_S(p)
      # extend T to (S U S*A) * E using membership queries
      table.extend(teacher)
      M = None
    # else halt and output m
  return M

if __name__ == '__main__':
  ALPHABET = '01'
  if len(argv) > 1:
    ALPHABET = argv[1]
  TEACHER = HumanTeacher()

  ACCEPTOR = l_star(ALPHABET, TEACHER)
  print(f'{len(TEACHER.query_history)} queries')
  print('++')
  for q in TEACHER.query_history:
    if ACCEPTOR.accepts(q):
      print(q)
  print('--')
  for q in TEACHER.query_history:
    if ACCEPTOR.rejects(q):
      print(q)
  ACCEPTOR.print_acceptor()
