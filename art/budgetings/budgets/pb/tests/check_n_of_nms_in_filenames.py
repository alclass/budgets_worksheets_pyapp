#!/usr/bin/env python3
"""
"""
import os


def get_unique_nms_from_filenames():
  total_xlsx = 0
  nms = []
  folderpath = "/home/dados/Pb/202402 FC37360 RF radiofreq itens consum Orç/Nolas/Lote 1 prices"
  filenames = sorted(os.listdir(folderpath))
  for fname in filenames:
    if not fname.endswith('.xlsx'):
      continue
    total_xlsx += 1
    # print(fname)
    name, _ = os.path.splitext(fname)
    pp = name.split(' ')
    nm = pp[-1]
    nms.append(nm)
  nms = list(set(nms))
  # print('total', total_xlsx, len(filenames), 'total nms', len(nms))
  return nms



def adhoctest():
  pass


def process():
  get_unique_nms_from_filenames()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
