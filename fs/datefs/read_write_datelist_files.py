#!/usr/bin/env python3
"""
fs/datefs/read_write_datelist_files.py
"""
import os
import fs.datefs.introspect_dates as intr
# import fs.datefs.datefunctions as dtfs
import settings as sett
DEFAULT_TXT_DATES_FILENAME = 'datesfile.txt'


def fetch_dates_from_textfile_w_filepath(filepath=None):
  if filepath is None or not os.path.isfile(filepath):
    return []
  text = open(filepath).read()
  lines = text.split('\n')
  strdatelist = []
  for line in lines:
    words = line.split(' ')
    words = list(map(lambda e: e.strip('\t\r\n'), words))
    # notice that words itself is an iterable/list, so the list-comprehension below
    # will help pick up the elment(s) to be appended to strdatelist
    _ = [strdatelist.append(word) for word in words]
  # notice that dates may be in some different formats (eg "2021-01-21" or "21/1/2021")
  # but they must all be converted to type datetime.date
  datelist = intr.introspect_n_convert_strdatelist_to_dates(strdatelist)
  datelist = sorted(filter(lambda e: e is not None, datelist))
  return sorted(datelist)


def form_datesfilepath_from_datafolder_w_filename(p_filename=None):
  filename = p_filename or DEFAULT_TXT_DATES_FILENAME
  folderpath = sett.get_datafolder_abspath()
  filepath = os.path.join(folderpath, filename)
  return filepath


def get_datesfilepath_from_datafolder_w_filename(p_filename=None):
  filepath = form_datesfilepath_from_datafolder_w_filename(p_filename)
  if not os.path.isfile(filepath):
    error_msg = 'File does not exist [%s].' % str(filepath)
    raise OSError(error_msg)
  return filepath


def get_default_datesfilepath():
  return get_datesfilepath_from_datafolder_w_filename()


def adhoc_test():
  fp = get_default_datesfilepath()
  print(fp)
  fp = get_datesfilepath_from_datafolder_w_filename()
  print(fp)
  dates = fetch_dates_from_textfile_w_filepath(fp)
  print(dates)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
