#!/usr/bin/env python3
"""
fs/datefs/introspect_dates_adhoctest.py
"""
import datetime
import fs.datefs.introspect_dates as intr  # intr.introspect_possible_month_position_in_date


def adhoc_test():
  strdate = '2021-10-21'
  print(strdate, type(strdate), 'introspect_transform_strdate_to_date')
  pdate = intr.introspect_n_convert_strdate_to_date_or_none(strdate, sep=None, positionstr=None)
  print('introspected/transformed', pdate, type(pdate))


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
