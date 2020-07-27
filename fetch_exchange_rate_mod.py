#!/usr/bin/env python3
import os, pathlib
import xlsxwriter
import fs.economicfs.financefunctions as finfs

strdatelist = '''
'''

datelist = []
def fetch_cotacao_brl_per_usd_for_datelist():
  quote_n_date_resultlist = finfs.fetch_cotacao_brl_per_usd_for_datelist(datelist)
  for quote_n_date in quote_n_date_resultlist:
    quote, pdate = quote_n_date
    print ('quote =', quote, '| date =', pdate)

def process():
  fetch_cotacao_brl_per_usd_for_datelist()

if __name__ == "__main__":
  process()
