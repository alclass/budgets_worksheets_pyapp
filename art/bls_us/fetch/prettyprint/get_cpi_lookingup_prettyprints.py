#!/usr/bin/env python3
"""
commands/fetch/bls_us/get_cpi_lookingup_prettyprints.py
  gets CPI acc_index (singular or plural) with seriesid and month from prettyprint files stored in datafolder

The indices can also be gotten from a sqlite-db and also from the BLS API open version 1.
The script is useful when either the API is not available or the sqlite-db file is not yet built.
  (The accompanying sqlite-db file can be built from the prettyprint files themselves
    with a specific script in this system.)
"""
import argparse
import datetime
import lib.datefs.refmonths_mod as rmfs
import art.bls_us.fetch.prettyprint.read_cpis_from_prettyprintdb as prettyfreader
import lib.db.sqlite.db_sqlite_manager as sqlim  # sqlim.SqliteHandler
import art.bls_us.classes.cpis_clsmod as cpimod
# from commands.fetch.bls_us.read_cpis_from_db import KNOWN_SERIESID  # CUUR0000SA0, SUUR0000SA0, others?
DEFAULT_SERIESID = cpimod.SERIESID_CUUR0000SA0
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
    self.curr_year = datetime.date.today().year
    self.current_refmonthdate = rmfs.make_refmonthdate_or_current()
    self.ppreader = prettyfreader.CPIPrettyPrintReader()
    self._refmonths_n_cpis_dict = None
    self.treat_attrs()

  def treat_attrs(self):
    if self.seriesid is None or self.seriesid not in cpimod.REGISTERED_SERIESIDS:
      self.seriesid = DEFAULT_SERIESID
    if self.year is None:
      self.year = self.curr_year - 1

  def read_n_set_refmonth_n_cpis_dict(self):
    reader_o = prettyfreader.CPIPrettyPrintReader(seriesid=self.seriesid)
    pdict = reader_o.get_cpis_dict(self.year)
    # the first key is seriesid, the second key is the wanted one, i.e., refmonthdate
    try:
      self._refmonths_n_cpis_dict = pdict[self.seriesid]
    except KeyError:
      # this may mean:
      # 1 - that the year's prettyprint file is not available
      # 2 - that maybe file is available but data is absent or malformed
      # consider dict is empty
      self._refmonths_n_cpis_dict = {}

  @property
  def refmonths_n_cpis_dict(self):
    """
    Dynamic attribute that keeps _refmonth_n_cpis_dict
    It's a lazy-dbfetch_months_n_refmonths_as_dict_bt_refmonths i.e., it's dbfetch_months_n_refmonths_as_dict_bt_refmonths upon first get
    """
    if self._refmonths_n_cpis_dict is None:
      self.read_n_set_refmonth_n_cpis_dict()
      if self._refmonths_n_cpis_dict is None:
        return {}
    return self._refmonths_n_cpis_dict

  def get_cpi_for_refmonth(self, p_refmonth):
    try:
      return self.refmonths_n_cpis_dict[p_refmonth]
    except (AttributeError, KeyError):
      pass
    return None

  def get_acc_cpi_for_refmonthdate(self, p_refmonthdate):
    refmonthdate = rmfs.make_refmonthdate_or_current(p_refmonthdate)
    try:
      datum = self.refmonths_n_cpis_dict[refmonthdate]
      return datum.acc_index
    except KeyError:
      pass
    return None

  def process(self):
    _ = self.refmonths_n_cpis_dict()

  def report_empty_dataset(self):
    outstr = "="*40 + '\n'
    outstr += f"Monthly CPI series {self.seriesid} for year {self.year}\n"
    outstr += "Data set is empty. Chances are:\n"
    outstr += f"\t1 - prettyprint file for year {self.year} is missing.\n"
    outstr += f"\t2 - prettyprint file, if exists, is empty.\n"
    outstr += "="*40 + '\n'
    return outstr

  def mount_report_w_year_monthly_cpis(self):
    if len(self.refmonths_n_cpis_dict) == 0:
      return self.report_empty_dataset()
    outstr = "="*40 + '\n'
    outstr += f"Monthly CPI series {self.seriesid} for year {self.year}\n"
    outstr += "="*40 + '\n'
    asc_refmonths_n_cpis_dict = sorted(self.refmonths_n_cpis_dict)
    compound_yearly_index = 1
    previous_month_idx = 0  # TODO this should be the increase from Dec to Jan
    first_acc_index = 0
    for i, refmonthdate in enumerate(asc_refmonths_n_cpis_dict):
      try:
        datum = self.refmonths_n_cpis_dict[refmonthdate]
        year = refmonthdate.year
        month = refmonthdate.month

        acc_index = datum.acc_index
        if i == 0:
          first_acc_index = acc_index
        increase_in_month = acc_index - previous_month_idx
        if increase_in_month != 0 and previous_month_idx != 0:
          increase_fraction = increase_in_month / previous_month_idx
        else:
          increase_fraction = 0
        compound_yearly_index *= (1 + increase_fraction)
        scrmsg = (f"{year}-{month:02} -> idx={acc_index} "
                  f"| incr={increase_fraction:5.3f}\n")
        outstr += scrmsg
        previous_month_idx = acc_index
      except (AttributeError, KeyError):
        pass
    recomposed = first_acc_index * compound_yearly_index
    line = "="*40 + '\n'
    outstr += line
    scrmsg = (f"11 months increase base1 idx -> {compound_yearly_index:5.3f} "
              f"| recomposed last idx={recomposed:7.3f} | first idx = {first_acc_index:7.3f}\n")
    outstr += scrmsg
    return outstr

  def __str__(self):
      outstr = "="*40 + "\n"
      outstr += f"{self.__class__.__name__}:\n"
      outstr += self.mount_report_w_year_monthly_cpis()
      return outstr


class CPIYears:

  def __init__(self, refmonthdate_fr, refmonthdate_to, seriesid):
    """
    self.refmonthdate_fr = rmfs.make_refmonthdate_for_year_n_month(self.year, 1)
    self.refmonthdate_to = rmfs.make_refmonthdate_for_year_n_month(self.year, 12)
    """
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

  def read_yearly_cpi_data(self):
    for i_year in range(self.year_fr, self.year_to+1):
      self.yearlycpi = FromPrettyPrintCPIYearlyGetter(seriesid=self.seriesid, year=i_year)
      _ = self.yearlycpi.refmonths_n_cpis_dict()

  def process(self):
    self.read_yearly_cpi_data()


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
  verifier.mount_report_w_year_monthly_cpis()


def get_args():
  seriesid = args.seriesid
  year = args.year
  return seriesid, year


def process():
  seriesid, year = get_args()
  yearcpis = FromPrettyPrintCPIYearlyGetter(seriesid=seriesid, year=year)
  print(yearcpis)


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
