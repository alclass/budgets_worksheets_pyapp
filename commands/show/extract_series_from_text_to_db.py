#!/usr/bin/env python3
"""
extract_series_from_text_to_db.py
"""
import settings as cfg


def gen_filenames():
  basenames = ['%d-%d CUUR0000SA0.dat', '%d-%d SUUR0000SA0.dat']
  tuplelist = [(2001, 2010), (2011, 2020), (2021, 2022)]
  filenames = []
  for basename in basenames:
    for tupl in tuplelist:
      ini, fim = tupl
      filename = basename % (ini, fim)
      filenames.append(filename)
  print(filenames)
  return filenames


def extract_data_from_files(filenames):
  tuplerecords = []
  for datfilename in filenames:
    datfilepath = cfg.get_datafile_abspath_in_app(datfilename)
    fd = open(datfilepath)
    for line in fd.readlines():
      pp = line.split('|')
      if len(pp) < 4:
        continue
      try:
        seriesid = pp[1].lstrip(' \t').rstrip(' \t\r\n')
        year = pp[2].lstrip(' \t').rstrip(' \t\r\n')
        year = int(year)
        month = pp[3].lstrip(' \tM').rstrip(' \t\r\n')
        month = int(month)
        baselineindex = pp[4].lstrip(' \t').rstrip(' \t\r\n')
        baselineindex = float(baselineindex)
      except ValueError:
        continue
      strdate = '%d-%02d-01' % (year, month)
      print(seriesid, strdate, '['+str(baselineindex)+']')
      recordtuple = (seriesid, strdate, baselineindex)
      tuplerecords.append(recordtuple)
  return tuplerecords


def insert_into_db(tuplerecords):
  conn = cfg.get_connection()
  cursor = conn.cursor()
  for tuplerecord in tuplerecords:
    # seriesid, strdate, baselineindex = tuplerecord
    sql = 'INSERT INTO cpi_indices (seriesid, refdate, baselineindex) values (?, ?, ?);'
    ins = cursor.execute(sql, tuplerecord)
    print('Inserting', ins, tuplerecord)
  print('DB-Committing')
  conn.commit()


def process():
  filenames = gen_filenames()
  tuplerecords = extract_data_from_files(filenames)
  insert_into_db(tuplerecords)


if __name__ == '__main__':
  process()
