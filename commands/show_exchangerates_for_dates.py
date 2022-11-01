#!/usr/bin/env python3
"""
show_exchangerates_for_dates.py

This script reads a dates data (text) file inside the app's data folder,
  fetches sell quotes for each date and outputs a 2-column data text.

The output text contains:
- in the first column the input dates and
- in the second the day-to-day 'sell quotes" *
  * 'cotação de venda' do par de moedas
"""
import commands.gen_composite_currency_updter as composite
import fs.economicfs.preapis_finfunctions as fin


def show_exchangerates_between_dates():
  pydates = composite.get_pydates_from_datafile()
  for pydate in pydates:
    bcb_api_nt = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pydate)
    print(str(pydate), bcb_api_nt.cotacao_venda)


def process():
  """
  pastdate = '2020-10-15'
  pydate = datetime.date(2020, 10, 15)

  """
  show_exchangerates_between_dates()


if __name__ == '__main__':
  process()
