#!/usr/bin/env python3
"""
commands/fetch/bcb/fetch_exchangerate_with_datefile.py

jetbrains://pycharm/navigate/reference?project=local_settings.py&path=fs%2Fdatefs%2Fread_write_datelist_files.py

"""
import fs.datefs.read_write_datelist_files as rw


def read_dates_from_files():
  reader = rw.DateFileReaderWriter()
  reader.posorder = 'dmy'
  reader.sep = '.'
  scrmpg = f"input_filepath = {reader.input_filepath}"
  print(scrmpg)
  scrmpg = f"input_filename = {reader.input_filename}"
  print(scrmpg)
  res = reader.fetch_dates_converting_from_strlist_w_sep_n_posorder()
  print(res)
  res = reader.fetch_dates_converting_from_strlist_w_sep_n_posorder(True)
  print(res)


def process():
  read_dates_from_files()


if __name__ == "__main__":
  process()
