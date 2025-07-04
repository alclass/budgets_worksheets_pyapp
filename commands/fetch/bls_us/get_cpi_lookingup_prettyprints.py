#!/usr/bin/env python3
"""
commands/fetch/cpi_us/get_cpi_lookingup_prettyprints.py
  gets CPI acc_index (singular or plural) with seriesid and month from prettyprint files stored in datafolder

The indices can also be gotten from a sqlite-db and also from the BLS API open version 1.
The script is useful when either the API is not available or the sqlite-db file is not yet built.
  (The accompanying sqlite-db file can be built from the prettyprint files themselves
    with a specific script in this system.)
"""
import argparse
import datetime
import fs.datefs.refmonths_mod as rmfs
import commands.fetch.bls_us.read_cpis_from_prettyprintdb as prettyfreader
from commands.fetch.bls_us.read_cpis_from_db import DEFAULT_SERIESID  # CUUR0000SA0
from commands.fetch.bls_us.read_cpis_from_db import KNOWN_SERIESID  # CUUR0000SA0, SUUR0000SA0, others?
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Download BLS CPI indices.")
parser.add_argument("--seriesid", type=str, default=DEFAULT_SERIESID,
                    help="Series Id")
parser.add_argument("--year", type=int, default=datetime.date.today().year,
                    help="CPI data'a year")
args = parser.parse_args()


class FromPrettyPrintCPIYearlyGetter:

  # prettyprint_filename_tointerpol = "{year} {seriesid} prettyprint.txt"
  # prettyprint_filename_tointerpol = prettyfreader.CPIPrettyPrintReader.prettyprint_file_tointerpol

  def __init__(self, seriesid=None, year=None):
    self.seriesid = seriesid
    self.year = year
    self.refmonthdate_fr = None
    self.refmonthdate_to = None
    self.curr_year = datetime.date.today().year
    self.current_refmonthdate = rmfs.make_refmonthdate_or_current()
    self.ppreader = prettyfreader.CPIPrettyPrintReader()
    self.refmonths_n_cpis_dict = {}
    self.treat_attrs()

  def treat_attrs(self):
    if self.seriesid is None or self.seriesid not in KNOWN_SERIESID:
      self.seriesid = DEFAULT_SERIESID
    if self.year is None:
      self.year = self.curr_year - 1
    self.refmonthdate_fr = rmfs.make_refmonthdate_for_year_n_month(self.year, 1)
    self.refmonthdate_to = rmfs.make_refmonthdate_for_year_n_month(self.year, 12)

  def get_cpis_dict(self):
    reader_o = prettyfreader.CPIPrettyPrintReader(seriesid=self.seriesid)
    pdict = reader_o.get_cpis_dict(self.year)
    # the first key is seriesid, the second key is the wanted one, i.e. refmonthdate
    dict2d = pdict[self.seriesid]
    for pdate in dict2d:
      print(pdate, dict2d[pdate])
      self.refmonths_n_cpis_dict.update({pdate: dict2d[pdate]})
    return dict2d

  def get_acc_cpi_for_refmonthdate(self, p_refmonthdate):
    refmonthdate = rmfs.make_refmonthdate_or_current(p_refmonthdate)
    try:
      datum = self.refmonths_n_cpis_dict[refmonthdate]
      return datum.acc_index
    except KeyError:
      pass
    return None

  def process(self):
    _ = self.get_cpis_dict()

  def show_the_years_monthly_cpis(self):
    print("="*40)
    scrmsg = f"Monthly CPI series {self.seriesid} for year {self.year}"
    print(scrmsg)
    print("="*40)
    asc_refmonths_n_cpis_dict = sorted(self.refmonths_n_cpis_dict)
    for refmonthdate in asc_refmonths_n_cpis_dict:
      try:
        datum = self.refmonths_n_cpis_dict[refmonthdate]
        year = refmonthdate.year
        month = refmonthdate.month
        scrmsg = f"{year}-{month:02} -> {datum.acc_index}"
        print(scrmsg)
      except (AttributeError, KeyError):
        pass

  def __str__(self):
      outstr = f"""Getter:
      """
      return outstr


class CPIYears:

  def __init__(self, refmonthdate_fr, refmonthdate_to, seriesid):
    self.refmonthdate_fr = refmonthdate_fr
    self.refmonthdate_to = refmonthdate_to
    self.seriesid = seriesid
    self.yearlycpi = None

  @property
  def year_fr(self):
    return self.refmonthdate_fr.year

  @property
  def year_to(self):
    return self.refmonthdate_to.year

  def get_thru_year_range(self):
    for i_year in range(self.year_fr, self.year_to+1):
      self.yearlycpi = FromPrettyPrintCPIYearlyGetter(seriesid=self.seriesid, year=i_year)
      _ = self.yearlycpi.get_cpis_dict()

  def process(self):
    self.get_thru_year_range()


def adhoctest():
  """
  refmonth_fr = datetime.date(year=2022, month=1, day=1)
  refmonth_to = datetime.date(year=2023, month=12, day=1)
  """
  verifier = FromPrettyPrintCPIYearlyGetter(year=2022)
  verifier.process()
  print('Stats', verifier)
  refmonthstr = '2022-05'
  ans = verifier.get_acc_cpi_for_refmonthdate(refmonthstr)
  scrmsg = f"verifier.get_cpi_for_refmonthdate({refmonthstr}) -> {ans}"
  print(scrmsg)
  refmonthstr = '2020-05'
  ans = verifier.get_acc_cpi_for_refmonthdate(refmonthstr)
  scrmsg = f"verifier.get_cpi_for_refmonthdate({refmonthstr}) -> {ans}"
  print(scrmsg)
  refmonthstr = '2022-08'
  ans = verifier.get_acc_cpi_for_refmonthdate(refmonthstr)
  scrmsg = f"verifier.get_cpi_for_refmonthdate({refmonthstr}) -> {ans}"
  print(scrmsg)
  refmonthstr = '2024-01'
  ans = verifier.get_acc_cpi_for_refmonthdate(refmonthstr)
  scrmsg = f"verifier.get_cpi_for_refmonthdate({refmonthstr}) -> {ans}"
  print(scrmsg)
  refmonthstr = '2023-12'
  ans = verifier.get_acc_cpi_for_refmonthdate(refmonthstr)
  scrmsg = f"verifier.get_cpi_for_refmonthdate({refmonthstr}) -> {ans}"
  print(scrmsg)
  verifier.show_the_years_monthly_cpis()


def get_args():
  seriesid = args.seriesid
  year = args.year
  return seriesid, year


def process():
  seriesid, year = get_args()
  getter = FromPrettyPrintCPIYearlyGetter(seriesid=seriesid, year=year)
  getter.show_the_years_monthly_cpis()


if __name__ == '__main__':
  process()
  adhoctest()
