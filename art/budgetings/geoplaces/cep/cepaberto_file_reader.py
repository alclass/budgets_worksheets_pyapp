#!/usr/bin/env python3
"""

import settings as sett
"""
import glob
import os
import pandas as pd
import requests
import art.budgetings.geoplaces.geoplaces_settings as cset
# import models.geoplaces.cep_etc_settings as   # cset.get_cepaberto_basefolderpath
cep_27_bra_est = "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO"
CEP_TEST = '20550045'


class CepDirTree:
  """
  The cepaberto CSV-Column mapping:
    {'A': cep, 'B': logradouro, 'C': logra_detalhe, 'D': bairro, 'E': citycode, 'E': ufcode}
  Example:
    {'cep': '20260260', 'logradouro': 'Rua Augusto Paulino Filho',
    'bairro': Tijuca, citycode: '7764', ufcode: '19'}

  The cep.awesomeapi.com.br, an alternative API, returns, for the same example as above:
    {"cep":"20260260","address_type":"Rua","address_name":"Augusto Paulino Filho",
    "address":"Rua Augusto Paulino Filho",
    "state":"RJ","district":"Tijuca","lat":"-22.926","lng":"-43.2206",
    "city":"Rio de Janeiro",
    "city_ibge":"3304557","ddd":"21"}

  Obs:
    1) Rio de Janeiro has IBGE id = 3304557
    2) The cepaberto equivalent id = 7764

  Sketches for sql-schema:
  CREATE TABLE geocep (
    id INT PRIMARY KEY,
    cep CHAR(8) NOT NULL,
    address_type CHAR(10),
    address_name TEXT NOT NULL,
    district TEXT,
    correiocitycode INT,
    ibgecitycode INT,
    ufcode CHAR(2),
    lat FLOAT,
    lng FLOAT,
    ddd CHAR(2),
    UNIQUE(cep)
   )
  """
  API_URL_TO_INTERPOL = 'https://cep.awesomeapi.com.br/json/{cep}'
  CEP_TABLENAME = 'geocep'

  def __init__(self):
    self.n_inserted = 0
    self.df = None  # pandas's dataframe, transient at every new csv file dbfetch_months_n_refmonths_as_dict_bt_refmonths
    self.siglas = cep_27_bra_est.split(' ')
    self.cepaberto_basefolderpath = cset.get_cepaberto_basefolderpath()
    self.tablename = self.CEP_TABLENAME

  def get_cep_data_via_api(self, cep):
    url = self.API_URL_TO_INTERPOL.format(cep)
    res = requests.get(url)
    if res.status_code == 200:
      json_r = res.json()
      print('json_r', json_r)

  def get_estado_folderpath(self, estado_sigla):
    siglalower = estado_sigla.lower()
    estado_folderpath = self.cepaberto_basefolderpath + '/' + siglalower
    return estado_folderpath

  def get_csvfilepaths_from_estado_folderpath(self, estado_sigla):
    estado_folderpath = self.get_estado_folderpath(estado_sigla)
    path_w_dash_asterisk_ext = estado_folderpath + '/*.csv'
    print('get_bra_sta_csvfiles for',  path_w_dash_asterisk_ext)
    csvfilepaths = sorted(glob.glob(path_w_dash_asterisk_ext))
    return csvfilepaths

  def trans_from_dataframe_to_db(self):
    """
    Record subset to transpose to DB:
      cep CHAR(8) NOT NULL,
      address_type CHAR(10),
      address_name TEXT NOT NULL,
      district TEXT,
      correiocitycode INT,
      ufcode CHAR(2)

    Obs: the other/complement fields will be scheduled, later on,
         to be fetched from the awesomeapi mentioned above
    """
    sql_insert = f"""
    INSERT OR IGNORE INTO {self.tablename}
      (cep, address_name, district, correiocitycode, ufcode)
      VALUES (?, ?, ?, ?, ?);
    """
    conn = self.get_connection()
    cursor = conn.cursor()
    for ro in self.df.index:
      tuplevalues = (ro.cep, ro.address_name, ro.district, ro.correiocitycode, ro.ufcode)
      retval = cursor.execute(sql, tuplevalues)
      if retval:
        self.n_inserted += 1
    if self.n_inserted > 0:
      conn.commit()
    conn.close()

  def open_csv_n_show_ceps_w_filepath(self, csvfilepath):
    df = pd.read_csv(csvfilepath)
    print(csvfilepath)
    print(df.to_string())

  def open_csv_n_show_ceps_w_estadosigla(self, estadosigla, seq=1):
    csvfilepaths = self.get_csvfilepaths_from_estado_folderpath(estadosigla)
    if -1< seq < len(csvfilepaths):
      csvfilepath = csvfilepaths[seq-1]
      return self.open_csv_n_show_ceps_w_filepath(csvfilepath)
    return None

  def get_bra_sta_csvfiles(self, estado_sigla):
    siglalower = estado_sigla.lower()
    csvfilepaths = self.get_csvfilepaths_from_estado_folderpath(estado_sigla)
    filenames = [os.path.split(ef)[-1] for ef in csvfilepaths]
    return filenames

  def show_filenames(self):
    for estadosigla in self.siglas:
      filenames = self.get_bra_sta_csvfiles(esestadosigla)
      print(estadosigla, '=>', filenames)
    print(cep_27_bra_est)
    print('total', len(self.siglas))

  def show_ceps_thru_states(self):
    for estadosigla in self.siglas:
      self.open_csv_n_show_ceps_w_estadosigla(estadosigla)
    print('show_ceps_thru_states total', len(self.siglas))

  def process(self):
    self.show_ceps_thru_states()


def adhoctest():
  pass


def process():
  cdt = CepDirTree()
  cdt.process()


if __name__ == "__main__":
  process()
  adhoctest()
