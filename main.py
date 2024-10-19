'''
The Learner L*
from Learning Regular Sets from Queries and Counterexamples
by Dana Angluin
'''


from human_teacher import HumanTeacher
from human_examples_teacher import HumanExamplesTeacher
from human_lambda_teacher import HumanLambdaTeacher
from teacher import Teacher
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
  # l_star('01', HumanExamplesTeacher(
    # every 3rd symbol is 0
    # {'000','110','010100'},
    # {'λ','0','1','001','000111'}
    # even # of 0s and 1s
    # {'λ', '00', '11', '0110', '0101'},
    # {'0', '1', '01', '10', '000', '100', '010', '110', '011', '0100', '001', '0111', '101', '111'}
    # do not end with 10 and have length at least 2
    # {'00', '01', '11', '000', '001', '011', '100', '101', '111'},
    # {'λ', '0', '1', '10', '010', '110'}
    # contains 00 exactly once
    # {'00', '001', '0010', '0011', '0100', '00110', '100', '1100', '10100', '101001', '101100', '1010010', '1010011', '1010100', '10100110', '10100111', '101001110'},
    # {'λ', '0', '01', '000', '010', '0001', '0000', '00000', '00001', '00010', '00011', '00100', '000000', '000010', '000100', '000101', '000110', '0000000', '0000100', '0001000', '0001010', '0001100', '00010100', '00010000', '1', '10', '11', '101', '110', '1000', '1010', '1011', '10000', '10101', '10110', '101000', '101010', '1010000', '10100000', '10100100', '101001000', '101001100', '1010011000', '1010011100', '10100110001'}
    # ))
  # l_star('ab', HumanTeacher())

  # contains 00 exactly once
  # l_star('01', HumanLambdaTeacher(lambda string : string.find('00') >= 0 and string.find('00', string.find('00') + 1) == -1))
  # multiple of 3 0s
  teacher = HumanLambdaTeacher(lambda string : string.count('0') % 3 == 0)
  l_star('01', teacher)
  print(f'{len(teacher.query_history)} queries')
  for q in teacher.query_history:
    print(q)