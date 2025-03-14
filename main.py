'''
The Learner L*
from Learning Regular Sets from Queries and Counterexamples
by Dana Angluin
'''

import sys
from human_teacher import HumanTeacher
from human_examples_teacher import HumanExamplesTeacher
from human_lambda_teacher import HumanLambdaTeacher
from human_lambda_examples_teacher import HumanLambdaExamplesTeacher
from examples_teacher import ExamplesTeacher
from lambda_teacher import LambdaTeacher
from lambda_examples_teacher import LambdaExamplesTeacher
from l_star import l_star

def inflate(example: str, alphabet: str) -> list[str]:
  '''
  replace each X with a in alphabet

  Args:
    example (set[str]): example to inflate
    alphabet (str): alphabet to use

  Returns:
    list[str]: inflated examples
  '''
  if 'X' not in example:
    return [example]
  inflated_examples = []
  for a in alphabet:
    es = inflate(example.replace('X', a, 1), alphabet)
    inflated_examples.extend(es)
  return inflated_examples

def inflate_all(example_set: set[str], alphabet: str) -> set[str]:
  '''
  replace each X with a in alphabet

  Args:
    example_set (set[str]): examples to inflate
    alphabet (str): alphabet to use

  Returns:
    set[str]: inflated set of examples
  '''
  s: set[str] = set()
  for example in example_set:
    inflated_examples = inflate(example, alphabet)
    for e in inflated_examples:
      s.add(e)
  return s

def read_examples(examples_file: str) -> dict[str, set[str]]:
  '''
  read examples

  Args:
      examples_file (str): path to examples file

  Returns:
      dict[str, set[str]]: P: positive examples, N: negative examples
  '''
  examples: dict[str, set[str]] = {}
  examples['P'] = set()
  examples['N'] = set()
  with open(examples_file, 'r', encoding="utf-8") as f:
    description = f.readline().strip()
    print(description)
    active_set = examples['P']
    for line in f:
      line = line.strip()
      if line == '++':
        active_set = examples['P']
      elif line == '--':
        active_set = examples['N']
      else:
        # empty string -> λ
        if len(line) == 0:
          line = 'λ'
        active_set.add(line)
  return examples

def get_alphabet(examples: dict[str, set[str]]) -> str:
  '''
  get the alphabet

  Args:
      examples (dict[str, set[str]]): positive and negative examples

  Returns:
      str: string of symbols
  '''
  alphabet: set[str] = set()
  for example in examples['P'].union(examples['N']):
    for symbol in example:
      alphabet.add(symbol)
  alphabet.discard('X')
  alphabet.discard('λ')
  return str(''.join(sorted(alphabet)))

def use_examples_teacher(examples_file):
  examples = read_examples(examples_file)
  alphabet = get_alphabet(examples)
  # print(f"{alphabet=}")
  examples['P'] = inflate_all(examples['P'], alphabet)
  examples['N'] = inflate_all(examples['N'], alphabet)
  # print(f"{EXAMPLES=}")
  return alphabet, ExamplesTeacher(examples)

def use_lambda_examples_teacher(membership, examples_file):
  examples = read_examples(examples_file)
  alphabet = get_alphabet(examples)
  # print(f"{alphabet=}")
  examples['P'] = inflate_all(examples['P'], alphabet)
  examples['N'] = inflate_all(examples['N'], alphabet)
  # print(f"{EXAMPLES=}")
  return alphabet, HumanLambdaExamplesTeacher(membership, examples)

def print_acceptor(teacher, acceptor):
  print(f'{len(teacher.query_history)} queries')
  print('++')
  for q in teacher.query_history:
    if acceptor.accepts(q):
      print(q)
  print('--')
  for q in teacher.query_history:
    if acceptor.rejects(q):
      print(q)
  acceptor.print_acceptor()

