#!/usr/bin/env python3
"""
commands/fetch/bcb_br/fetch_exchangerate_with_datefile.py
jetbrains://pycharm/navigate/reference?project=local_settings.py&path=commands%2Ffetch%2Fbcb%2Ffetch_exchangerate_with_datefile.py

"""
import fs.datefs.read_write_datelist_files_cls as rw


class ExchangeRateOnDateFetcher:
  """
  This class organizes fetching Exchange Rates on dates stored in a text file
  """

  def __init__(self):
    self.datesreader = None

  def read_dates_from_files(self):
    self.datesreader = rw.DateFileReaderWriter()

  def fetch_exchange_rate_date_on_date(self):
    for pdate in self.datesreader.get_n_store_pydates_converting_textfile_w_sep_n_posorder():
      # go fetch exc-rat on date
      scrmsg = f"{pdate} => 1.0"
      print(scrmsg)

  def process(self):
    self.read_dates_from_files()
    self.fetch_exchange_rate_date_on_date()


def process():
  erdf = ExchangeRateOnDateFetcher()
  erdf.process()


if __name__ == "__main__":
  process()
