#!/usr/bin/env python3
"""
commands/fetch/cpi_us/get_cpi_lookingup_prettyprints.py
"""
import datetime
# from dateutil.relativedelta import relativedelta
# import fs.datefs.years_date_functions as dtfs
import fs.datefs.refmonths_mod as rmfs
import commands.fetch.cpi_us.read_cpis_from_prettyprintdb as prettyfreader
MIN_REFMONTHS_ELAPSED_FOR_A_NEW_REMOTE_FETCH = 1


class FromPrettyPrintCPIGetter:

  prettyprint_filename_tointerpol = "{year} CUUR0000SA0 prettyprint.txt"

  def __init__(self, refmonthdate_fr, refmonthdate_to):
    self.refmonthdate_fr = refmonthdate_fr
    self.refmonthdate_to = refmonthdate_to
    self.current_refmonthdate = rmfs.make_refmonthdate_or_current()
    self.ppreader = prettyfreader.CPIPrettyPrintReader()

  @property
  def year_fr(self):
    return self.refmonthdate_fr.year

  @property
  def year_to(self):
    return self.refmonthdate_to.year

  @property
  def current_year(self):
    return self.current_refmonthdate.year

  def get_cpis_dict(self, year):
    reader_o = prettyfreader.CPIPrettyPrintReader()
    pdict = reader_o.get_cpis_dict(year)
    for k in pdict:
      print(k, pdict[k])

  def process(self):
    for i_year in range(self.year_fr, self.year_to+1):
      self.get_cpis_dict(i_year)
  # def get_prettyprint_for_year(self, year):

  def __str__(self):
      outstr = f"""Getter:
      """
      return outstr


def process():
  refmonth_fr = datetime.date(year=2022, month=1, day=1)
  refmonth_to = datetime.date(year=2023, month=12, day=1)
  verifier = FromPrettyPrintCPIGetter(refmonth_fr, refmonth_to)
  verifier.process()
  print('Stats', verifier)


if __name__ == '__main__':
  process()
