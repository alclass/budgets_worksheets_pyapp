#!/usr/bin/env python3
import os, pathlib
import xlsxwriter
import fs.economicfs.financefunctions as finfs
import fs.datefs.datefunctions as dtfs

_ = '''
07/08/2020
07/10/2020
06/11/2019
'''
strdatelist = '''
2020-7-8
2020-7-10
2019-6-11
'''
strdatelist = '''
19/6/2006
29/7/2019
'''

def get_datelist():
  datelist = strdatelist.split('\n')
  datelist = map(lambda x : x.strip(' \t\n'), datelist)
  datelist = list(filter(lambda x : x != '', datelist))
  # the line below only works for the y-m-d pos-&-sep case
  # datelist = dtfs.prepare_datelist_uniq_n_in_desc_order(datelist)
  return datelist

def batch_convert_dates():
  datelist = get_datelist()
  for strdate in datelist:
    tosep = '-'; inposorder = 'dmy'; outposorder = 'ymd'
    ostrdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate, tosep, inposorder, outposorder)
    print (ostrdate)

def process():
  batch_convert_dates()

if __name__ == "__main__":
  process()
