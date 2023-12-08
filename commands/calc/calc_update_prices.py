#!/usr/bin/env python3
"""
commands/calc/calc_update_prices.py
  calculates prices update using the monet corr multiplication factors from
    commands/calc/calc_monet_corr.py

input: tuple list with dates and prices
output: list (or DataFrame) with at least the updated prices

"""
import collections
import datetime
import commands.calc.calc_monet_corr as cmc  # cmc.DatePriceRecordsMonetCorrCalculator
price_rec_constr = collections.namedtuple(
  'PriceRecord', field_names=['rid', 'date', 'price', 'descr', 'obs', 'ref']
)


def get_test_data():
  records = []
  #
  seq = 1
  rid, date, price, descr, obs, ref = seq, '2023-1-1', 24.34, 'pencil smart', None, None
  price_rec = price_rec_constr(rid=rid, date=date, price=price, descr=descr, obs=obs, ref=ref)
  records.append(price_rec)
  #
  seq += 1
  rid, date, price, descr, obs, ref = seq, '2022-12-12', 44.15, 'office pencial rubber', None, None
  price_rec = price_rec_constr(rid=rid, date=date, price=price, descr=descr, obs=obs, ref=ref)
  records.append(price_rec)
  #
  seq += 1
  rid, date, price, descr, obs, ref = seq, '2023-5-4', 23.77, 'plastic box', None, None
  price_rec = price_rec_constr(rid=rid, date=date, price=price, descr=descr, obs=obs, ref=ref)
  records.append(price_rec)
  return records


class DatePriceList:

  def __init__(self):
    self.today = datetime.date.today()
    self.dates = []
    self.records = []
    self.prices = []
    self.ddmc = None
    self.df = None

  def sort_records_by_date(self):
    sorted(self.records, key=lambda e: e.date)

  def extract_dates_from_dateprice_list(self):
    self.dates = [d.date for d in self.records]

  def extract_prices_from_dateprice_list(self):
    self.prices = [d.price for d in self.records]

  def process(self):
    self.sort_records_by_date()
    self.extract_dates_from_dateprice_list()
    print(self.dates)
    self.ddmc = cmc.DatePriceRecordsMonetCorrCalculator(refdate=self.today)
    self.ddmc.calc_monetcorr_w_datelist_n_refdate(self.dates)
    self.df = self.ddmc.df
    print(self.df.to_string())

  def report(self):
    self.extract_prices_from_dateprice_list()
    self.df['prices'] = self.prices
    self.df['newprice'] = self.df.prices * self.df.mult
    print(self.df.to_string())


def adhoctest2():
  records = get_test_data()
  for rec in records:
    print(rec)


def adhoctest():
  dpl = DatePriceList()
  dpl.process()
  dpl.report()


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest()
  process()
  """
  adhoctest2()
