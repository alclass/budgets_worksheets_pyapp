#!/usr/bin/env python3
"""
models/exrate/fetch_exchange_rate_by_date.py
  docstring
"""
import datetime
import sys
import fs.economicfs.bcb.bcb_cotacao_fetcher_from_db_or_api as prefs


def get_args():
  datelist = []
  for argdate in sys.argv[1:]:
    if argdate.startswith('--help'):
      print(__doc__)
      return {}
    print('Arg', argdate)
    datelist.append(argdate)
  return datelist


def adhoctest():
  datelist = get_args()
  for argdate in datelist:
    bcb = prefs.BCBCotacaoFetcher(argdate)
    res_bcb_api1 = bcb.namedtuple_cotacao
    print(res_bcb_api1)
  today = datetime.date.today()
  bcb = prefs.BCBCotacaoFetcher(today)
  res_bcb_api1 = bcb.namedtuple_cotacao
  print(res_bcb_api1)
  pdate = '2020-03-31'
  bcb = prefs.BCBCotacaoFetcher(pdate)
  res_bcb_api1 = bcb.namedtuple_cotacao
  print(res_bcb_api1)


def process():
  pass


if __name__ == "__main__":
  """
  adhoctest()
  """
  process()
  adhoctest()
