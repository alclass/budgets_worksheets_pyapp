#!/usr/bin/env python3

def pop_str(word):
  if word is None:
    return '', None
  if len(word) == '':
    return '', ''
  last_char = word[-1]
  word = word[ : -1]
  return last_char, word

def is_cotacaoCompra_a_number(cotacaoCompra):
  try:
    _ = float(cotacaoCompra)
  except ValueError: # a non-None non-number arg
    return False
  except TypeError: # a None arg
    return False
  return True

def replace_point_to_comma(cotacaoCompra, decimal_places=2):
  if not is_cotacaoCompra_a_number(cotacaoCompra):
    return cotacaoCompra
  if decimal_places < 0:
    decimal_places = 0
  if decimal_places == 0:
    return str(int(cotacaoCompra))
  strCotacaoCompra = str(cotacaoCompra)
  pos = strCotacaoCompra.find('.')
  if pos < 0:
    return cotacaoCompra
  strCotacaoCompra = strCotacaoCompra.replace('.', ',')
  pp = strCotacaoCompra.split(',')
  intpart = pp[0]
  if intpart == '':
    intpart = '1'
  nplaces = len(pp[-1])
  if nplaces == decimal_places:
    return strCotacaoCompra
  dif = abs(nplaces - decimal_places)
  if nplaces < decimal_places:
    return strCotacaoCompra + '0'*dif
  strplaces = pp[-1]
  strplaces = strplaces[:-dif]
  recomposed = intpart + ',' + strplaces
  return recomposed


def pick_first_word(phrase):
  if phrase is None:
    return None
  if ' ' not in phrase:
    return phrase
  return phrase.split(' ')[0]

def adhoc_test():
  '''
  stri = 'sadfadfx'
  c, newstr = pop_str(stri)
  print(stri, 'pop() =>', c, ',', newstr)

  :return:
  '''
  cotacaoCompra = None #'bla' # .141
  res = replace_point_to_comma(cotacaoCompra, decimal_places=7)
  print(cotacaoCompra, '=>', res)

def process():
  adhoc_test()

if __name__ == "__main__":
  process()

