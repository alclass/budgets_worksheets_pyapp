#!/usr/bin/env python3
"""
  docstring

  bcb_api1_nt = coll.namedtuple(
    'BCBAPI1DataStr',
    'cotacao_compra cotacao_venda cotacao_datahora param_date error_msg gen_msg exchanger'
  )


"""
import csv
import os
import xlsxwriter
import fs.datefs.datefunctions as dtfs
import fs.economicfs.preapis_finfunctions as prefs
import fs.economicfs.financefunctions as finfs
import fs.numberfs.tableaufunctions as tblfs
import config


class HistPrice:
  """
  The aim of this class is to monetarily correct a past price
    with its comparison/proportion to foreign currency exchange rates,
    the rate on the price's past date and the rate on the target date (defaulted to today (*)).

  (*) It's defaulted to yesterday depending on time of day or availability.
      Also there is no exchange rates on weekend days and holidays, in theses cases,
      the system looks up a previous available exchange rate.

  In words, the price is index-adjusted by the exchange rate on the origin price's date
   to the one on the target date, defaulted to today (or yesterday).
  It's the abs(origin-target)/origin as a proportion index.

  At the time of writing, this class invokes a db (or API) for BRL-USD/USD rates from BCB data.
  """

  def __init__(self, source_price, source_date,
               saporder=None, target_date=None, source_currency=None, target_currency=None):
    self.source_price = float(source_price)
    self.source_date = source_date
    try:
      self.saporder = int(saporder)
    except ValueError:
      self.saporder = 99999999999  # attribrarily given, it's not processed here & probably does not exist in db
    self.quotes_source_datetime = None
    self.target_date = target_date
    self.quotes_target_datetime = None
    self.source_currency = source_currency  # None means DEFAULT which is, by now, BRL
    self.target_currency = target_currency  # None means DEFAULT which is, by now, USD
    self.source_quote = None  # quote is the exchange rate on a date
    self.target_quote = None
    self._target_price = None  # to be calculated to the same proportional of cotacao_compra_orig/cotacao_compra_dest
    self._monet_corr_index = None
    self.treat_dates()
    self.treat_currency()
    self.fetch_source_n_target_exchange_rates()

  def treat_dates(self):
    self.source_date = dtfs.returns_date_or_none(self.source_date)
    if self.source_date is None:
      error_msg = "Invalid price's source date (%s) for class HistPrice." % str(self.source_date)
      raise ValueError(error_msg)
    self.target_date = dtfs.returns_date_or_today(self.target_date)
    self.quotes_source_datetime = None
    self.quotes_target_datetime = None

  def treat_currency(self):
    if self.source_currency is None:
      self.source_currency = finfs.CURR_BRL  # reais
    if self.source_currency not in finfs.CURRENCIES:
      error_msg = 'Currency %s is not within %s' % (self.source_currency, str(finfs.CURRENCIES))
      raise ValueError(error_msg)
    if self.target_currency is None:
      self.target_currency = finfs.CURR_USD  # dólares
    if self.target_currency not in finfs.CURRENCIES:
      error_msg = 'Currency %s is not within %s' % (self.target_currency, str(finfs.CURRENCIES))
      raise ValueError(error_msg)

  def fetch_source_n_target_exchange_rates(self):
    resbcbapi1 = prefs.dbfetch_bcb_cotacao_compra_dolar_apifallback(self.source_date)
    if resbcbapi1.error_msg:
      raise ValueError(resbcbapi1.error_msg)
    if resbcbapi1.cotacao_compra is None:
      print('resbcbapi1.cotacao_compra is None')
      return
    self.source_quote = resbcbapi1.cotacao_compra
    self.quotes_source_datetime = resbcbapi1.cotacao_datahora
    # self.source_quote_date = resbcbapi1.cotacao_data
    resbcbapi1 = prefs.dbfetch_bcb_cotacao_compra_dolar_apifallback(self.target_date)
    if resbcbapi1.error_msg:
      raise ValueError(resbcbapi1.error_msg)
    if resbcbapi1.cotacao_compra is None:
      print('resbcbapi1.cotacao_compra is None')
      return
    self.target_quote = resbcbapi1.cotacao_compra
    self.quotes_target_datetime = resbcbapi1.cotacao_datahora

  @property
  def target_price(self):
    if self._target_price is None:
      self.fetch_source_n_target_exchange_rates()
    if self.source_quote is None or self.target_quote is None or self.source_quote == 0:
      print('Data unavailable')
      return None
    self._monet_corr_index = abs(self.source_quote - self.target_quote) / self.source_quote
    factor = 1 + self._monet_corr_index
    self._target_price = self.source_price * factor
    return self._target_price

  @property
  def monet_corr_index(self):
    if self._monet_corr_index is None:
      _ = self.target_price  # to trigger fetch routine
      if self._monet_corr_index is None:  # second try, do not retrigger fetch routine at this point
        return None
    return self._monet_corr_index

  def as_dict(self):
    outdict = {
      'source_date': self.source_date,
      'quotes_source_datetime': self.quotes_source_datetime,
      'source_quote': self.source_quote,
      'source_price': self.source_price,
      'saporder': self.saporder,
      'target_date': self.target_date,
      'quotes_target_datetime': self.quotes_target_datetime,
      'target_quote': self.target_quote,
      'target_price': self.target_price,
      'monet_corr_index': self.monet_corr_index,
    }
    return outdict

  def __str__(self):
    outstr = '''
  source_date  = %(source_date)s
  quotes_source_datetime = %(quotes_source_datetime)s,
  source_quote = %(source_quote).4f
  source_price = %(source_price).2f
  saporder = %(saporder)d
  target_date  = %(target_date)s
  quotes_target_datetime = %(quotes_target_datetime)s,
  target_quote = %(target_quote).4f
  target_price = %(target_price).2f
  monet_corr_index = %(monet_corr_index).4f
    ''' % self.as_dict()
    return outstr


