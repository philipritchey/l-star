'''
brzozowski algebraic method
'''

from sexpr import sexpr

STAR = 'star'
UNION = 'union'
CONCAT = 'concat'
EMPTY_STRING = 'ε'
EMPTY_LANGUAGE = '∅'

class literal(sexpr):
  def __init__(self, symbol: str):
    sexpr.__init__(self, symbol)

class concat(sexpr):
  def __init__(self, left: sexpr, right: sexpr):
    sexpr.__init__(self, CONCAT)
    self.left = left
    self.right = right

class union(sexpr):
  def __init__(self, left: sexpr, right: sexpr):
    sexpr.__init__(self, UNION)
    self.left = left
    self.right = right

class star(sexpr):
  def __init__(self, child: sexpr):
    sexpr.__init__(self, STAR)
    self.left = child

class empty_string(sexpr):
  def __init__(self):
    sexpr.__init__(self, EMPTY_STRING)

class empty_language(sexpr):
  def __init__(self):
    sexpr.__init__(self, EMPTY_LANGUAGE)

# def concat(e: set[str], f: set[str]) -> set[str]:
#   '''
#   concatenate two expressions

#   Args:
#       e (set[str]): first expression
#       f (set[str]): second expression

#   Returns:
#       set[str]: new expression: ef
#   '''
#   if len(e) > 1:
#     e = e.difference({EMPTY_LANGUAGE})
#   if len(e) > 1:
#     left = '('+'|'.join(e)+')'
#   elif len(e) == 1:
#     left = e.pop()
#   else:
#     left = ''

#   if left == EMPTY_LANGUAGE:
#     return {EMPTY_LANGUAGE}

#   if len(f) > 1:
#     f = f.difference({EMPTY_LANGUAGE})
#   if len(f) > 1:
#     right = '('+'|'.join(f)+')'
#   elif len(f) == 1:
#     right = f.pop()
#   else:
#     right = ''

#   if right == EMPTY_LANGUAGE:
#     return {EMPTY_LANGUAGE}

#   s = (left + right).replace(EMPTY_STRING, '')
#   if len(s) == 0:
#     return {EMPTY_STRING}
#   return {f"{s}"}

# def star(e: set[str]) -> set[str]:
#   '''
#   closure of expression

#   Args:
#       e (set[str]): expression

#   Returns:
#       set[str]: new exression: (e)*
#   '''
#   if len(e) > 1:
#     e = e.difference({EMPTY_LANGUAGE})
#   if len(e) > 1:
#     left = '('+'|'.join(e)+')'
#   elif len(e) == 1:
#     left = e.pop()
#   else:
#     left = ''

#   if len(left) == 0 or left == EMPTY_LANGUAGE:
#     return {EMPTY_STRING}
#   return {f"({left})*"}

# def union(e: set[str], f: set[str]) -> set[str]:
#   '''
#   union of two expressions

#   Args:
#       e (set[str]): first expression
#       f (set[str]): second expression

#   Returns:
#       set[str]: new expression: (e|f)
#   '''
#   g = e.union(f)
#   if len(g) > 1:
#     g = g.difference({EMPTY_LANGUAGE})
#   if len(g) > 1:
#     left = '('+'|'.join(g)+')'
#   elif len(g) == 1:
#     left = g.pop()
#   else:
#     left = ''

#   if left == EMPTY_LANGUAGE:
#     return {EMPTY_LANGUAGE}
#   if len(left) == 0 or left == EMPTY_LANGUAGE:
#     return {EMPTY_STRING}
#   return {f"{left}"}

def combine(symbols: list[str]) -> sexpr:
  n = len(symbols)
  match n:
    case 0:
      return empty_language()
    case 1:
      return sexpr(symbols[0])
    case 2:
      return union(sexpr(symbols[0]), sexpr(symbols[1]))
    case _:
      m = int(n/2) + 1
      return union(combine(symbols[:m]), combine(symbols[m:]))

def brzozowski(m: int, alphabet: str, final: set[int], trans: dict[tuple[int, str], set[int]]) -> sexpr:
  B: list[sexpr] = []
  for i in range(m):
    if i in final:
      B.append(empty_string())
    else:
      B.append(empty_language())
  # print(f"[DEBUG] {B=}")

  A: list[list[sexpr]] = []
  for i in range(m):
    A.append([])
    for j in range(m):
      symbols = []
      for a in alphabet:
        if (i, a) in trans and j in trans[(i, a)]:
          symbols.append(a)
      A[i].append(combine(symbols))
  # print(f"[DEBUG] {A=}")

  for n in range(m-1,-1,-1):
    B[n] = concat(star(A[n][n]), B[n])
    # print(f"[DEBUG] B[{n}]={B[n]}")
    for j in range(n):
      A[n][j] = concat(star(A[n][n]), A[n][j])
      # print(f"[DEBUG] A[{n}][{j}]={A[n][j]}")
    for i in range(n):
      B[i] = union(B[i], concat(A[i][n], B[n]))
      # print(f"[DEBUG] B[{i}]={B[i]}")
      for j in range(n):
        A[i][j] = union(A[i][j], concat(A[i][n], A[n][j]))
        # print(f"[DEBUG] A[{i}][{j}]={A[i][j]}")

  return B[0]

