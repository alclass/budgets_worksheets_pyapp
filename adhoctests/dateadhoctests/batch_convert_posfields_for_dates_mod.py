#!/usr/bin/env python3
"""
batch_convert_posfields_for_dates_mod.py

"""
# import os, pathlib
# import xlsxwriter
# import fs.economicfs.financefunctions as finfs
import fs.datefs.datefunctions as dtfs


def get_datelist(datestext):
  """

  """
  if datestext is None:
    return []
  datestext = str(datestext)
  for c in ['\n', '\r', '\t']:
    datestext = datestext.replace(c, ' ')
  datelist = datestext.split(' ')
  datelist = list(filter(lambda x: x != '', datelist))
  # the line below only works for the y-m-d pos-&-sep case
  # datelist = dtfs.prepare_datelist_uniq_n_in_desc_order(datelist)
  return datelist


def batch_convert_dates(datelist):
  for i, strdate in enumerate(datelist):
    tosep = '-'
    input_pos_order = 'dmy'
    output_pos_order = 'ymd'
    ostrdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(
      strdate, tosep, input_pos_order, output_pos_order
    )
    seq = i + 1
    print(seq, strdate, '=>', ostrdate)


def get_test_data():
  strdateslist = []
  line = '07/08/2020   07/10/2020   06/11/2019'
  strdateslist.append(line)
  line = '2020-7-8   2020-7-10   2019-6-11'
  strdateslist.append(line)
  line = '19/6/2006   29/7/2019'
  strdateslist.append(line)
  line = '07/08/2020 07/10/2020 06/11/2019'
  strdateslist.append(line)
  line = '2020-7-8 2020-7-10 2019-6-11'
  strdateslist.append(line)
  line = '19-6-2006  29/7/2019'
  strdateslist.append(line)
  datestext = ' '.join(strdateslist)  # datestext will not have a \n
  datelist = get_datelist(datestext)
  return datelist


def adhoctest():
  datelist = get_test_data()
  print(datelist)
  batch_convert_dates(datelist)


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoctest()
