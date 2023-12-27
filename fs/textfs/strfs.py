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


def graft_thousands_pointsep_from_a_commasep_strnumber(strnumber, decimal_places=2):
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
    if len(str_dec_places) > decimal_places:
      intdecplaces = round_last_digit_from_integer_get_as_int(str_dec_places)
      str_dec_places = str(int(intdecplaces/10))
    strnumber = strnumber + ',' + str_dec_places
  return strnumber


def trans_pointsep_str_or_number_to_tuple_commasep_str_n_float(str_or_number, decimal_places=2, graft_pointsep=False):
  decimal_places = 0 if decimal_places < 0 else decimal_places
  if str_or_number is None:
    return None
  if isinstance(str_or_number, int):
    intnumber = str_or_number
    str_number = str(intnumber)
    strdecplaces = '' if decimal_places == 0 else ','+'0'*decimal_places
    str_number = str_number + strdecplaces
    return str_number, intnumber
  if isinstance(str_or_number, float):
    floatnumber = str_or_number
    str_number = str(round(floatnumber, decimal_places))
    str_number = str_number.replace(',', '').replace('.', ',')
    return str_number, floatnumber
  # at this point, continue converting str_or_number to str
  str_number = str(str_or_number)
  if str_number.find(',') > -1:
    errmsg = f"""param strnumber "{str_number}" for trans_str_or_number_to_tuple_commasepstrnumber_n_float()
    cannot contain "," (ie the comma character) as input: script cannot continue.
    """
    raise ValueError(errmsg)
  floatnumber = float(str_or_number)
  rounded_floatnumber = round(floatnumber, decimal_places)
  # notice that str(round()) may leave a '.' dec pla sep
  str_number = str(rounded_floatnumber)
  str_number = str_number.replace('.', ',')
  if str_number.find(',') > -1:
    pp = str_number.split(',')
    intpart = pp[0]
    commaside = pp[-1]
    n_decplaces_at_str = len(commaside)
    if n_decplaces_at_str != decimal_places:
      if decimal_places == 0:
        str_number = intpart
      elif n_decplaces_at_str > decimal_places:
        commaside = commaside[:decimal_places]
        str_number = intpart + ',' + commaside
      else:  # n_decplaces_at_str < decimal_places:
        complement = decimal_places - n_decplaces_at_str
        commaside += '0'*complement
        str_number = intpart + ',' + commaside
    else:  # ie n_decplaces_at_str == decimal_places:
      # str_number is itself
      pass
    if graft_pointsep:
      str_number = graft_thousands_pointsep_from_a_commasep_strnumber(str_number, decimal_places)
  return str_number, floatnumber


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
  cotacaocompra = "2456.456"
  strnumber, float_n = trans_pointsep_str_or_number_to_tuple_commasep_str_n_float(cotacaocompra, decimal_places=2)
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


def adhoc_test2():
  """
  cotacaocompra = "2456"
  strnumber, float_n = trans_pointsep_str_or_number_to_tuple_commasep_str_n_float(
    cotacaocompra, decimal_places=2, graft_pointsep=True
  )
  scrmsg = f"cotacaocompra = {cotacaocompra} | strnumber = {strnumber} | float_n = {float_n}"
  print(scrmsg)

  """
  cotacaocompra = "65332456.1234"
  strnumber, float_n = trans_pointsep_str_or_number_to_tuple_commasep_str_n_float(
    cotacaocompra, decimal_places=5, graft_pointsep=True
  )
  scrmsg = f"cotacaocompra = {cotacaocompra} | strnumber = {strnumber} | float_n = {float_n}"
  print(scrmsg)


def process():
  adhoc_test2()


if __name__ == "__main__":
  process()