class HistPriceWorkbook:

  def __init__(self, histprices, wb_filepath=None):
    self.wb_filepath = wb_filepath
    self.set_wb_filepath()
    self.histprices = histprices
    self.cellref = 'A3'
    self._totalprice = 0
    self.worksheet = None

  def set_wb_filepath(self):
    filename = 'histprices.xlsx'
    if self.wb_filepath is None:
      datafolder_abspath = config.get_datafolder_abspath()
      self.wb_filepath = os.path.join(datafolder_abspath, filename)

  def generate_xlsx(self):
    workbook = xlsxwriter.Workbook(self.wb_filepath)
    self.worksheet = workbook.add_worksheet()
    self.cellref = 'C2'
    self.worksheet.write(self.cellref, 'Preços Históricos')
    self.cellref = 'A5'
    for histpriceitem in self.histprices:
      self.add_row_to_worksheet(histpriceitem)
      self.cellref = tblfs.move_cell_along_tableau(self.cellref, -7, 1)
    print('Closing ', self.wb_filepath)
    workbook.close()

  def add_row_to_worksheet(self, histpriceitem):
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.source_date)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.source_price)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.source_quote)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.target_quote)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.monet_corr_index)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.target_price)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.target_date)

  @property
  def totalprice(self):
    if self._totalprice is not None:
      return self._totalprice
    for hpi in self.histprices:
      self._totalprice += hpi.target_price
    return self._totalprice

  def __str__(self):
    return '<HistPriceWorkbook n_of_rows=%d totalprice=%.2f>' % (len(self.histprices), self.totalprice)


