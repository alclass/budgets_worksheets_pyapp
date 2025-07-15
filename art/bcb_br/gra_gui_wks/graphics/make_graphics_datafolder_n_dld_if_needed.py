#!/usr/bin/env python3
"""
art/bcb_br/gra_gui_etc/make_graphics_datafolder_n_dld_if_needed.py

"""
import os.path
import pandas as pd
import settings as sett
import matplotlib.pyplot as plt
import requests
GRAPHICS_DATAFOLDERNAME = 'gra_gui_etc'


def get_graphics_datafolderpath():
  datafolder_abspath = sett.get_datafolder_abspath()
  graphfolderpath = os.path.join(datafolder_abspath, GRAPHICS_DATAFOLDERNAME)
  return graphfolderpath


def create_graphics_datafolder_if_needed(graphexfilepath):
  graphfolderpath = get_graphics_datafolderpath()
  if not os.path.isdir(graphfolderpath):
    os.makedirs(graphfolderpath)
  return


def download_exfile_to_folder_if_needed(graphexfilepath):
  if os.path.isfile(graphexfilepath):
    print('File in folder, no need to download.')
    print(graphexfilepath)
    return
  url = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv'
  req = requests.get(url)
  print('Downloading', url)
  fd = open('graphexfilepath', 'wb')
  fd.write(req.content)
  fd.close()
  print('Saved ', graphexfilepath)


def get_example1_filepath():
  """
  https://github.com/fivethirtyeight
  https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv

  """
  example1_filename = 'recent-grads.csv'
  graphfolderpath = get_graphics_datafolderpath()
  graphexfilepath = os.path.join(graphfolderpath, example1_filename)
  download_exfile_to_folder_if_needed(graphexfilepath)
  return graphexfilepath


def adhoctest():
  pass


def process():
  """
  """
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
