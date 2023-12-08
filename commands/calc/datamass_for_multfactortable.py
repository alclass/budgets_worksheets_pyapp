#!/usr/bin/env python3
"""
commands/calc/datamass_for_multfactortable.py

"""
import collections
import fs.datefs.datefunctions as dtfs
nt_dateprice_constr = collections.namedtuple('NTDeP', field_names=['date', 'price'])


def get_date_n_price_ntlist():
  tlist = []
  # elem 1
  pdate = dtfs.make_date_or_none('2013-01-01')
  price = 24.57
  nt = nt_dateprice_constr(date=pdate, price=price)
  tlist.append(nt)
  # elem 2
  pdate = dtfs.make_date_or_none('2013-12-31')
  price = 31.59
  nt = nt_dateprice_constr(date=pdate, price=price)
  tlist.append(nt)
  # elem 3
  pdate = dtfs.make_date_or_none('2023-11-13')
  price = 27.19
  nt = nt_dateprice_constr(date=pdate, price=price)
  tlist.append(nt)
  return tlist


def adhoctest():
  """
  """
  tlist = get_date_n_price_ntlist()
  for nt in tlist:
    print(nt)


def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
