import datetime
import math
import random
import collections
import fs.datefs.read_write_datelist_files as daterw
import commands.calc.calc_monet_corr as cmc  # cmc.MonetCorrCalculator
date_price_ntconstr = collections.namedtuple('NTDateNPrice', field_names=['date', 'price'])


def make_ntlist_dates_n_random_prices_from_datesfile(datesfilepath=None):
  dtrw = daterw.DateFileReaderWriter(datesfilepath)
  ntlist = []
  for pdate in dtrw.gen_dates_converting_one_by_one():
    price = random.random() * 100
    price = round(price, 2)
    scrline = f"{pdate} | {price} "
    print(scrline)
    nt = date_price_ntconstr(date=pdate, price=price)
    ntlist.append(nt)
  return ntlist


def adhoctest():
  ntlist = make_ntlist_dates_n_random_prices_from_datesfile()
  print('='*30)
  for nt in ntlist:
    print(nt)
  today = datetime.date.today()
  cmcalc = cmc.DatePriceRecordsMonetCorrCalculator(today)
  cmcalc.set_dates_n_prices_ntlist(ntlist)
  cmcalc.update_prices()




def process():
  """
  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoctest()
