#!/usr/bin/env python3
"""


import copy
import os
"""
import pandas as pd
import models.budgets.pb.db_n_file_settings as dbs  # dbf.get_xlsx_ppubase_filepath
import models.budgets.pb.insert_ppubase_from_xlsx_to_db as ins  # ins.Insertor
PPUBASE_COLUMNNAMES = dbs.PPUBASE_COLUMNNAMES


def get_pandas_df_from_xlsx():
  inso = ins.Insertor()
  return inso.df


class AllNMsInfo:

  nminfo_nm_dict = {}
  nminfo_seqlist = []

  def __init__(self):
    self.df = get_pandas_df_from_xlsx()
    self.process()

  def get_nminfo_by_nm(self, nmcode):
    try:
      return self.nminfo_nm_dict[nmcode]
    except IndexError:
      pass
    return None

  def process(self):
    for row in self.df.iterrows():
      try:
        _, series = row
        nminfo = NMMetaNComplement()
        nminfo.seq = int(series['seq'])
        nminfo.nmcode = int(series['nmcode'])
        nminfo.ipi = series['ipi']
        nminfo.familycode = int(series['familycode'])
        nminfo.ncmcode = int(series['ncmcode'])
        nminfo.partnumber = series['partnumber']
        nminfo.manufacturer_sname = series['manufacturer_sname']
        nminfo.textobreve = series['textobreve']
        nminfo.description = series['description']
        nminfo.qty = float(series['qty'])
        nminfo.meas_unit = series['meas_unit']
      except ValueError:
        continue
      self.nminfo_seqlist.append(nminfo)
      self.nminfo_nm_dict[nminfo.nmcode] = nminfo
      # print(nminfo)

  def printout(self):
    for i, nminfo in enumerate(self.nminfo_seqlist):
      seq = i + 1
      print(seq, nminfo)
    print('total', len(self.nminfo_seqlist))


class NMMetaNComplement:
  """
  PPUBASE_COLUMNNAMES = [
    'seq', 'ncmcode', 'ipi', 'familycode', 'nmcode', 'partnumber',
    'manufacturer_sname', 'textobreve', 'description', 'qty', 'meas_unit'
  ]  # 11 fieldnames
  """

  def __init__(self):
    self.seq = None
    self.ncmcode = 0
    self.ipi = None
    self.familycode = None
    self.nmcode = 0
    self.partnumber = 0
    self.manufacturer_sname = 0
    self.textobreve = None
    self.description = None
    self.qty = 0
    self.meas_unit = 0

  def adhoctest(self):
    pass

  def __str__(self):
    outstr = f"""{self.__class__.__name__} {self.seq} | {self.nmcode}
      % ipi = {self.ipi}
      familycode = {self.familycode}
      partnumber = {self.partnumber}
      manufacturer = {self.manufacturer_sname}
      textobreve = {self.textobreve}
      description = {self.description}
      qty = {self.qty}
      meas_unit = {self.meas_unit}"""
    return outstr


def adhoctest():
  pass


def process():
  allo = AllNMsInfo()
  allo.printout()


if __name__ == '__main__':
  """
  """
  # adhoctest1()
  process()
