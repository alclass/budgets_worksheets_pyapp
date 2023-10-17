#!/usr/bin/env python3
"""
show_exchangerates_for_dates.py

This script reads a dates data (text) file inside the app's data folder,
  fetches sell quotes for each date and outputs a 2-column data text.

The output text contains:
- in the first column the input dates and
- in the second the day-to-day 'sell quotes *
  * 'cotação de venda' do par de moedas
"""
import sys

import commands.show.gen_composite_currency_updter as composite
import fs.economicfs.preapis_finfunctions as fin
import fs.datefs.dategenerators as gendt
import fs.datefs.datefunctions as dtfs


def show_exchangerates_between_dates():
  pydates = composite.get_pydates_from_datafile()
  for pdate in pydates:
    bcb_api_nt = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    print(str(pdate), bcb_api_nt.cotacao_venda)


def show_exchangerates_for_rangedate(date_ini, date_fim):
  for pdate in gendt.gen_daily_dates_for_daterange(date_ini, date_fim):
    bcb_api_nt = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    print(str(pdate), bcb_api_nt.cotacao_venda)


def show_exchangerates_for_last_month():
  for pdate in gendt.gen_daily_dates_for_last_month(decrescent=True):
    bcb_api_nt = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    print(str(pdate), bcb_api_nt.cotacao_venda)


def show_exchangerates_for_current_year():
  for pdate in gendt.gen_daily_dates_for_current_year(decrescent=True):
    bcb_api_nt = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    print(str(pdate), bcb_api_nt.cotacao_venda)


def adhoctest():
  """
  pastdate = '2020-10-15'
  pydate = datetime.date(2020, 10, 15)

  """
  # show_exchangerates_between_dates()
  # show_exchangerates_for_last_month()
  show_exchangerates_for_current_year()


def get_args():
  pdate_ini = None
  pdate_fim = None
  for arg in sys.argv:
    if arg.startswith('-ini='):
      strdate = arg[len('-ini='):]
      pdate_ini = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate)
    else:
      strdate = arg[len('-ini='):]
      pdate_ini = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate)
  return pdate_ini, pdate_fim


def process():
  date_ini, date_fim = get_args()
  show_exchangerates_for_rangedate(date_ini, date_fim)


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()

