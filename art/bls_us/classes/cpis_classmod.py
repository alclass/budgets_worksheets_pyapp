#!/usr/bin/env python3
"""
art/bls_us/classes/cpis_clsmod.py
  Contains CPI-related functions, constants and/or classes

"""
import datetime
import lib.datefs.introspect_dates as intr
import lib.datefs.refmonths_mod as rmd
SERIESID_CUUR0000SA0 = 'CUUR0000SA0'
SERIESID_SUUR0000SA0 = 'SUUR0000SA0'
REGISTERED_SERIESIDS = [SERIESID_CUUR0000SA0, SERIESID_SUUR0000SA0]
DEFAULT_SERIESID = SERIESID_CUUR0000SA0


def find_seriesid_by_serieschar(serieschar):
  if serieschar == 'C':
    return SERIESID_CUUR0000SA0
  elif serieschar == 'S':
    return SERIESID_SUUR0000SA0
  else:
    return DEFAULT_SERIESID


class CPIDatum:

  def __init__(
      self,
      seriesid: str,
      year: str | int,
      refmonthdate: str | datetime.date,
      acc_index: str | float,
      footnootes=None
    ):
    self.seriesid = seriesid
    self.year = year
    self.refmonthdate = refmonthdate
    self.acc_index = acc_index
    self.footnotes = footnootes
    self.treat_attribs()

  def treat_attribs(self):
    # 1 year
    try:
      self.year = int(self.year)
    except ValueError:
      errmsg = f"year ({self.year}) was not passed as integer to class CPIDatum. Please, correct data and retry."
      raise ValueError(errmsg)
    # 2 refmonthdate
    if self.refmonthdate is None:
      errmsg = f"refmonthdate is None. Please, correct data and retry."
      raise ValueError(errmsg)
    if not isinstance(self.refmonthdate, datetime.datetime):
      p_refmonthdate = intr.make_refmonthdate_or_none(self.refmonthdate)
      if p_refmonthdate is None:
        # try a mmonth
        if self.refmonthdate.startswith('M'):
          refmonth = rmd.transform_mmonth_to_refmonthdate(self.refmonthdate, self.year)
          if refmonth is None:
            errmsg = f"refmonthdate (None) was not passed to class CPIDatum. Please, correct data and retry."
            raise ValueError(errmsg)
          self.refmonthdate = refmonth
    # 3 refmonthdate
    if self.seriesid is None or self.seriesid not in REGISTERED_SERIESIDS:
      errmsg = (f"series {self.seriesid} was not passed to class CPIDatum"
                f" belonging to list {REGISTERED_SERIESIDS}. Please, correct data and retry.")
      raise ValueError(errmsg)
    # 4 acc_index
    try:
      self.acc_index = float(self.acc_index)
    except ValueError:
      errmsg = f"acc_index is not a float. Please, correct data and retry."
      raise ValueError(errmsg)

  def __str__(self):
    outstr = f"""CPIDatum:
    seriesid = {self.seriesid} 
    year = {self.year} 
    refmonthdate = {self.refmonthdate} 
    acc_index =  {self.acc_index}
    footnotes = {self.footnotes} 
    """
    return outstr

  def show_as_line(self):
    outstr = '{seriesid} | {refmonthdate} | {acc_index}'.format(
      seriesid=self.seriesid,
      refmonthdate=self.refmonthdate,
      acc_index=self.acc_index,
    )
    return outstr

  @classmethod
  def instantiate_from_dict(cls, pdict):
    pdict = dict(pdict)
    seriesid = pdict['seriesid']
    year = pdict['year']
    mmonth = pdict['mmonth']
    refmonthdate = rmd.transform_mmonth_to_refmonthdate(mmonth, year)
    acc_index = pdict['acc_index']
    datum = cls(
      seriesid=seriesid,
      year=year,
      refmonthdate=refmonthdate,
      acc_index=acc_index
    )
    for ifieldname in pdict:
      fieldname = ifieldname
      # _ = fieldname  # just for the IDE (because of the exec() below)
      pyline = 'datum.{fieldname} = pdict["{fieldname}"]'.format(
        fieldname=fieldname,
      )
      exec(pyline)
    return datum


class CPIData:
  def __init__(self, cpis: list[CPIDatum] = None):
    self.cpis = cpis or []

  def append(self, cpidatum):
    self.cpis.append(cpidatum)

  def __str__(self):
    outstr = 'CPIData\n'
    for i, cpi in enumerate(self.cpis):
      seq = i + 1
      outstr += '{seq:03} \t| {seriesid}  \t| {refmonthdate} \t| {acc_index}\n'.format(
        seq=seq,
        seriesid=cpi.seriesid,
        refmonthdate=cpi.refmonthdate,
        acc_index=cpi.acc_index,
      )
    return outstr


def adhoctest():
  mmonth = 'M05'
  year = 2025
  res = rmd.transform_mmonth_to_refmonthdate(mmonth, year)
  print('res', res)
  mmonth = 'M12'
  year = 2025
  res = rmd.transform_mmonth_to_refmonthdate(mmonth, year)
  print('res', res)


def process():
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