def simplify(expr: sexpr) -> sexpr:
  match expr.name:
    case 'union':
      if expr.left == expr.right:
        return simplify(expr.left)

      if expr.left.name == 'union':
        e, f, g = expr.left.left, expr.left.right, expr.right
        return simplify(union(e, union(f, g)))

      if expr.left.name == EMPTY_LANGUAGE:
        return simplify(expr.right)

      if expr.right.name == EMPTY_LANGUAGE:
        return simplify(expr.left)

      return union(simplify(expr.left), simplify(expr.right))

    case 'concat':
      if expr.left.name == 'concat':
        e, f, g = expr.left.left, expr.left.right, expr.right
        return simplify(concat(e, concat(f, g)))

      if expr.left.name == EMPTY_STRING:
        return simplify(expr.right)

      if expr.right.name == EMPTY_STRING:
        return simplify(expr.left)

      if expr.left.name == EMPTY_LANGUAGE:
        return empty_language()

      if expr.right.name == EMPTY_LANGUAGE:
        return empty_language()

      return concat(simplify(expr.left), simplify(expr.right))

    case 'star':
      if expr.left == EMPTY_STRING or expr.left == EMPTY_LANGUAGE:
        return empty_string()

      return star(simplify(expr.left))

    case _:
      return expr

def opt(e: sexpr) -> sexpr:
  e2 = simplify(e)
  if e == e2:
    return e2
  # print(f"[DEBUG] e2={e2}")
  return opt(e2)

def pretty(e: sexpr) -> str:
  match e.name:
    case 'concat':
      return f"{pretty(e.left)}{pretty(e.right)}"
    case 'union':
      return f"({pretty(e.left)}|{pretty(e.right)})"
    case 'star':
      inner = pretty(e.left)
      if e.left.name == UNION:
        return f"{inner}*"
      return f"({inner})*"
    case _:
      return e.name

def test_pretty() -> None:
  # (concat b a) => ba
  pre = concat(literal('b'), literal('a'))
  post = 'ba'
  assert pretty(pre) == post, f"\n  actual: {pretty(pre)}\nexpected: {post}"

  # (star (union (concat b a) (concat (union a (concat b b)) (concat (star (concat a b)) (union b (concat a a))))))
  #   => (ba|(a|bb)(ab)*(b|aa))*
  pre = star(
    union(
      concat(
        literal('b'),
        literal('a')
      ),
      concat(
        union(
          literal('a'),
          concat(
            literal('b'),
            literal('b')
          )
        ),
        concat(
          star(
            concat(
              literal('a'),
              literal('b')
            )
          ),
          union(
            literal('b'),
            concat(
              literal('a'),
              literal('a')
            )
          )
        )
      )
    )
  )
  assert pretty(pre) == '(ba|(a|bb)(ab)*(b|aa))*', f"got: {pretty(pre)}"

def test_opt() -> None:
  # (union (concat a b) (concat a b)) => (concat a b)
  pre = union(concat(literal('a'), literal('b')), concat(literal('a'), literal('b')))
  post = concat(literal('a'), literal('b'))
  assert opt(pre) == post

def test_simplify() -> None:
  # (union (concat a b) (concat a b)) => (concat a b)
  pre = union(concat(literal('a'), literal('b')), concat(literal('a'), literal('b')))
  post = concat(literal('a'), literal('b'))
  assert simplify(pre) == post

def test_brzozowski() -> None:
  ans = brzozowski(
    3,     # number of states
    'ab',  # alphabet
    {0},   # final states
    {      # transitions
      (0, 'a'): {1},
      (0, 'b'): {2},
      (1, 'a'): {2},
      (1, 'b'): {0},
      (2, 'a'): {0},
      (2, 'b'): {1}
    })
  assert pretty(opt(ans)) == '(ba|(a|bb)(ab)*(b|aa))*'

  ans = brzozowski(
    4,
    '01',
    {3},
    {
      (0,'0'): {0,1,2},
      (0,'1'): {0,1},
      (1,'1'): {3},
      (2,'0'): {3},
      (2,'1'): {3},
    }
  )
  assert pretty(opt(ans)).replace('(0|1)', '.') == '.*(0.|.1)', f"got {pretty(opt(ans))}"

def test() -> None:
  test_simplify()
  test_opt()
  test_pretty()
  test_brzozowski()
  print('ALL TESTS PASSING')

if __name__ == '__main__':
  test()