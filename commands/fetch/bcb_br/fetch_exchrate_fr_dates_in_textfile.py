#!/usr/bin/env python3
"""
commands/fetch/bcb_br/fetch_exchangerate_with_datefile.py

jetbrains://pycharm/navigate/reference?project=local_settings.py&path=commands%2Ffetch%2Fbcb%2Ffetch_exchangerate_with_datefile.py

"""
import fs.datefs.read_write_datelist_files_cls as rw
import settings as sett
import os
BRL_3LETTER_CURR = 'BRL'
USD_3LETTER_CURR = 'USD'
REGISTERED_CURRENCIES_3LETTER = [BRL_3LETTER_CURR, USD_3LETTER_CURR]
DEFAULT_DATES_FILENAME = 'dates.txt'


class BCBExchangeRatesFromDatesFileFetcher:
  """
  This class organizes fetching Exchange Rates on dates stored in a text file
  """

  def __init__(self, curr_fr=None, curr_to=None, datafolderpath=None, datafilename=None, p_datafilepath=None):
    self.curr_fr, self.curr_to = curr_fr, curr_to
    self.datafolderpath, self.datafilename, self.p_datafilepath = datafolderpath, datafilename, p_datafilepath
    self.datesreader = None
    self.treat_attrs()

  def treat_attrs(self):
    """
    Obs:
      p_datafilepath is just used if given and existing and, if so, overrides datafolderpath and/or datafilename
    """
    if self.curr_fr is None or self.curr_fr not in REGISTERED_CURRENCIES_3LETTER:
      self.curr_fr = USD_3LETTER_CURR
    if self.curr_to is None or self.curr_to not in REGISTERED_CURRENCIES_3LETTER:
      if self.curr_to != BRL_3LETTER_CURR:
        self.curr_to = BRL_3LETTER_CURR
      else:
        self.curr_to = USD_3LETTER_CURR
    if self.datafolderpath is None or not os.path.isdir(self.datafolderpath):
      self.datafolderpath = sett.get_datafolder_abspath()
    if self.datafilename is None:
      self.datafilename = DEFAULT_DATES_FILENAME
    if self.p_datafilepath is None:
      return
    if os.path.isfile(self.p_datafilepath):
      # override folderpath and filename if given previously
      folderpath, filename = os.path.split(self.p_datafilepath)
      self.datafolderpath = folderpath
      self.datafilename = filename

  @property
  def datafilepath(self):
    return os.path.join(self.datafolderpath, self.datafilename)

  def read_dates_from_files(self):
    self.datesreader = rw.DateFileReaderWriter(self.datafilepath)

  def fetch_exchange_rate_date_on_date(self):
    """
    get_n_store_pydates_converting_textfile_w_sep_n_posorder()
    """
    for pdate in self.datesreader.gen_n_dont_store_pydates_converting_textfile_w_sep_n_posorder():
      # go fetch exc-rat on date
      scrmsg = f"{pdate} => 1.0"
      print(scrmsg)

  def process(self):
    self.read_dates_from_files()
    self.fetch_exchange_rate_date_on_date()


def process():
  erdf = BCBExchangeRatesFromDatesFileFetcher()
  erdf.process()


if __name__ == "__main__":
  process()
