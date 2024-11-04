'''
brzozowski algebraic method
'''

from sexpr import sexpr

EMPTY_LANGUAGE = '∅'
EMPTY_STRING = 'ε'
CONCAT = 'concat'
OPTIONAL = 'option'
SOME = 'some'
STAR = 'star'
UNION = 'union'


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

class optional(sexpr):
  def __init__(self, child: sexpr):
    sexpr.__init__(self, OPTIONAL)
    self.left = child

class some(sexpr):
  def __init__(self, child: sexpr):
    sexpr.__init__(self, SOME)
    self.left = child

class empty_string(sexpr):
  def __init__(self):
    sexpr.__init__(self, EMPTY_STRING)

class empty_language(sexpr):
  def __init__(self):
    sexpr.__init__(self, EMPTY_LANGUAGE)

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
      # (e|e) => e
      if expr.left == expr.right:
        return simplify(expr.left)

      # (∅|e) => e
      if expr.left.name == EMPTY_LANGUAGE:
        return simplify(expr.right)

      # (e|∅) => e
      if expr.right.name == EMPTY_LANGUAGE:
        return simplify(expr.left)

      # (ε|e) => e?
      if expr.left.name == EMPTY_STRING:
        return simplify(optional(expr.right))

      # (e|ε) => e?
      if expr.right.name == EMPTY_STRING:
        return simplify(optional(expr.left))

      # (e|fe) => f?e
      # (e|ef) => ef?
      if expr.right.name == 'concat':
        if expr.left == expr.right.right:
          return simplify(concat(optional(expr.right.left), expr.left))
        if expr.left == expr.right.left:
          return simplify(concat(expr.left, optional(expr.right.right)))

      # (fe|e) => f?e
      # (ef|e) => ef?
      if expr.left.name == 'concat':
        if expr.right == expr.left.right:
          return simplify(concat(optional(expr.left.left), expr.right))
        if expr.right == expr.left.left:
          return simplify(concat(expr.right, optional(expr.left.right)))

      # TODO
      # (e+|e*) => e*
      # (e+|e?) => e*
      # (e*|e?) => e*

      # ((e|f)|g) => (e|(f|g))
      if expr.left.name == 'union':
        e, f, g = expr.left.left, expr.left.right, expr.right
        return simplify(union(e, union(f, g)))

      return union(simplify(expr.left), simplify(expr.right))

    case 'concat':
      # ∅e => ∅
      if expr.left.name == EMPTY_LANGUAGE:
        return empty_language()

      # e∅ => ∅
      if expr.right.name == EMPTY_LANGUAGE:
        return empty_language()

      # εe => e
      if expr.left.name == EMPTY_STRING:
        return simplify(expr.right)

      # eε => e
      if expr.right.name == EMPTY_STRING:
        return simplify(expr.left)

      # ee* = e*e => e+
      if expr.right.name == 'star' and expr.right.left == expr.left:
        return some(simplify(expr.left))
      if expr.left.name == 'star' and expr.left.left == expr.right:
        return some(simplify(expr.right))

      # e*e* => e*
      if expr.left.name == 'star' and expr.left == expr.right:
        return simplify(expr.left)

      # e+e+ => ee+
      if expr.left.name == 'some' and expr.left == expr.right:
        return simplify(concat(expr.left.left, expr.right))

      # (ef)g => e(fg)
      if expr.left.name == 'concat':
        e, f, g = expr.left.left, expr.left.right, expr.right
        return simplify(concat(e, concat(f, g)))

      return concat(simplify(expr.left), simplify(expr.right))

    case 'star':
      # ∅* => ε
      # ε* => ε
      if expr.left.name == EMPTY_STRING or expr.left.name == EMPTY_LANGUAGE:
        return empty_string()

      return star(simplify(expr.left))

    case 'option':
      # ∅? => ε
      # ε? => ε
      if expr.left.name == EMPTY_STRING or expr.left.name == EMPTY_LANGUAGE:
        return empty_string()

      return optional(simplify(expr.left))

    case 'some':
      # ∅+ => ∅
      if expr.left.name == EMPTY_LANGUAGE:
        return empty_language()

      # ε+ => ε
      if expr.left.name == EMPTY_STRING:
        return empty_string()

      # (e+)+ => e+
      if expr.left.name == 'some':
        return simplify(expr.left)

      # (e*)+ => e*
      if expr.left.name == 'star':
        return simplify(expr.left)

      # (e?)+ => e*
      if expr.left.name == 'option':
        return simplify(star(expr.left.left))

      return some(simplify(expr.left))

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
      if e.left.name != CONCAT:
        return f"{inner}*"
      return f"({inner})*"
    case 'option':
      inner = pretty(e.left)
      if e.left.name != CONCAT:
        return f"{inner}?"
      return f"({inner})?"
    case 'some':
      inner = pretty(e.left)
      if e.left.name != CONCAT:
        return f"{inner}+"
      return f"({inner})+"
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

  pre = optional(
    union(
      literal('a'),
      literal('b')
    )
  )
  assert pretty(pre) == '(a|b)?', f"got: {pretty(pre)}"

  pre = optional(
    literal('a')
  )
  assert pretty(pre) == 'a?', f"got: {pretty(pre)}"

  pre = star(
    union(
      literal('a'),
      literal('b')
    )
  )
  assert pretty(pre) == '(a|b)*', f"got: {pretty(pre)}"

  pre = star(
    literal('a')
  )
  assert pretty(pre) == 'a*', f"got: {pretty(pre)}"

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

  # 00* => 0+
  pre = concat(literal('0'), star(literal('0')))
  post = some(literal('0'))
  assert simplify(pre) == post, f"got: {simplify(pre)}"

  # 0(0*1) => 0+1
  pre = concat(literal('0'), concat(star(literal('0')), literal('1')))
  post = concat(some(literal('0')), literal('1'))
  assert simplify(pre) == post, f"got: {simplify(pre)}"

  # (1|00*1)* => (1|0+1)* => ((empty|0+)1)* => ((0+)?1)* => (0*1)*
  pre = star(union(literal('1'), concat(literal('0'), concat(star(literal('0')), literal('1')))))
  post = star(concat(star(literal('0')), literal('1')))
  assert simplify(pre) == post, f"got: {simplify(pre)}"

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
  assert pretty(opt(ans)) == '(ba|(a|bb)(ab)*(b|aa))*', f"got {pretty(opt(ans))}"

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

  ans = brzozowski(
    5,
    '01',
    {0,1,2},
    {
      (0,'0'): {0},
      (0,'1'): {1},
      (1,'0'): {0},
      (1,'1'): {2},
      (2,'0'): {2},
      (2,'1'): {3},
      (3,'0'): {2},
      (3,'1'): {4},
      (4,'0'): {4},
      (4,'1'): {4},
    }
  )
  assert pretty(opt(ans)) == '(0|10)*(1(1(0|10)*)?)?', f"got {pretty(opt(ans))}"

  ans = brzozowski(
    5,
    '01',
    {0,1,2},
    {
      (0,'0'): {0},
      (0,'1'): {1},
      (1,'0'): {0},
      (1,'1'): {2},
      (2,'0'): {3},
      (2,'1'): {4},
      (3,'0'): {3},
      (3,'1'): {2},
      (4,'0'): {4},
      (4,'1'): {4},
    }
  )
  assert pretty(opt(ans)) == '(0|10)*(1(1(00*1)*)?)?', f"got {pretty(opt(ans))}"

def test() -> None:
  test_simplify()
  test_opt()
  test_pretty()
  test_brzozowski()
  print('ALL TESTS PASSING')

if __name__ == '__main__':
  test()