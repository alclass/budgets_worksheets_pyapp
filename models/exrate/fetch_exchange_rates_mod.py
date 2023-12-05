#!/usr/bin/env python3
"""
  This script has three accompanying parameters, they are:
  1) -- help                 |     shows this message
  2) -- procyear=<year>      |     fetches brl/usd exchange rate quotes for year <year>
  3) -- procdaterange=<dtini,dtfim>      |     fetches brl/usd exchange rate quotes for daterange <dtini,dtfim>
"""
import sys
import fs.economicfs.bcb.bcb_financefunctions as finfs


def get_args():
  argsdict = {}
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      return {}
    elif arg.startswith('--procyear='):
      year = int(arg[len('--procyear='):])
      argsdict = {'procyear': year}
    elif arg.startswith('--procdaterange='):
      strdaterange = arg[len('--procdaterange='):]
      daterange = strdaterange.split(',')
      argsdict = {'procdaterange': daterange}
  return argsdict


def adhoctest():
  argsdict = get_args()
  if len(argsdict) == 0:
    return
  if 'procyear' in argsdict.keys():
    year = argsdict['procyear']
    print('Parameter procyear = ', year)
    return finfs.fetch_cotacao_brl_per_usd_for_datelist(year)
  if 'procdaterange' in argsdict.keys():
    daterange = argsdict['procdaterange']
    inidate, findate = daterange
    print('Parameter procdaterange = ', daterange)
    finfs.fetch_cotacao_brl_per_usd_for_datelist(inidate, findate)


def process():
  pass


if __name__ == "__main__":
  process()
