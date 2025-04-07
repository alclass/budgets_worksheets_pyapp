#!/usr/bin/env python3
"""
commands/calc/cpi/adhoctests/datamass_for_multfactortable.py

This script contains just an adhoc-test function that:

 1) creates a namedtuple with fields: date and price
 2) date initially is a string and get transformed into a pythondate
    an external function does that (string date to pythondate)
 3) price here is just a float number (it may become a Price-like type in the future)
 4) appends some namedtuples to a list
 5) returns this namedtuple items list

"""
import collections
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
nt_dateprice_constr = collections.namedtuple('NTDeP', field_names=['date', 'price'])


def adhoctest_get_date_n_price_ntlist():
  tlist = []
  # elem 1
  pdate = cnv.make_date_or_none('2025-01-01')
  price = 4.57
  nt = nt_dateprice_constr(date=pdate, price=price)
  tlist.append(nt)
  # elem 2
  pdate = cnv.make_date_or_none('2013-12-31')
  price = 31.12
  nt = nt_dateprice_constr(date=pdate, price=price)
  tlist.append(nt)
  # elem 3
  pdate = cnv.make_date_or_none('2023-11-13')
  price = 13.11
  nt = nt_dateprice_constr(date=pdate, price=price)
  tlist.append(nt)
  # elem 4
  pdate = cnv.make_date_or_none('2019-11-13')
  price = 27.19
  nt = nt_dateprice_constr(date=pdate, price=price)
  tlist.append(nt)
  tlist.sort(key=lambda x: x.date)
  return tlist


def adhoctest():
  """
  """
  tlist = adhoctest_get_date_n_price_ntlist()
  for i, nt in enumerate(tlist):
    seq = i + 1
    print(seq, nt)
  for i, nt in enumerate(tlist):
    seq = i + 1
    print(seq, 'date', nt.date, 'price', nt.price)


def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
