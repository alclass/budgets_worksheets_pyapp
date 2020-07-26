#!/usr/bin/env python3
import os, pathlib
import xlsxwriter
'''

'''
import fs.economicfs.financefunctions as finfs
finfs.CURR_BRL

DEFAULT_CURRENCY = CURR_BRL
class HistPriceItem:

  def __init__(self, pricedate, netprice, ordernum, currency=None):
    self.pricedate, self.netprice, self.ordernum = pricedate, netprice, ordernum
    self.currency = currency
    self._brlnetprice = None
    self.treat_currency()

  def treat_currency(self):
    if self.currency is None:
      self.currency = DEFAULT_CURRENCY
    if self.currency not in CURRENCIES:
      error_msg = 'Currency %s is not within %s' %(self.currency, str(CURRENCIES))
      raise ValueError(error_msg)

  def get_currency_in_brl(self):
    if self._brlnetprice:
      return self._brlnetprice
    if self.currency == CURR_BRL:
      self._brlnetprice = self.netprice
    elif self.currency == CURR_EUR:
      self._brlnetprice = convert_fromto_currency(origvalue, currfrom=self.currency, currto='BRL')
    elif self.currency == CURR_USD:
      self._brlnetprice = convert_fromto_currency(origvalue, currfrom=self.currency, currto='BRL')
    return self.netprice


class HistPriceList:

  def __init__(self, items):
    self.items = items



  def generate_xlsx(self):
    workbook = xlsxwriter.Workbook('hello.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Hello world')
    workbook.close()

def process():
  HistPriceItem()

if __name__ == "__main__":
  process()
