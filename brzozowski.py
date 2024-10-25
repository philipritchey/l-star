'''
brzozowski algebraic method
'''

EMPTY_STRING = 'ε'
EMPTY_LANGUAGE = '∅'

class sexpr:
  def __init__(self, name: str):
    self.name = name
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if not self.left:
      return f"({self.name})"
    if not self.right:
      return f"({self.name} {self.left})"
    return f"({self.name} {self.left} {self.right})"

  def __eq__(self, other) -> bool:
    return str(self) == str(other)

class concat(sexpr):
  def __init__(self, left: sexpr, right: sexpr):
    sexpr.__init__(self, 'concat')
    self.left = left
    self.right = right

class union(sexpr):
  def __init__(self, left: sexpr, right: sexpr):
    sexpr.__init__(self, 'union')
    self.left = left
    self.right = right

class star(sexpr):
  def __init__(self, child: sexpr):
    sexpr.__init__(self, 'star')
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

def brzozowski(m: int, alphabet: str, final: set[int], trans: dict[tuple[int, str], int]) -> sexpr:
  B: list[sexpr] = []
  for i in range(m):
    if i in final:
      B.append(empty_string())
    else:
      B.append(empty_language())
  print(f"[DEBUG] {B=}")

  A: list[list[sexpr]] = []
  for i in range(m):
    A.append([])
    for j in range(m):
      symbols = []
      for a in alphabet:
        if (i, a) in trans and trans[(i, a)] == j:
          symbols.append(a)
      A[i].append(combine(symbols))
  print(f"[DEBUG] {A=}")

  for n in range(m-1,-1,-1):
    B[n] = concat(star(A[n][n]), B[n])
    print(f"[DEBUG] B[{n}]={B[n]}")
    for j in range(n):
      A[n][j] = concat(star(A[n][n]), A[n][j])
      print(f"[DEBUG] A[{n}][{j}]={A[n][j]}")
    for i in range(n):
      B[i] = union(B[i], concat(A[i][n], B[n]))
      print(f"[DEBUG] B[{i}]={B[i]}")
      for j in range(n):
        A[i][j] = union(A[i][j], concat(A[i][n], A[n][j]))
        print(f"[DEBUG] A[{i}][{j}]={A[i][j]}")

  return B[0]

def simplify(expr: sexpr) -> sexpr:
  match expr.name:
    case 'union':
      if expr.left == expr.right:
        return expr.left

      if expr.left.name == 'union':
        e, f, g = expr.left.left, expr.left.right, expr.right
        return simplify(union(e, union(f, g)))

      if expr.left.name == EMPTY_LANGUAGE:
        return expr.right

      if expr.right.name == EMPTY_LANGUAGE:
        return expr.left

      return union(simplify(expr.left), simplify(expr.right))

    case 'concat':
      if expr.left.name == 'concat':
        e, f, g = expr.left.left, expr.left.right, expr.right
        return simplify(concat(e, concat(f, g)))

      if expr.left.name == EMPTY_STRING:
        return expr.right

      if expr.right.name == EMPTY_STRING:
        return expr.left

      if expr.left.name == EMPTY_LANGUAGE:
        return expr.left

      if expr.right.name == EMPTY_LANGUAGE:
        return expr.right

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
  print(f"[DEBUG] e2={e2}")
  return opt(e2)

if __name__ == '__main__':
  FINAL = {0}
  TRANS: dict[tuple[int, str], int] = {
    (0, 'a'): 1,
    (0, 'b'): 2,
    (1, 'a'): 2,
    (1, 'b'): 0,
    (2, 'a'): 0,
    (2, 'b'): 1
  }
  ans = brzozowski(3, 'ab', FINAL, TRANS)
  print('=====')
  print(ans)
  print('-----')
  # TODO(pcr) why is opt not working?
  print(opt(ans))