#!/usr/bin/env python3
"""
commands/calc/calc_update_prices.py
  calculates prices update using the monet corr multiplication factors from
    commands/calc/calc_monet_corr.py

input: tuple list with dates and prices
output: list (or DataFrame) with at least the updated prices

"""
import datetime
import commands.calc.calc_monet_corr as cmc  # cmc.DoubleDateMonetCorr


class DatePriceList:

  def __init__(self):
    self.today = datetime.date.today()
    self.dateprice_list = data_test()
    self.datelist = []
    self.prices = []
    self.ddmc = None
    self.df = None

  def sort_dateprice_list(self):
    sorted(self.dateprice_list, key=lambda e: e[0])

  def extract_dates_from_dateprice_list(self):
    self.datelist = [d[0] for d in self.dateprice_list]

  def extract_prices_from_dateprice_list(self):
    self.prices = [d[1] for d in self.dateprice_list]

  def process(self):
    self.sort_dateprice_list()
    self.extract_dates_from_dateprice_list()
    print(self.datelist)
    self.ddmc = cmc.DoubleDateMonetCorr(refdate=self.today)
    self.ddmc.calc_monetcorr_bw_datelist_n_refdate(self.datelist)
    self.df = self.ddmc.df
    print(self.df.to_string())

  def report(self):
    self.extract_prices_from_dateprice_list()
    self.df['prices'] = self.prices
    self.df['newprice'] = self.df.prices * self.df.mult
    print(self.df.to_string())


def data_test():
  t = [
        ('24/10/2022', 10.54),
        ('28/04/2023', 11.75),
        ('15/06/2023', 7.34),
  ]
  return t


def adhoctest():
  dpl = DatePriceList()
  dpl.process()
  dpl.report()


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
  adhoctest()
