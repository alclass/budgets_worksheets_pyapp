#!/usr/bin/env python3
"""
  docstring
"""
import datetime
import sys
import fs.economicfs.preapis_finfunctions as prefs


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
    res_bcb_api1 = prefs.dbfetch_bcb_cotacao_compra_dolar_apifallback(argdate)
    print(res_bcb_api1)
  res_bcb_api1 = prefs.dbfetch_bcb_cotacao_compra_dolar_apifallback(datetime.date.today())
  print(res_bcb_api1)
  pdate = '2020-03-31'
  res_bcb_api1 = prefs.dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
  print(res_bcb_api1)


def process():
  pass


if __name__ == "__main__":
  process()
