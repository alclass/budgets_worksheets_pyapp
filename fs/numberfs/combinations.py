"""
fs/numberfs/combinations.py
  contains, in its first version, two "related" functions, they are:
    comb_n_2_by_2(n)
    sum_first_n_ints_non_negative(n)

  They relate thus:
   a) c(n) = s(n-1)
   b) s(n) = c(n+1) [which is just the same as "a"]

Example:
  n = 5 comb=10.0
  n = 4 sum_first_n=10.0

In a nutshell, the combination of n 2 by 2 is equivalent to the sequence sum of the first (n-1) integers;
"""


def fact_inner(n):
  """
    calculates recursively the factorial of a number.

    Obs:
      this function can only be called from fact(), below,
      which "protects" it from the input parameter being a non-int or less than 0.
  """
  if n < 2:
    return 1
  return n * fact_inner(n-1)


def fact(n):
  """
    calculates the factorial of a number.

    Obs:
      this function calls fact_inner(n) that does the computing recursively;
      it, however, "protects" the latter from the input parameter being a non-int or less than 0.
  """
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None
  if n < 0:
    return None
  return fact_inner(n)


def comb_n_2_by_2(n):
  """
  c(n) = n! / (2 * (n-2)!)

  Notice that c(n) = s(n-1)
  where s() is sum_first_n_ints_non_negative
  """
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None
  if n < 2:
    return None
  num = fact(n)
  den = 2 * fact(n-2)
  return num / den


def sum_first_n_ints_non_negative(n):
  """
  s(n) = (n + 1) * n / 2

  Notice that s(n) = c(n+1)
  where s() is sum_first_n_ints_non_negative & c() is comb_n_2_by_2
  """
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None
  if n < 0:
    return None
  return (n + 1) * n / 2


def sum_first_n_ints_allow_negative(n):
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None
  is_negative = False
  nn = n
  if n < 0:
    is_negative = True
    nn = -n
  s = sum_first_n_ints_non_negative(nn)
  s = -s if is_negative else s
  return s


def adhoctest():
  n = 5
  comb = comb_n_2_by_2(n)
  scrmsg = f"n = {n} comb_n_2_2={comb}"
  print(scrmsg)
  n = 4
  sum_n = sum_first_n_ints_non_negative(n)
  scrmsg = f"n = {n} sum_first_ns={sum_n}"
  print(scrmsg)
  n = 12
  comb = comb_n_2_by_2(n)
  scrmsg = f"n = {n} comb_n_2_2={comb}"
  print(scrmsg)
  n = 11
  sum_n = sum_first_n_ints_non_negative(n)
  scrmsg = f"n = {n} sum_first_ns={sum_n}"
  print(scrmsg)


def process():
  """
  """
  pass


if __name__ == "__main__":
  process()
  adhoctest()
