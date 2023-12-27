#!/usr/bin/env python3
"""
    Python's round() adopts "rounding half to even strategy"
"""


def show_round_with_4_n_6_as_last_digit():
  print("Rounding showing the stratety of 'rounding half to even strategy'")
  print('='*40)
  base = 1.21
  for i in range(10):
    n = base + i/100 + 0.004
    n2 = base + i/100 + 0.006
    r = round(n, 2)
    r2 = round(n2, 2)
    scrmsg = f"n={n} | round={r} | n2={n2} | round2={r2}"
    print(scrmsg)
  print('='*40)
  base = 1.32
  for i in range(10):
    n = base + i/100 + 0.005
    n2 = base + i/100 + 0.006
    r = round(n, 2)
    r2 = round(n2, 2)
    scrmsg = f"n={n} | round={r} | n2={n2} | round2={r2}"
  base = 1.32
  epsilon = 0.0051
  n = base + epsilon
  print(base, 'plus epsilon', epsilon, n, '=>', round(n, 2))


def show_round_with_5_followed_by_5():
  n = 1.5
  r = round(n, 0)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 2.5
  r = round(n, 0)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 3.5
  r = round(n, 0)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 4.5
  r = round(n, 0)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 1.15
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg, '|', n/2*2, 'did not work the "nearest even"')
  n = 1.151
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 1.25
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 1.35
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 1.45
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 1.55
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 1.65
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 1.75
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 1.85
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}  (did not work 'nearest even'"
  print(scrmsg)
  n = 1.95
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}  (did not work 'nearest even'"
  print(scrmsg)
  n = 2.85
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}  (did not work 'nearest even'"
  print(scrmsg)
  n = 2.95
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 3.85
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}  (did not work 'nearest even'"
  print(scrmsg)
  n = 3.95
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 5.85
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}  (did not work 'nearest even'"
  print(scrmsg)
  n = 5.95
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)
  n = 7.85
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}  (did not work 'nearest even'"
  print(scrmsg)
  n = 7.95
  r = round(n, 1)
  scrmsg = f"n={n} | round={r}"
  print(scrmsg)


def adhoctest():
  """

  """
  show_round_with_4_n_6_as_last_digit()
  show_round_with_5_followed_by_5()


def process():
  pass


if __name__ == "__main__":
  process()
  adhoctest()
