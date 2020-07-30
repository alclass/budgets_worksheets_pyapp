#!/usr/bin/env python3
'''

'''
import xlsxwriter
import fs.datefs.datefunctions as dtfs
import fs.economicfs.apis_finfunctions as apis
import fs.economicfs.financefunctions as finfs

class HistPriceItem:
  '''
  The aim of this class is to monetarily correct a past price
    with its comparison to foreign currency exchange rates,
    the rate on the price's past date and the rate on the target date (defaulted to today (*)).
  (*) It's defaulted to yesterday depending on time of day or availability.
      Also there is no exchange rates on weekend days and holidays, in theses cases,
      the system looks up a previous available exchange rate.

  In words, the price is index-adjusted by the exchange rate on the origin price's date
   to the one on the target date, defaulted to today (or yesterday).

  At the time of writing, this class only works for USD as a BRL-USD open API from BCB is in use.
  '''

  def __init__(self, source_price, source_date, target_date=None, source_currency=None, target_currency=None):
    self.source_price = float(source_price)
    self._target_price = None
    self._monet_corr_index = None
    self.source_date = source_date
    self.target_date = target_date
    self.source_quote = None # quote is the exchange rate on a date
    self.target_quote = None
    self.source_currency  = source_currency # None means DEFAULT which is, by now, BRL
    self.target_currency  = target_currency # None means DEFAULT which is, by now, USD
    self.treat_dates()
    self.treat_currency()
    self.fetch_source_n_target_exchange_rates()

  def treat_dates(self):
    self.source_date = dtfs.returns_date_or_None(self.source_date)
    if self.source_date is None:
      error_msg = "Invalid price's source date (%s) for class HistPriceItem." %str(self.source_date)
      raise ValueError(error_msg)
    self.target_date = dtfs.returns_date_or_today(self.target_date)
    self.source_quote_date = None
    self.target_quote_date = None

  def treat_currency(self):
    if self.source_currency is None:
      self.source_currency = finfs.CURR_BRL # reais
    if self.source_currency not in finfs.CURRENCIES:
      error_msg = 'Currency %s is not within %s' %(self.source_currency, str(finfs.CURRENCIES))
      raise ValueError(error_msg)
    if self.target_currency is None:
      self.target_currency = finfs.CURR_USD # dólares
    if self.target_currency not in finfs.CURRENCIES:
      error_msg = 'Currency %s is not within %s' %(self.target_currency, str(finfs.CURRENCIES))
      raise ValueError(error_msg)

  def fetch_source_n_target_exchange_rates(self):
    _, cotacao, cotacaoData = apis.call_api_bcb_cotacao_dolar_on_date(self.source_date)
    self.source_quote = cotacao
    self.source_quote_date = cotacaoData
    _, cotacao, cotacaoData = apis.call_api_bcb_cotacao_dolar_on_date(self.target_date)
    if cotacao is not None and cotacao.lower().startswith('error'):
      error_msg = cotacao
      raise IOError(error_msg)
    self.target_quote = cotacao
    self.target_quote_date = cotacaoData

  @property
  def target_price(self):
    if self._target_price is None:
      self.fetch_source_n_target_exchange_rates()
    if self.source_quote is None or self.target_quote is None or self.source_quote == 0:
      return None
    self._monet_corr_index = abs(self.source_quote - self.target_quote) / self.source_quote
    factor = 1 + self._monet_corr_index
    self._target_price = self.source_price * factor
    return self._target_price

  @property
  def monet_corr_index(self):
    if self._monet_corr_index is None:
      _ = self.target_price
      if self._monet_corr_index is None:
        return None
    return self._monet_corr_index

  def as_dict(self):
    outdict = {}
    outdict['source_date'] = self.source_date
    outdict['source_price'] = self.source_price
    outdict['source_quote'] = self.source_quote
    outdict['target_quote'] = self.target_quote
    outdict['monet_corr_index'] = self.monet_corr_index
    outdict['target_price'] = self.target_price
    outdict['target_date'] = self.target_date
    return outdict

  def __str__(self):
    outstr = '''
  source_date  = %(source_date)s
  source_price = %(source_price).2f
  source_quote = %(source_quote)s
  target_quote = %(target_quote)s
  monet_corr_index = %(monet_corr_index).4f
  target_price = %(target_price).2f
  target_date  = %(target_date)s
    ''' %self.as_dict()
    return outstr

class HistPriceList:

  def __init__(self, datedprices):
    self.datedprices = datedprices

  def generate_xlsx(self):
    workbook = xlsxwriter.Workbook('hello.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Hello world')
    workbook.close()

  def add_row_to_worksheet(self,
      source_date,
      source_price,
      source_quote,
      target_quote,
      monet_corr_index,
      target_price,
      target_date,
    ):
    pass

  def process(self):
    for datedprice in self.datedprices:
      source_price, source_date = datedprice
      hpitem = HistPriceItem(source_price, source_date)
      self.add_row_to_worksheet(
        source_date,
        source_price,
        hpitem.source_quote,
        hpitem.target_quote,
        hpitem.monet_corr_index,
        hpitem.target_price,
        hpitem.target_date,
      )

  def __str__(self):
    return 'HistPriceList'

def adhoc_test():
  dates = []
  source_price = '100'
  source_date = '2019-12-12'
  hptiem = HistPriceItem(source_price, source_date)
  print (hptiem)

def process():
  # HistPriceItem()
  adhoc_test()


if __name__ == "__main__":
  process()
