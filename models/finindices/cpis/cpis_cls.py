#!/usr/bin/env python3
"""
models/finindices/cpis/cpis_cls.py
  contains CPI-related functions and/or classes
"""
import datetime
SERIESID_LIST = ['CUUR0000SA0', 'SUUR0000SA0']
DEFAULT_SERIESID = 'CUUR0000SA0'


def transform_mmonth_to_refmonthdate(mmonth, year):
  try:
    month_n = int(mmonth.lstrip('M').strip())
    return datetime.date(year=year, month=month_n, day=1)
  except ValueError:
    pass
  return None



def find_seriesid_by_serieschar(serieschar):
  if serieschar == 'C':
    return 'CUUR0000SA0'
  elif serieschar == 'S':
    return 'SUUR0000SA0'
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
          refmonth = transform_mmonth_to_refmonthdate(self.refmonthdate, self.year)
          if refmonth is None:
            errmsg = f"refmonthdate (None) was not passed to class CPIDatum. Please, correct data and retry."
            raise ValueError(errmsg)
    # 3 refmonthdate
    if self.seriesid is None or self.seriesid not in SERIESID_LIST:
      errmsg = (f"series {self.seriesid} was not passed to class CPIDatum"
                f" belonging to list {SERIESID_LIST}. Please, correct data and retry.")
      raise ValueError(errmsg)
    # 4 acc_index
    try:
      self.acc_index = float(self.acc_index)
    except ValueError:
      errmsg = f"acc_index is not a float. Please, correct data and retry."
      raise ValueError(errmsg)

  def __str__(self):
    outstr = """CPIDatum:
    self.seriesid = 
    self.year = 
    self.refmonthdate = 
    self.acc_index = 
    self.footnotes = 
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
    acc_index = pdict['mmonth']
    datum = cls(
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
  def __init__(self, cpis=None):
    self.cpis = cpis or []

  def append(self, cpidatum):
    self.cpis.append(cpidatum)

  def __str__(self):
    outstr = 'CPIData\n'
    for i, cpi in enumerate(self.cpis):
      seq = i + 1
      outstr += '{seq:03} \t| {seriesid}  \t| {refmonthdate} \t| {baselineindex}\n'.format(
        seq=seq,
        seriesid=cpi.seriesid,
        refmonthdate=cpi.refmonthdate,
        baselineindex=cpi.baselineindex,
      )
    return outstr


def adhoctest():
  mmonth = 'M05'
  year = 2025
  res = transform_mmonth_to_refmonthdate(mmonth, year)
  print('res', res)
  mmonth = 'M12'
  year = 2025
  res = transform_mmonth_to_refmonthdate(mmonth, year)
  print('res', res)


def process():
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