if __name__ == '__main__':
  # if len(sys.argv) == 1:
  #   print('error: missing required examples filename')
  #   sys.exit(1)

  # examples_file = sys.argv[-1]

  # ALPHABET, TEACHER = use_examples_teacher(examples_file)

  # def starts_and_ends_with_11(string: str) -> bool:
  #   return string.startswith('11') and string.endswith('11')
  # ALPHABET, TEACHER = use_lambda_examples_teacher(starts_and_ends_with_11, 'examples/starts_and_ends_with_11')

  def second_symbol_1(string: str) -> bool:
    return len(string) > 1 and string[1] == '1'
  ALPHABET = '01'
  EXAMPLES = {
    'P': {'01', '11', '010', '011', '110', '111'},
    'N': {'λ', '0', '1', '00' '10', '000', '001', '100', '101'}
  }
  TEACHER = LambdaExamplesTeacher(second_symbol_1, EXAMPLES)

  ACCEPTOR = l_star(ALPHABET, TEACHER)

  print_acceptor(TEACHER, ACCEPTOR)

  # teacher = HumanTeacher()
  # P: set[str] = set()
  # N: set[str] = set()
  # def fn(string: str) -> bool:
  #   return False

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

  # contains 00 exactly once
  # l_star('01', HumanLambdaTeacher(lambda string : string.find('00') >= 0 and string.find('00', string.find('00') + 1) == -1))

  # multiple of 3 0s
  # teacher = HumanLambdaTeacher(lambda string : string.count('0') % 3 == 0)
  # P: set[str] = {'000'}
  # N: set[str] = set()
  # teacher = HumanLambdaExamplesTeacher(lambda string : string.count('0') % 3 == 0, P, N)
  # l_star('01', teacher)
  # print(f'{len(teacher.query_history)} queries')
  # for q in teacher.query_history:
  #   print(q)

  # length at least 2 and does not end with 10
  # def fn(string: str) -> bool:
  #   return len(string) >= 2 and not string.endswith('10')
  # P: set[str] = {
  #   '100',
  #   '101',
  #   '11',
  #   '1001',
  #   '1011',
  #   '111',
  #   '01',
  #   '1101',
  #   '1111',
  #   '1000',
  #   '1100',
  #   '00',
  #   '10001',
  #   '10000',
  #   '10011'
  # }
  # N: set[str] = {
  #   'λ',
  #   '0',
  #   '1',
  #   '10',
  #   '110',
  #   '1010',
  #   '1110',
  #   '10010'
  # }

  # contains 11 at most once
  # def fn(string: str) -> bool:
  #   return string.count('11') <= 1 and string.find('111') == -1
  # P = {
  #   'λ',
  #   '0',
  #   '1',
  #   '110',
  #   '10',
  #   '11',
  #   '1101',
  #   '01',
  #   '101',
  #   '011',
  #   '1011',
  #   '11001',
  #   '1100',
  #   '11000',
  #   '110001',
  #   '110010',
  #   '1100101',
  #   '10011',
  #   '0011'
  # }
  # N = {
  #   '111',
  #   '1111',
  #   '11111',
  #   '1110',
  #   '11101',
  #   '11011',
  #   '111111',
  #   '111011',
  #   '110111',
  #   '11001111',
  #   '110011',
  #   '1100111',
  #   '1100011',
  #   '11001011',
  #   '1101011',
  #   '110011011',
  #   '1111011',
  #   '1110011',
  #   '11000011',
  #   '110010011'
  # }

  # contains a non-prime number of 1s
  # def fn(string: str) -> bool:
  #   n = len(string)
  #   if n < 2:
  #     return True
  #   if n < 4:
  #     return False
  #   if n % 2 == 0 or n % 3 == 0:
  #     return True
  #   f = 6
  #   while (f-1)*(f-1) <= n:
  #     if n % (f-1) == 0 or n % (f+1) == 0:
  #       return True
  #     f += 6
  #   return False
  # N = {
  #   '11',
  #   '111',
  #   '11111',
  #   '1111111',
  #   '11111111111',
  #   '1111111111111',
  #   '11111111111111111',
  #   '1111111111111111111',
  #   '11111111111111111111111',
  #   '11111111111111111111111111111',
  #   '1111111111111111111111111111111',
  #   '1111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
  # }
  # P = {
  #   'λ',
  #   '1',
  #   '1111',
  #   '111111',
  #   '11111111',
  #   '111111111',
  #   '1111111111',
  #   '111111111111',
  #   '11111111111111',
  #   '111111111111111',
  #   '1111111111111111',
  #   '111111111111111111',
  #   '11111111111111111111',
  #   '111111111111111111111',
  #   '1111111111111111111111',
  #   '111111111111111111111111',
  #   '1111111111111111111111111',
  #   '11111111111111111111111111',
  #   '111111111111111111111111111',
  #   '1111111111111111111111111111',
  #   '111111111111111111111111111111',
  #   '11111111111111111111111111111111',
  #   '111111111111111111111111111111111',
  #   '1111111111111111111111111111111111',
  #   '11111111111111111111111111111111111',
  #   '111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
  #   '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
  # }

  # mystery 14 / no29
  # P: set[str] = {
  #   'λ',
  #   '00'
  # }
  # N: set[str] = {
  #   '0',
  #   '1',
  #   '01'
  # }

  # teacher = HumanLambdaExamplesTeacher(fn, P, N)
  # teacher = HumanExamplesTeacher(P, N)

  # acceptor = l_star('01', teacher)
  # print(f'{len(teacher.query_history)} queries')
  # print('++')
  # for q in teacher.query_history:
  #   if acceptor.accepts(q):
  #     print(q)
  # print('--')
  # for q in teacher.query_history:
  #   if acceptor.rejects(q):
  #     print(q)

  # for p in P:
  #   if p not in teacher.query_history:
  #     print(p, 'NOT USED')
  # for n in N:
  #   if n not in teacher.query_history:
  #     print(n, 'NOT USED')
