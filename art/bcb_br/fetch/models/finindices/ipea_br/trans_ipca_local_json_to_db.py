#!/usr/bin/env python3
"""
models/finindices/ipea/trans_ipca_local_json_to_db.py

Conceptually, for any series, two (maybe three) fields are necessary, ie:
 -> refmonth
 -> accumulated index

However, the seriesid itself ends up as a third field.

Another alternative is that a foreigh key might be established for the third field.
  In this case, an autoincrement integer id in a 'seriestable' would be
  the foreign key as the third field in the indices table.

The need this system has is the following:

  => indicator 'ind', for month 'mon', has index 'idx'

Examples:
  IGP-DI, for month 2023-01, has index 'idx1'
  IPCA-geral, for month 2023-01, has index 'idx2'
  CPI_US, for month 2023-01, has index 'idx3'
  PPI_US, for month 2023-01, has index 'idx4'
  and so on
-------------
-------------
The last two records in IPCA seriesid 'PRECOS12_IPCA12':
  526
    SERCODIGO	"PRECOS12_IPCA12"
    VALDATA	"2023-10-01T00:00:00-03:00"
    VALVALOR	6716.74
    NIVNOME	""
    TERCODIGO	""
  527
    SERCODIGO	"PRECOS12_IPCA12"
    VALDATA	"2023-11-01T00:00:00-03:00"
    VALVALOR	6735.55
    NIVNOME	""
    TERCODIGO	""

"""
import datetime
import art.bcb_br.fetch.models.finindices.ipea_br.folders_n_files_ipea_data as ipeaff  # .get_ipca12_filepath
IPEA_IPCA_URL = "http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='PRECOS12_IPCA12')"
today = datetime.date.today()
IPEA_MIDDLE_FOLDERNAME = 'findata/ipea'
IPCA_DATAFRAME_FILENAME = str(today) + '_ipca_dataframe_001.xlsx'


def read_file_into_dataframe():
  """
  df = pd.read_excel(ipca12_filepath)
  print(df.to_string())
  """
  ipca12_filepath, pdate = ipeaff.find_if_any_most_recent_ipca12_filepath_n_its_date()
  print(ipca12_filepath, pdate)


def trans_file_to_dataframe_adhoc():
  read_file_into_dataframe()


def adhoctest():
  trans_file_to_dataframe_adhoc()


def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
