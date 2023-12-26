#!/usr/bin/env python3
"""
fs/textfs/strfs.py
  Contains string related functions.
"""
import string


def pop_str(word):
  if word is None:
    return '', None
  if len(word) == '':
    return '', ''
  last_char = word[-1]
  word = word[: -1]
  return last_char, word


def is_cotacaocompra_a_number(cotacaocompra):
  try:
    _ = float(cotacaocompra)
  except (TypeError, ValueError):  # a non-None non-number arg
    return False
  return True


def round_last_digit_from_integer_get_as_str(anumber):
  inumber = round_last_digit_from_integer_get_as_int(anumber)
  if isinstance(inumber, int):
    return str(inumber)
  return None


def round_last_digit_from_integer_get_as_int(anumber):
  try:
    anumber = int(anumber)
  except (TypeError, ValueError):
    return None
  complement = anumber % 10
  if anumber % 2 == 0:  # even numbers
    if complement > 5:
      outnumber = anumber + (10 - complement)
    else:
      outnumber = anumber - complement
  else:  # odd numbers
    if complement > 6:
      outnumber = anumber + (10 - complement)
    else:
      outnumber = anumber - complement
  return outnumber


def graft_thousands_pointsep_from_a_commasep_strnumber(strnumber, max_dec_places=2):
  try:
    strnumber = str(strnumber)
    if strnumber.find('.') > -1:
      return None
    pp = strnumber.split(',')
    strintnumber = pp[0]
  except (AttributeError, TypeError, ValueError):
    return None
  rev_strintnumber_list = reversed(list(strintnumber))
  rev_strintnumber = ''.join(rev_strintnumber_list)
  ongoing = ''
  while 1:
    if len(rev_strintnumber) < 3:
      chunk = rev_strintnumber
      ongoing += chunk
      break
    chunk = rev_strintnumber[:3]
    rev_strintnumber = rev_strintnumber[3:]
    ongoing += chunk + '.'
  strintnumber_list = reversed(list(ongoing))
  strnumber = ''.join(strintnumber_list)
  if len(pp) > 1:
    str_dec_places = pp[1]
    if len(str_dec_places) > max_dec_places:
      intdecplaces = round_last_digit_from_integer_get_as_int(str_dec_places)
      str_dec_places = str(int(intdecplaces/10))
    strnumber = strnumber + ',' + str_dec_places
  return strnumber


def trans_str_or_number_to_tuple_commasepstrnumber_n_float(str_or_numbe, decimal_places=2, graft_pointsep=False):
  try:
    decimal_places = 0 if decimal_places < 0 else decimal_places
    if decimal_places == 0:
      return str(int(str_or_numbe))  # notice that its decimal part, if it exists, will be lost
    #
    strnumber = str(str_or_numbe).replace('.', '').replace(',', '.')
    output_floatnumber = float(strnumber)
    intnumber = int(round(output_floatnumber * (10 ** decimal_places), 0))
    re_floatnumber = intnumber / (10 ** decimal_places)
    strnumber = str(re_floatnumber).replace('.', ',')
    pp = strnumber.split(',')
    if len(pp) > 1:
      newdecplaces = round_last_digit_from_integer_get_as_str(pp[1])
      strnumber = pp[0] + ',' + newdecplaces
    if graft_pointsep:
      strnumber = graft_thousands_pointsep_from_a_commasep_strnumber(strnumber)
    return strnumber, output_floatnumber
  except ValueError:
    pass
  return None, None


def pick_first_word(phrase):
  if phrase is None:
    return None
  if ' ' not in phrase:
    return phrase
  return phrase.split(' ')[0]


def validate_formedness_returning_brazils_cep_as_str_or_none(p_cep):
  """
  Validades a CEP number or string. It returns its string 8-char form or None.
    Obs: it validates its "well-formedness", not its existence.

  Brazil's CEP is composed of 8 numeric digits and may have a dot and a dash in format.
  These, the dot and the dash, are stripped out so that the work is only
    to check up 8 number digits.
  """
  try:
    strcep = str(p_cep)
    strcep = strcep.replace('.', '').replace('-', '')
    charlist = list(filter(lambda c: c in string.digits, strcep))
    strcep = ''.join(charlist)
    if len(strcep) == 8:
      return strcep
  except (TypeError, ValueError):
    pass
  return None


def adhoc_test():
  """
  stri = 'sadfadfx'
  c, newstr = pop_str(stri)
  print(stri, 'pop() =>', c, ',', newstr)

  """
  cotacaocompra = "2.456,456"
  strnumber, float_n = trans_str_or_number_to_tuple_commasepstrnumber_n_float(cotacaocompra, decimal_places=2)
  scrmsg = f"cotacaocompra = {cotacaocompra} | strnumber = {strnumber} | float_n = {float_n}"
  print(scrmsg)
  ceptest = '20.550-045'
  cep = validate_formedness_returning_brazils_cep_as_str_or_none(ceptest)
  scrmsg = f"ceptest {ceptest} validate cep => {cep}"
  print(scrmsg)
  # =============
  anumber = '123'
  rounded_number = round_last_digit_from_integer_get_as_str(anumber)
  scrmsg = f"anumber {anumber} | rounded_number = {rounded_number}"
  print(scrmsg)
  anumber = '127'
  rounded_number = round_last_digit_from_integer_get_as_str(anumber)
  scrmsg = f"anumber {anumber} | rounded_number = {rounded_number}"
  print(scrmsg)
  strnumbers = ['12345677,326', '12345677,335', '12345676,325']
  for strnumber in strnumbers:
    re_strnumber = graft_thousands_pointsep_from_a_commasep_strnumber(strnumber)
    scrmsg = f"strnumber {strnumber} | re_strnumber = {re_strnumber}"
    print(scrmsg)


def process():
  adhoc_test()


if __name__ == "__main__":
  process()
