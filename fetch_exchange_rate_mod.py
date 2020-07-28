#!/usr/bin/env python3
import os, pathlib
import xlsxwriter
import fs.economicfs.financefunctions as finfs
import fs.datefs.datefunctions as dtfs

strdatelist = '''
2006-06-19
2019-07-29
'''

datelist = []
def fetch_cotacao_brl_per_usd_for_datelist(datelist):
  quote_n_date_resultlist = finfs.fetch_cotacao_brl_per_usd_for_datelist(datelist)
  for quote_n_date in quote_n_date_resultlist:
    quote, pdate = quote_n_date
    print ('quote =', quote, '| date =', pdate)

def get_datelist():
  datelist = strdatelist.split('\n')
  datelist = list(filter(lambda x : x != '', datelist))
  datelist = list(map(lambda x: dtfs.returns_date_or_None(x), datelist))
  print (datelist)
  return datelist

def process():
  datelist = get_datelist()
  fetch_cotacao_brl_per_usd_for_datelist(datelist)

if __name__ == "__main__":
  process()
