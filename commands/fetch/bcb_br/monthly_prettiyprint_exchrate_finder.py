"""
BCBMonthlyPrettiyPrintFinder
"""
import os
import re
import settings as sett
from models.budgets.pb.join_via_pandas_excelfiles_as_sheets_in_one import folderpath
import fs.datefs.refmonths_mod as rmd
repatt_year_ending_str = r'.+(?P<year>\d{4})$'
recmpl_repatt_year_ending_str = re.compile(repatt_year_ending_str)
re_patt_exchangerate_datafilename =\
  r"^(?P<yearmonth>\d{4}\-\d{2})\s{1}(?P<currs_num_den_w_uline>[A-Z]{3}_[A-Z]{3}) exchange rates\.txt$"
re_cmpld_exchangerate_datafilename = re.compile(re_patt_exchangerate_datafilename)
tointerpol_exchangerate_datafilename = \
  '{yearmonth} {currnum_currden} exchange rates.txt'


class BCBMonthlyPrettiyPrintFinder:

  bcb_datafoldername = 'bcb_indices'

  def __init__(
      self,
      datafolderpath: os.path = None,
      curr_fr: str = None,
      curr_to: str = None,
    ):
    self.datafolderpath = datafolderpath
    self.years = None
    self.curr_fr = curr_fr
    self.curr_to = curr_to
    self.treat_attrs()

  def treat_attrs(self):
    if self.datafolderpath is None or not os.path.isdir(folderpath):
      self.datafolderpath = sett.get_datafolder_abspath()

  @property
  def bcb_datafolderpath(self):
    dtfopath = os.path.join(self.datafolderpath, self.bcb_datafoldername)
    os.makedirs(dtfopath, exist_ok=True)
    return dtfopath

  @property
  def year_min(self):
    if self.years is None:
      return None
    return min(self.years)

  @property
  def year_max(self):
    if self.years is None:
      return None
    return max(self.years)

  @property
  def year_range(self):
    if self.years is None:
      return None, None
    return self.year_min, self.year_max

  def get_folderpath_for_year(self, year):
    return os.path.join(self.bcb_datafolderpath, str(year))

  def find_monthly_files(self):
    """
    r"^(?P<yearmonth>slashd{4}slash-slashd{2})
      slashs{1}(?P<currs_num_den_w_uline>[A-Z]{3}_[A-Z]{3}) exchange ratesslash.txt$"
    """
    for year in self.years:
      fopath = self.get_folderpath_for_year(year)
      entries = os.listdir(fopath)
      filenames = filter(re_cmpld_exchangerate_datafilename.match, entries)
      for fn in filenames:
        year_dash_month = re_cmpld_exchangerate_datafilename.match().group('yearmonth')
        refmonthdate = rmd.make_refmonth_or_none(year_dash_month)
        self.refmonths.append(refmonthdate)
      return



  def find_year_folders(self):
    """

    """
    fopath = self.bcb_datafolderpath
    entries = os.listdir(fopath)
    print(entries)
    entries_abspath = map(lambda e: os.path.join(fopath, e), entries)
    print(entries_abspath)
    direntries_abspath = filter(lambda e: os.path.isdir(e), entries_abspath)
    direntries_abspath = filter(recmpl_repatt_year_ending_str.match, direntries_abspath)
    direntries_abspath = list(direntries_abspath)
    self.years = []
    print('entries_abspath', direntries_abspath)
    for fopath in direntries_abspath:
      year = recmpl_repatt_year_ending_str.match(fopath).group(1)
      scrmsg = f"year = {year}"
      print(scrmsg)
      self.years.append(year)
      print(scrmsg)
    print(self.years)

  def __str__(self):
    outstr = f"""{self.__class__.__name__}
    bcb_datafolderpath = {self.bcb_datafolderpath}
    year min = {self.year_min}
    year max = {self.year_max}
    """
    return outstr


def adhoctest1():
  """
  repatt_year_ending_str = r'(?<year>slashd{4})$'
  recmpl_repatt_year_ending_str = re.compile(repatt_year_ending_str)
  """
  s = 'bla bla 2020'
  match = recmpl_repatt_year_ending_str.match(s)
  year = None if match is None else match.group('year')
  scrmsg = f"from [{s}] -> extracting year at the ending => {year}"
  print(scrmsg)
  s = 'bla bla 2020 foo'
  match = recmpl_repatt_year_ending_str.match(s)
  year = None if match is None else match.group('year')
  scrmsg = f"from [{s}] -> extracting year at the ending => {year}"
  print(scrmsg)


def adhoctest2():
  finder = BCBMonthlyPrettiyPrintFinder()
  finder.find_year_folders()
  print(finder)


def process():
  """
  """
  adhoctest2()


if __name__ == "__main__":
  process()
