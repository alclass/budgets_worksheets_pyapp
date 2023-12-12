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
import glob
import os
import xlsxwriter
import fs.datefs.introspect_dates as intr
import fs.numberfs.tableaufunctions as tblfs
import models.histprice.histprice_mod as hispri
import fs.numberfs.tableaufunctions as tbfs  # .Tableau
import settings as sett
HISTPRICE_FOLDERNAME = 'histprices'
OUTPUT_HISTPRICE_EXCEL_FILENAME = 'histprices.xlsx'


class HistPriceWorkbook:

  def __init__(self, histprice_obj, wb_filepath=None):
    self.wb_filepath = wb_filepath
    self.set_wb_filepath_as_default_if_none()
    self.histprice_obj = histprice_obj
    self.tableau = tbfs.Tableau()
    self.tableau.cellref = 'a3'
    self.tableau.insert_columns = ['date', 'price_i', 'cpi', 'exr', 'mul', 'price_f']
    self.tableau.fixref_fields = ['date_f', 'cpi_f', 'exr_f']
    self._totalprice = 0
    self.worksheet = None

  def set_wb_filepath_as_default_if_none(self):
    """
      if not os.path.isdir(histprice_folderpath):
        os.mkdir(histprice_folderpath)
    """
    if self.wb_filepath is None:
      datafolder_abspath = sett.get_datafolder_abspath()
      histprice_foldername = HISTPRICE_FOLDERNAME
      histprice_folderpath = os.path.join(datafolder_abspath, histprice_foldername)
      self.wb_filepath = os.path.join(histprice_folderpath, OUTPUT_HISTPRICE_EXCEL_FILENAME)

  def save_generate_xlsx(self):
    wb_folderpath, wb_filename = os.path.split(self.wb_filepath)
    if not os.path.isdir(wb_folderpath):
      print('Creating folder', wb_folderpath)
      os.mkdir(wb_folderpath)
      print('For saving file', wb_filename)
    workbook = xlsxwriter.Workbook(self.wb_filepath)
    self.worksheet = workbook.add_worksheet()
    self.tableau = 'C2'
    self.worksheet.write(self.tableau, 'Preços Históricos')
    self.tableau = 'A5'
    for histpriceitem in self.histprice_obj:
      self.add_row_to_worksheet(histpriceitem)
      self.tableau = tblfs.move_cell_along_tableau(self.tableau, -11, 1)
    print('Closing ', self.wb_filepath)
    workbook.close()

  def add_row_to_worksheet(self, histpriceitem):
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.date_ini)
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.price_ini)
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.cpi_ini)
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.cpi_fim)
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.exrate_ini)
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.exrate_fim)
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.monecorr_mul_fac)
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.price_fim)
    self.tableau = tblfs.move_cell_along_columns(self.tableau, 1)
    self.worksheet.write(self.tableau, histpriceitem.date_fim)

  @property
  def totalprice(self):
    if self._totalprice is not None:
      return self._totalprice
    for hpi in self.histprice_obj:
      self._totalprice += hpi.price_fim
    return self._totalprice

  def __str__(self):
    return '<HistPriceWorkbook n_of_rows=%d totalprice=%.2f>' % (len(self.histprice_obj), self.totalprice)


class TripleHistPrice:
  """
  This is a sort of "helper class" that instantiate an object
    with the following 3 atrributes:
      a) dmydotdate,
      b) commadecimalprice,
      c) sap_order

  a) the dmydotdate is a date in format {'sep': '.', posorder='dmy'},
  example: 30.07.2013; notice 30.7.2013 (with the leftzero in month) is also valid;

  b) the commadecimalprice is a float date in money format
  {'thousands_sep': '.', 'decimalplaces_sep': ',' }, example: 2.466,44

  c) sap_order is the order number and is just informative and identificational
  and does not take any effect in here;

An example "altogether":
    data	        Preço líq.  Nº pedido (int saporder)
    30.07.2013	  2.466,44 	  4505421893
    11.07.2016	  4.454,58 	  4507292659
    (...)
  """

  def __init__(self, dmydotdate=None, commadecimalprice='1,00', sap_order=None):
    self.dmydotdate = dmydotdate
    self.commadecimalprice = commadecimalprice
    self.sap_order = sap_order
    self._date = None  # converted from the dmydotdate
    self._dmybardate = None
    self._price = None  # converted from the commadecimalprice
    self._histpriceitem = None

  @property
  def dmybardate(self):
    if self._dmybardate is not None:
      return self._dmybardate
    _ = self.date  # force first convertion to pdate
    if self.date is None:  # can't continue
      return None
    self._dmybardate = intr.trans_from_date_to_strdate_w_sep_posorder_n_zfill(
      self.date, sep='/', posorder='dmy', zfill=2
    )
    return self._dmybardate

  @property
  def date(self):
    if self._date is not None:
      return self._date
    if self.dmydotdate is None:  # needed for the convertion/calculation below
      return
    self._date = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(
        strdate=self.dmydotdate, sep='.', orderpos='dmy'
    )
    return self._date

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
    self._histpriceitem = hispri.HistPrice(self.price, self.date)

  def as_dict(self):
    outdict = {
      'pricesdate': self.dmybardate,
      'price': self.price,
      'saporder': self.sap_order,
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
      price_ini=triplehistprice.price,
      date_ini=triplehistprice.date,
      sap_order=triplehistprice.sap_order,
    )
    histprices.append(histprice)
    # print('-+'*30)
  workbook = HistPriceWorkbook(histprices)
  workbook.save_generate_xlsx()


def adhoc_test():
  source_price = '100'
  source_date = '2019-12-12'
  hptiem = hispri.HistPrice(source_price, source_date)
  print(hptiem)
  print('-'*30)


def fetch_triplehistprice_files_n_folderpath_from_its_folder():
  """
  # weirdly the IDE (v2023.3) "stranged"the line below (via list-comprehensions)
  # which does the same as its a-like version via map
  # filenames = [os.path.split(fp)[-1] for fp in fps]
  """
  data_folderpath = sett.get_datafolder_abspath()
  triplehp_folderpath = os.path.join(data_folderpath, HISTPRICE_FOLDERNAME)
  entries = os.listdir(triplehp_folderpath)
  fps = glob.glob(triplehp_folderpath + '/triplehistprice*')
  filenames = sorted(filter(lambda e: e.startswith('triplehistprice'), entries))
  return filenames, triplehp_folderpath


def read_csv_n_get_triplehistprices(pdelimiter='\t'):
  filenames, fp = fetch_triplehistprice_files_n_folderpath_from_its_folder()
  if len(filenames) > 0:
    filename = filenames[0]
  else:
    return
  filepath = os.path.join(fp, filename)
  print('Reading input csv', filepath)
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
  if triplehistprices:
    print('Processing ', len(triplehistprices), 'rows')
    process_triplehistprices(triplehistprices)
  else:
    print('triplehistprices returned None')


if __name__ == "__main__":
  process()
