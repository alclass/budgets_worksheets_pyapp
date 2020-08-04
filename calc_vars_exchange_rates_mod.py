#!/usr/bin/env python3
import sys
import models.exchange_rate_modelmod as mmod
import models.conn_sa as con
import fs.economicfs.preapis_finfunctions as preapi
import fs.datefs.datefunctions as dtfs


class MinMax:

  def __init__(self):
    self.minbuy = sys.maxsize
    self.maxbuy = -sys.maxsize
    self.minsell = sys.maxsize
    self.maxsell = -sys.maxsize
    self.minbuydate = None
    self.maxbuydate = None
    self.minselldate = None
    self.maxselldate = None

  def find_min_max_n_dates(self, exchanger):
    """
    , minbuy, minsell, maxbuy, maxsell, minbuydate, minselldate, maxbuydate, maxselldate
    :return:
    """
    if exchanger.buyquote < self.minbuy:
      self.minbuy = exchanger.buyquote
      self.minbuydate = exchanger.quotesdate
    if exchanger.sellquote < self.minsell:
      self.minsell = exchanger.buyquote
      self.minselldate = exchanger.quotesdate
    if exchanger.buyquote > self.maxbuy:
      self.maxbuy = exchanger.buyquote
      self.maxbuydate = exchanger.quotesdate
    if exchanger.sellquote > self.maxsell:
      self.maxsell = exchanger.sellquote
      self.maxselldate = exchanger.quotesdate
    return

  @property
  def buy_variation(self):
    return calculate_fraction_variation(self.minbuy, self.maxbuy)

  @property
  def sell_variation(self):
    return calculate_fraction_variation(self.minsell, self.maxsell)

  def as_dict(self):
    odict = {
      'minbuy': self.minbuy,
      'maxbuy': self.maxbuy,
      'minsell': self.minsell,
      'maxsell': self.maxsell,
      'minbuydate': self.minbuydate,
      'maxbuydate': self.maxbuydate,
      'minselldate': self.minselldate,
      'maxselldate': self.maxselldate,
      'buy_variation': self.buy_variation,
      'sell_variation': self.sell_variation,
    }
    return odict

  def __str__(self):
    outstr = '''
minbuy  = %(minbuy).4f on minbuydate  = %(minbuydate)s
minsell = %(minsell).4f on minselldate = %(minselldate)s
maxbuy  = %(maxbuy).4f on maxbuydate  = %(maxbuydate)s
maxsell = %(maxsell).4f on maxselldate = %(maxselldate)s
buy_var = %(buy_variation).2f & sell_var = %(sell_variation).2f  
    ''' % self.as_dict()
    return outstr


def list_min_max(inidate, findate):
  session = con.Session()
  minmax = MinMax()
  for pdate in dtfs.generate_daterange(inidate, findate):
    exchanger = session.query(mmod.ExchangeRateDate).filter(mmod.ExchangeRateDate.quotesdate == pdate).first()
    if exchanger is None or exchanger.buyquote is None:
      continue
    minmax.find_min_max_n_dates(exchanger)
  print (minmax)


def calculate_fraction_variation(n1, n2):
  return abs(n1-n2)/n1

def calculate_var_inidate_to_findate(inidate, findate):
  """

  :param inidate:
  :param findate:
  :return:
  """
  ini_res_bcb_api1 = preapi.dbfetch_bcb_cotacao_compra_dolar_apifallback(inidate)
  fin_res_bcb_api1 = preapi.dbfetch_bcb_cotacao_compra_dolar_apifallback(findate)
  buyincrease = None
  sellincrease = None
  try:
    ini_buyquote = ini_res_bcb_api1.exchanger.buyquote
    fin_buyquote = fin_res_bcb_api1.exchanger.buyquote
    buyincrease = calculate_fraction_variation(ini_buyquote, fin_buyquote)
  except AttributeError:
    pass
  try:
    ini_sellquote = ini_res_bcb_api1.exchanger.sellquote
    fin_sellquote = fin_res_bcb_api1.exchanger.sellquote
    sellincrease = abs(ini_sellquote - fin_sellquote) / ini_sellquote
  except AttributeError:
    pass
  return buyincrease, sellincrease


def form_percent_str(fraction):
  percent = fraction*100
  return '%.2f%%' % percent


def adhoc_test():
  inidate = '2017-01-01'
  findate = '2017-12-31'
  buyincrease, sellincrease = calculate_var_inidate_to_findate(inidate, findate)
  print('buyincrease', form_percent_str(buyincrease))
  print('sellincrease', form_percent_str(sellincrease))
  inidate = '2018-01-01'
  findate = '2018-12-31'
  buyincrease, sellincrease = calculate_var_inidate_to_findate(inidate, findate)
  print('buyincrease', form_percent_str(buyincrease))
  print('sellincrease', form_percent_str(sellincrease))
  inidate = '2019-01-01'
  findate = '2019-12-31'
  buyincrease, sellincrease = calculate_var_inidate_to_findate(inidate, findate)
  print('buyincrease', form_percent_str(buyincrease))
  print('sellincrease', form_percent_str(sellincrease))


def adhoc_test2():
  inidate = '2016-01-01'
  findate = '2016-12-31'
  list_min_max(inidate, findate)
  inidate = '2017-01-01'
  findate = '2017-12-31'
  list_min_max(inidate, findate)
  inidate = '2018-01-01'
  findate = '2018-12-31'
  list_min_max(inidate, findate)
  inidate = '2019-01-01'
  findate = '2019-12-31'
  list_min_max(inidate, findate)
  inidate = '2020-01-01'
  findate = '2020-05-31'
  list_min_max(inidate, findate)

def process():
  adhoc_test2()

if __name__ == "__main__":
  process()
