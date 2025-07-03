#!/usr/bin/env python3
"""
  This script has three accompanying parameters, they are:
  1) -- help                 |     shows this message
  2) -- procyear=<year>      |     fetches brl/usd exchange rate quotes for year <year>
  3) -- procdaterange=<dtini,dtfim>      |     fetches brl/usd exchange rate quotes for daterange <dtini,dtfim>
"""
import sys
import fs.indices.bcb_br.bcb_financefunctions as finfs
import fs.datefs.dategenerators as gendt


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
  """
  TO-DO: adapt the argparse library for this adhoctest1()
  """
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
    datelist = gendt.gen_dailydates_or_empty_bw_ini_fim_opt_order(inidate, findate)
    finfs.fetch_cotacao_brl_per_usd_for_datelist(datelist)


def process():
  pass


if __name__ == "__main__":
  """
  adhoctest1()
  """
  process()
  adhoctest()
