from helpers import compact, prefixes

def test_compact():
  '''
  should remove λs from input string
  '''
  assert compact('λ') == 'λ'
  assert compact('aλ') == 'a'
  assert compact('λa') == 'a'
  assert compact('λλλ') == 'λ'
  assert compact('aλbcλdλe') == 'abcde'

def test_prefixes():
  '''
  should generate the non-empty prefixes of t
  '''
  assert list(prefixes('')) == []
  assert list(prefixes('a')) == []
  assert list(prefixes('ab')) == ['a']
  assert list(prefixes('abc')) == ['a', 'ab']