class TripleHistPrice:
  """
    data	        Preço líq.  Nº pedido (int saporder)
    30.07.2013	  2.466,44 	  4505421893
    11.07.2016	  4.454,58 	  4507292659
    (...)

  """

  def __init__(self, dmydotdate=None, commadecimalprice='1,00', saporder=None):
    self.dmydotdate = dmydotdate
    self.commadecimalprice = commadecimalprice
    self.saporder = saporder
    self._pdate = None
    self._dmybardate = None
    self._price = None
    self._histpriceitem = None

  @property
  def dmybardate(self):
    if self._dmybardate is not None:
      return self._dmybardate
    _ = self.pdate  # force first convertion to pdate
    if self.pdate is None:  # can't continue
      return None
    self._dmybardate = dtfs.\
        convert_sep_or_datefields_position_for_ymdstrdate(self.pdate, tosep='/', targetposorder='dmy')
    return self._dmybardate

  @property
  def pdate(self):
    if self.dmydotdate is None:  # needed for the convertion/calculation below
      return
    if self._pdate is not None:
      return self._pdate
    strdate = dtfs.\
        convert_sep_or_datefields_position_for_ymdstrdate(self.dmydotdate, sourceposorder='dmy')
    self._pdate = dtfs.returns_date_or_none(strdate)
    return self._pdate

  @property
  def price(self):
    if self._price is not None:
      return self._price
    strprice = self.commadecimalprice.replace('.', '')
    strprice = strprice.replace(',', '.')
    self._price = float(strprice)
    return self._price

  @property
  def histpriceitem(self):
    if self._histpriceitem is not None:
      return self._histpriceitem
    self._histpriceitem = HistPrice(self.price, self.pdate)

  def as_dict(self):
    outdict = {
      'pricesdate': self.dmybardate,
      'price': self.price,
      'saporder': self.saporder,
    }
    return outdict

  def __str__(self):
    outstr = '''
  pricesdate  = %(pricesdate)s
  price = %(price).2f
  saporder = %(saporder)d
    ''' % self.as_dict()
    outstr += '-'*30
    _ = self.histpriceitem
    outstr += str(self.histpriceitem)
    return outstr


def get_example_adhoctest_data():
  tuplelist = []
  thp = TripleHistPrice('30.07.2013', '2.466,44', 4505421893)
  tuplelist.append(thp)
  thp = TripleHistPrice('11.07.2016', '4.454,58', 4507292659)
  tuplelist.append(thp)
  thp = TripleHistPrice('28.02.2020', '8.865,67', 4510003704)
  tuplelist.append(thp)
  thp = TripleHistPrice('31.03.2020', '5.601,70', 4510087906)
  tuplelist.append(thp)
  return tuplelist


def process_triplehistprices(triplehistprices):
  histprices = []
  for triplehistprice in triplehistprices:
    histprice = HistPrice(
      source_price=triplehistprice.price,
      source_date=triplehistprice.pdate,
      saporder=triplehistprice.saporder,
    )
    histprices.append(histprice)
    # print('-+'*30)
  workbook = HistPriceWorkbook(histprices)
  workbook.generate_xlsx()


def adhoc_test():
  source_price = '100'
  source_date = '2019-12-12'
  hptiem = HistPrice(source_price, source_date)
  print(hptiem)
  print('-'*30)


def read_csv_n_get_triplehistprices():
  filename = 'triplehistprices.csv'
  datafolder_abspath = config.get_datafolder_abspath()
  filepath = os.path.join(datafolder_abspath, filename)
  print('Reading input csv', datafolder_abspath, filepath)
  triplehistprices = []
  with open(filepath, newline='') as csvfp:
    reader = csv.reader(csvfp)  # delimiter = '"' tab = True, sep = comma
    for rowfieldvalues in reader:
      ddmmyyydotdate = rowfieldvalues[0]
      commaprice =  rowfieldvalues[1]
      saporder =  int(rowfieldvalues[2])
      triplehistprice = TripleHistPrice(ddmmyyydotdate, commaprice, saporder)
      triplehistprices.append(triplehistprice)
  return triplehistprices


def process():
  triplehistprices = read_csv_n_get_triplehistprices()
  print('Processing ', len(triplehistprices), 'rows')
  process_triplehistprices(triplehistprices)


if __name__ == "__main__":
  process()
