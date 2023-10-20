#!/usr/bin/env python3
"""
show_cpis.py
"""
DEFAULT_SERIESID = 'CUUR0000SA0'


def find_seriesid_by_serieschar(serieschar):
  if serieschar == 'C':
    return 'CUUR0000SA0'
  elif serieschar == 'S':
    return 'SUUR0000SA0'
  else:
    return DEFAULT_SERIESID


class CPIData:
  def __init__(self, cpis=[]):
    self.cpis = cpis

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


class CPIDatum:
  """

  """

  @classmethod
  def instantiate_from_dict(cls, pdict):
    pdict = dict(pdict)
    datum = cls()
    for ifieldname in pdict:
      fieldname = ifieldname
      # _ = fieldname  # just for the IDE (because of the exec() below)
      pyline = 'datum.{fieldname} = pdict["{fieldname}"]'.format(
        fieldname=fieldname,
      )
      exec(pyline)
    return datum

  def __init__(self, seriesid=None, refmonthdate=None, baselineindex=None):
    self.seriesid = seriesid
    self.refmonthdate = refmonthdate
    self.baselineindex = baselineindex

  def __str__(self):
    outstr = '{seriesid} | {refmonthdate} | {baselineindex}'.format(
      seriesid=self.seriesid,
      refmonthdate=self.refmonthdate,
      baselineindex=self.baselineindex,
    )
    return outstr


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
