#!/usr/bin/env python3
"""
fs/os/os_complement.py

"""
import os
import settings as sett


def fetch_only_filepaths_from_folderpath(folderpath):
  if folderpath is None or not os.path.isdir(folderpath):
    return []
  entries = os.listdir(folderpath)
  if len(entries) == 0:
    return []
  fullentries = map(lambda e: os.path.join(folderpath, e), entries)
  filepaths = sorted(filter(lambda e: os.path.isfile(e), fullentries))
  return filepaths


def fetch_only_filenames_from_folderpath(folderpath):
  if folderpath is None or not os.path.isdir(folderpath):
    return []
  entries = os.listdir(folderpath)
  if len(entries) == 0:
    return []
  filepaths = fetch_only_filepaths_from_folderpath(folderpath)
  filenames = sorted(map(lambda e: os.path.split(e)[-1], filepaths))
  return filenames


def fetch_only_files_as_path_n_name_tuple_from_folderpath(folderpath):
  filepaths = fetch_only_filepaths_from_folderpath(folderpath)
  path_n_name_files = [os.path.split(fp) for fp in filepaths]
  return path_n_name_files


def adhoctest():
  """
  scrmsg = f"output_filepath = '{output_filepath}'"
  print(scrmsg)
  """
  folderpath = sett.get_datafolder_abspath()
  res = fetch_only_files_as_path_n_name_tuple_from_folderpath(folderpath)
  for item in res:
    print(item)


def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
