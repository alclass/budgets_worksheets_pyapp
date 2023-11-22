# calc.py
"""
https://realpython.com/command-line-interfaces-python-argparse/
"""

import argparse


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return a / b


def example1():
  global_parser = argparse.ArgumentParser(prog="calc")
  subparsers = global_parser.add_subparsers(title="subcommands", help="arithmetic operations")
  arg_template = {
      "dest": "operands",
      "type": float,
      "nargs": 2,
      "metavar": "OPERAND",
      "help": "a numeric value",
  }
  add_parser = subparsers.add_parser("add", help="add two numbers a and b")
  add_parser.add_argument(**arg_template)
  add_parser.set_defaults(func=add)
  sub_parser = subparsers.add_parser("sub", help="subtract two numbers a and b")
  sub_parser.add_argument(**arg_template)
  sub_parser.set_defaults(func=sub)
  mul_parser = subparsers.add_parser("mul", help="multiply two numbers a and b")
  mul_parser.add_argument(**arg_template)
  mul_parser.set_defaults(func=mul)
  div_parser = subparsers.add_parser("div", help="divide two numbers a and b")
  div_parser.add_argument(**arg_template)
  div_parser.set_defaults(func=div)
  args = global_parser.parse_args()
  print(args.func(*args.operands))


def get_args_via_argparse():
  """
  https://realpython.com/command-line-interfaces-python-argparse/
  One Example:
    parser.add_argument("--veggies", nargs="+")
    parser.add_argument("--fruits", nargs="*")
      $ python cooking.py --veggies pepper tomato --fruits apple banana
    parser.add_argument("--size", choices=["S", "M", "L", "XL"], default="M")
    my_parser.add_argument("--weekday", type=int, choices=range(1, 8))
  """
  parser = argparse.ArgumentParser(description="Obtain Arguments")
  parser.add_argument(
    '-i', '--ini', metavar='date_ini', type=str, nargs='?',
    help="the beginning date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-f', '--fim', metavar='date_fim', type=str, nargs='?',
    help="the ending date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-cmc', '--calc-monet-corr', metavar='twodates', type=str, nargs=2,
    help="the ending date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-dl', '--datelist', metavar='datelist', type=str, nargs='+',
    help="datelist for finding daily exchange rate quotes one by one",
  )
  parser.add_argument(
    # example -rm "2023-04"
    '-rm', '--refmonth', type=str, nargs=1,
    help="the month as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-cy', '--current-year', action='store_true',
    help="days since the beginning of the current year as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-y', '--year', type=int, nargs=1,
    help="year as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-yr', '--yearrange', type=int, nargs=2,
    help="year range (ini, fim) as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-rdf', '--readdatefile', action='store_true',
    help="marker/signal for inputting the dates from the conventioned datefile located in the app's data folder",
  )
  parser.add_argument(
    '-s', '--serieschar', choices=["C", "S"], default="C",
    help="marker/signal for inputting the dates from the conventioned datefile located in the app's data folder",
  )
  parser.add_argument(
    '-cp', '--currencypair', type=str, nargs=1, default='brl/usd',
    help="for specifying the currency pair ratio that corresponds to the output quotes (default 'brl/usd')",
  )
  args = parser.parse_args()
  print('args =>', args)
  if args.refmonth is not None:
    # return calc_monet_corr_between_dates(args.refmonth)
    refmonthdate = args.refmonth[0]
    print('argparse refmonthdate', refmonthdate)
    return functionref(refmonthdate)
  if args.year is not None:
    pass
  return args


def functionref(refmonthdate):
  """
  Temporary
  """
  return refmonthdate


def process():
  """
    $ python calc.py add 3 8
    11.0
    $ python calc.py sub 15 5
    10.0
    $ python calc.py mul 21 2
    42.0
    $ python calc.py div 12 2
    6.0
    $ python calc.py -h
  """
  example1()


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
