#!/usr/bin/env python3
"""
models/exrate/histprices_mod.py

The namedtuple for the BCB API response data is the following:
  namedtuple_bcb_api1 = coll.namedtuple(
    'BCBAPI1DataStr',
    'cotacao_compra cotacao_venda cotacao_datahora param_date error_msg gen_msg exchanger'
  )
import xlsxwriter
import fs.numberfs.tableaufunctions as tblfs
"""
import csv
import datetime
import os
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import fs.datefs.introspect_dates as intr
import fs.economicfs.bcb.bcb_financefunctions as finfs
import commands.calc.multiplication_factor_calc as mfc  # .MonetCorrCalculator
import settings as sett


class HistPrice:
  """
  The aim of this class is to monetarily correct a past price
    with its comparison/proportion to foreign currency exchange rates,
    the rate on the price's past date and the rate on the target date (defaulted to today (*)).

  (*) It's defaulted to yesterday depending on time of day or availability.
      Also, there is no exchange rates on weekend days and holidays, in these cases,
      the system looks up a previous available exchange rate.

  In words, the price is index-adjusted by the exchange rate on the origin price's date
   to the one on the target date, defaulted to today (or yesterday).
  It's the abs(origin-target)/origin as a proportion index.

  At the time of writing, this class invokes a db (or API) for BRL-USD/USD rates from BCB data.
  """

  def __init__(
      self, price_ini, date_ini, date_fim=None,
      sap_order=None, curr_numerator=None, curr_denominator=None
  ):
    self.price_ini = float(price_ini)
    self._price_fim = None  # to be calculated to the same proportional of cotacao_compra_orig/cotacao_compra_dest
    self.date_ini = date_ini
    try:
      self.sap_order = int(sap_order)
    except (TypeError, ValueError):
      self.sap_order = 99999999999  # attribrarily given, it's not processed here & probably does not exist in db
    self.quotes_ini_dt = None
    self.quotes_fim_dt = None
    self.date_fim = date_fim
    self._mcc = None
    self.curr_numerator = curr_numerator  # None means DEFAULT which is, by now, BRL
    self.curr_denominator = curr_denominator  # None means DEFAULT which is, by now, USD
    self.treat_dates()
    self.treat_currency()
    _ = self.mcc  # self.enclose_mul_fac_obj()
    # self.fetch_source_n_target_exchange_rates()
    # self.fetch_source_n_target_cpis()

  @property
  def n_days(self):
    try:
      return self.mcc.n_days
    except TypeError:
      pass
    return -1

  @property
  def exrate_ini(self):
    try:
      return self.mcc.exrate_ini
    except TypeError:
      pass
    return None

  @property
  def exrate_fim(self):
    try:
      return self.mcc.exrate_fim
    except TypeError:
      pass
    return None

  @property
  def cpi_ini(self):
    try:
      return self.mcc.cpi_ini
    except TypeError:
      pass
    return None

  @property
  def cpi_fim(self):
    try:
      return self.mcc.cpi_fim
    except TypeError:
      pass
    return None

  @property
  def mcc(self):
    if self._mcc is None:
      self._mcc = mfc.MonetCorrCalculator(self.date_ini, self.date_fim)
    return self._mcc

  def treat_dates(self):
    self.date_ini = cnv.make_date_or_none(self.date_ini)
    if self.date_ini is None:
      # second try: extract date from the dot separated strdate (dd.mm.yyyy)
      # this date dmy dot-format is expected in the csv input files
      self.date_ini = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(self.date_ini, sep='.', orderpos='dmy')
      if self.date_ini is None:
        error_msg = "Invalid price's source date (%s) for class HistPrice." % str(self.date_ini)
        raise ValueError(error_msg)
    self.date_fim = cnv.make_date_or_today(self.date_fim)
    if self.date_fim == datetime.date.today():
      # prefer yesterday, for today's exchange rate depends on the hour rate as 'closed'
      self.date_fim = self.date_fim - datetime.timedelta(days=1)
    self.quotes_ini_dt = None
    self.quotes_fim_dt = None

  def treat_currency(self):
    if self.curr_numerator is None:
      self.curr_numerator = finfs.CURR_BRL  # reais
    if self.curr_numerator not in finfs.CURRENCIES:
      error_msg = 'Currency %s is not within %s' % (self.curr_numerator, str(finfs.CURRENCIES))
      raise ValueError(error_msg)
    if self.curr_denominator is None:
      self.curr_denominator = finfs.CURR_USD  # dólares
    if self.curr_denominator not in finfs.CURRENCIES:
      error_msg = 'Currency %s is not within %s' % (self.curr_denominator, str(finfs.CURRENCIES))
      raise ValueError(error_msg)

  @property
  def price_fim(self):
    if self._price_fim is None:
      try:
        self._price_fim = self.price_ini * self.monecorr_mul_fac
      except TypeError:
        pass
    return self._price_fim

  @property
  def monecorr_mul_fac(self):
    try:
      return self.mcc.multiplication_factor
    except TypeError:
      pass
    return None

  def as_dict(self):
    outdict = {
      'source_date': self.date_ini,
      'quotes_source_datetime': self.quotes_ini_dt,
      'source_quote': self.exrate_ini,
      'source_price': self.price_ini,
      'saporder': self.sap_order,
      'target_date': self.date_fim,
      'quotes_target_datetime': self.quotes_fim_dt,
      'target_quote': self.exrate_fim,
      'target_price': self.price_fim,
      'monet_corr_index': self.monecorr_mul_fac,
    }
    return outdict

  def __str__(self):
    outstr = f'''
  saporder = {self.sap_order}
  quotes_source_datetime = {self.quotes_ini_dt}
  quotes_target_datetime = {self.quotes_fim_dt}
  date_ini  = {self.date_ini} | cpi_i = {self.cpi_ini}
  date_fim  = {self.date_fim} | cpi_f = {self.cpi_fim}
  price_ini = {self.price_ini:02f} | exr_i = {self.exrate_ini:04f} 
  price_fim = {self.price_fim:02f} | exr_f = {self.exrate_fim:04f}
  mul_fac = {self.monecorr_mul_fac:04f} | days = {self.n_days}
    '''
    return outstr


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
    self._dmybardate = intr.trans_from_date_to_strdate_w_sep_posorder_n_zfill(
      self.pdate, sep='/', posorder='dmy', zfill=2
    )
    return self._dmybardate

  @property
  def pdate(self):
    if self._pdate is not None:
      return self._pdate
    if self.dmydotdate is None:  # needed for the convertion/calculation below
      return
    self._pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(
        strdate=self.dmydotdate, sep='.', orderpos='dmy'
    )
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
    self._histpriceitem = HistPrice(price_ini=self.price, date_ini=self.pdate)

  def as_dict(self):
    outdict = {
      'pricesdate': self.dmybardate,
      'price': self.price,
      'saporder': self.saporder,
    }
    return outdict

  def __str__(self):
    outstr = f""""""'''
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


def read_csv_n_get_triplehistprices(pdelimiter='\t'):
  filename = 'triplehistprices.csv'
  datafolder_abspath = sett.get_datafolder_abspath()
  filepath = os.path.join(datafolder_abspath, filename)
  print('Reading input csv', datafolder_abspath, filepath)
  triplehistprices = []
  with open(filepath, newline='') as csvfp:
    reader = csv.reader(csvfp, delimiter=pdelimiter)  # delimiter = '"' tab = True, sep = comma
    for rowfieldvalues in reader:
      try:
        ddmmyyydotdate = rowfieldvalues[0]
        commaprice = rowfieldvalues[1]
        saporder = int(rowfieldvalues[2])
        triplehistprice = TripleHistPrice(ddmmyyydotdate, commaprice, saporder)
        triplehistprices.append(triplehistprice)
      except IndexError as e:
        if pdelimiter == ';':
          raise IndexError(e)
        return read_csv_n_get_triplehistprices(pdelimiter=';')
  return triplehistprices


def adhoc_test():
  source_price = '100'
  source_date = '2019-12-12'
  hptiem = HistPrice(source_price, source_date)
  print(hptiem)
  print('-'*30)


def process():
  pass


if __name__ == "__main__":
  process()
  adhoc_test()