from typing import Generator

def compact(s: str) -> str:
  '''
  remove λs from s

  Args:
      s (str): string from which to remove λs

  Returns:
      str: s without λs
  '''
  t = s.replace('λ', '')
  if len(t) == 0:
    t = 'λ'
  return t

def prefixes(t: str) -> Generator[str, None, None]:
  '''
  non-empty prefixes of t
  '''
  for i in range(1, len(t)):
    yield t[:i]