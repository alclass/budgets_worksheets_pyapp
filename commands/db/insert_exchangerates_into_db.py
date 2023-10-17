#!/usr/bin/env python3
"""
insert_exchangerates_into_db.py
"""
import datetime
import settings as cfg
import fs.economicfs.preapis_finfunctions as fin

def fetch_exchangerate_thru_api(pydate):
  bcb_api_nt = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pydate)
  return bcb_api_nt


def process():
  """
  pastdate = '2020-10-15'

  """
  pydate = datetime.date(2020, 10, 15)
  bcb_api_nt = fetch_exchangerate_thru_api(pydate)
  print(bcb_api_nt)
  print(bcb_api_nt.cotacao_venda)


if __name__ == '__main__':
  process()
