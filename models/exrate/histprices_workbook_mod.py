#!/usr/bin/env python3
"""
models/exrate/histprices_workbook_mod.py

The namedtuple for the BCB API response data is the following:
  namedtuple_bcb_api1 = coll.namedtuple(
    'BCBAPI1DataStr',
    'cotacao_compra cotacao_venda cotacao_datahora param_date error_msg gen_msg exchanger'
  )
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import datetime
import fs.economicfs.bcb.bcb_fetchfunctions as prefs
import fs.economicfs.bcb.bcb_financefunctions as finfs
"""
import csv
import os
import xlsxwriter
import fs.datefs.introspect_dates as intr
import fs.numberfs.tableaufunctions as tblfs
import models.exrate.histprices_mod as hispri
import settings as sett


class HistPriceWorkbook:

  def __init__(self, histprices, wb_filepath=None):
    self.wb_filepath = wb_filepath
    self.set_wb_filepath()
    self.histprices = histprices
    self.cellref = 'A3'
    self._totalprice = 0
    self.worksheet = None

  def set_wb_filepath(self):
    filename = 'histprices.xlsx'
    if self.wb_filepath is None:
      datafolder_abspath = sett.get_datafolder_abspath()
      self.wb_filepath = os.path.join(datafolder_abspath, filename)

  def generate_xlsx(self):
    workbook = xlsxwriter.Workbook(self.wb_filepath)
    self.worksheet = workbook.add_worksheet()
    self.cellref = 'C2'
    self.worksheet.write(self.cellref, 'Preços Históricos')
    self.cellref = 'A5'
    for histpriceitem in self.histprices:
      self.add_row_to_worksheet(histpriceitem)
      self.cellref = tblfs.move_cell_along_tableau(self.cellref, -7, 1)
    print('Closing ', self.wb_filepath)
    workbook.close()

  def add_row_to_worksheet(self, histpriceitem):
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.source_date)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.source_price)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.source_quote)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.target_quote)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.monet_corr_index)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.target_price)
    self.cellref = tblfs.move_cell_along_columns(self.cellref, 1)
    self.worksheet.write(self.cellref, histpriceitem.target_date)

  @property
  def totalprice(self):
    if self._totalprice is not None:
      return self._totalprice
    for hpi in self.histprices:
      self._totalprice += hpi.target_price
    return self._totalprice

  def __str__(self):
    return '<HistPriceWorkbook n_of_rows=%d totalprice=%.2f>' % (len(self.histprices), self.totalprice)


class TripleHistPrice:
  """
    data	        Preço líq.  Nº pedido (int saporder)
    30.07.2013	  2.466,44 	  4505421893
    11.07.2016	  4.454,58 	  4507292659
    (...)

  """

  def __init__(self, dmydotdate=None, commadecimalprice='1,00', saporder=None):
    self.dmydotdate = dmydotdate
    self.commadecimalprice = commadecimalprice
    self.saporder = saporder
    self._pdate = None
    self._dmybardate = None
    self._price = None
    self._histpriceitem = None

  @property
  def dmybardate(self):
    if self._dmybardate is not None:
      return self._dmybardate
    _ = self.pdate  # force first convertion to pdate
    if self.pdate is None:  # can't continue
      return None
    self._dmybardate = intr.trans_from_date_to_strdate_w_sep_posorder_n_zfill(
      self.pdate, sep='/', posorder='dmy', zfill=2
    )
    return self._dmybardate

  @property
  def pdate(self):
    if self._pdate is not None:
      return self._pdate
    if self.dmydotdate is None:  # needed for the convertion/calculation below
      return
    self._pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(
        strdate=self.dmydotdate, sep='.', orderpos='dmy'
    )
    return self._pdate

  @property
  def price(self):
    if self._price is not None:
      return self._price
    strprice = self.commadecimalprice.replace('.', '')
    strprice = strprice.replace(',', '.')
    self._price = float(strprice)
    return self._price

  @property
  def histpriceitem(self):
    if self._histpriceitem is not None:
      return self._histpriceitem
    self._histpriceitem = hispri.HistPrice(self.price, self.pdate)

  def as_dict(self):
    outdict = {
      'pricesdate': self.dmybardate,
      'price': self.price,
      'saporder': self.saporder,
    }
    return outdict

  def __str__(self):
    outstr = '''
  pricesdate  = %(pricesdate)s
  price = %(price).2f
  saporder = %(saporder)d
    ''' % self.as_dict()
    outstr += '-'*30
    _ = self.histpriceitem
    outstr += str(self.histpriceitem)
    return outstr


def get_example_adhoctest_data():
  tuplelist = []
  thp = TripleHistPrice('30.07.2013', '2.466,44', 4505421893)
  tuplelist.append(thp)
  thp = TripleHistPrice('11.07.2016', '4.454,58', 4507292659)
  tuplelist.append(thp)
  thp = TripleHistPrice('28.02.2020', '8.865,67', 4510003704)
  tuplelist.append(thp)
  thp = TripleHistPrice('31.03.2020', '5.601,70', 4510087906)
  tuplelist.append(thp)
  return tuplelist


def process_triplehistprices(triplehistprices):
  histprices = []
  for triplehistprice in triplehistprices:
    histprice = hispri.HistPrice(
      source_price=triplehistprice.price,
      source_date=triplehistprice.pdate,
      saporder=triplehistprice.saporder,
    )
    histprices.append(histprice)
    # print('-+'*30)
  workbook = HistPriceWorkbook(histprices)
  workbook.generate_xlsx()


def adhoc_test():
  source_price = '100'
  source_date = '2019-12-12'
  hptiem = hispri.HistPrice(source_price, source_date)
  print(hptiem)
  print('-'*30)


def read_csv_n_get_triplehistprices(pdelimiter='\t'):
  filename = 'triplehistprices.csv'
  datafolder_abspath = sett.get_datafolder_abspath()
  filepath = os.path.join(datafolder_abspath, filename)
  print('Reading input csv', datafolder_abspath, filepath)
  triplehistprices = []
  with open(filepath, newline='') as csvfp:
    reader = csv.reader(csvfp, delimiter=pdelimiter)  # delimiter = '"' tab = True, sep = comma
    for rowfieldvalues in reader:
      try:
        ddmmyyydotdate = rowfieldvalues[0]
        commaprice = rowfieldvalues[1]
        saporder = int(rowfieldvalues[2])
        triplehistprice = TripleHistPrice(ddmmyyydotdate, commaprice, saporder)
        triplehistprices.append(triplehistprice)
      except IndexError as e:
        if pdelimiter == ';':
          raise IndexError(e)
        return read_csv_n_get_triplehistprices(pdelimiter=';')
  return triplehistprices



def process():
  triplehistprices = read_csv_n_get_triplehistprices()
  print('Processing ', len(triplehistprices), 'rows')
  process_triplehistprices(triplehistprices)


if __name__ == "__main__":
  process()
