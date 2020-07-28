#!/usr/bin/env python3
import os, pathlib
import xlsxwriter
'''

'''
import fs.economicfs.financefunctions as finfs

class HistPriceItem:
  '''
  This class is planned to receive either a USD or a EUR foreign_netprice value.
  Then, it attempts to fetch the exchange rate on the price's recorded date (pricedate).
  '''

  def __init__(self, foreign_netprice, pricedate, ordernum, currency=None):
    self.foreign_netprice  = foreign_netprice
    self.pricedate = pricedate
    self.ordernum  = ordernum
    self.currency  = currency # None means DEFAULT which is, by now, USD
    self._brlnetprice = None
    self.treat_currency()

  def treat_currency(self):
    if self.currency is None:
      self.currency = finfs.DEFAULT_CURRENCY
    if self.currency not in finfs.CURRENCIES:
      error_msg = 'Currency %s is not within %s' %(self.currency, str(finfs.CURRENCIES))
      raise ValueError(error_msg)
    if self.currency == finfs.CURR_BRL:
      self._brlnetprice = self.foreign_netprice

  def get_currency_in_brl(self):
    if self._brlnetprice:
      return self._brlnetprice
    if self.currency == finfs.CURR_BRL:
      self._brlnetprice = self.foreign_netprice
    elif self.currency == finfs.CURR_EUR:
      self._brlnetprice = finfs.convert_fromto_currency(self.foreign_netprice, currfrom=self.currency, currto=finfs.CURR_BRL)
    elif self.currency == finfs.CURR_USD:
      self._brlnetprice = finfs.convert_fromto_currency(self.foreign_netprice, currfrom=self.currency, currto=finfs.CURR_BRL)
    return self.foreign_netprice

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
