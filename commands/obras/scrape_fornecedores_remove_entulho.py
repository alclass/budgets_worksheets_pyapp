#!/usr/bin/env python3
"""
2024-07 lista da prefeitura RJ-RJ Entulhos & Resíduos CmprOD
https://comlurbnet.rio.rj.gov.br/extranet/credenciadas/listacredsEXTRANET.php#5
"""
import os
datafilename = "2024-07 lista da prefeitura Entulhos & Resíduos CmprOD.dat"
datafolder_abspath = "/home/dados/OurDocs/Biz OD/Compras OD/Mats Cnst CmprOD/Entulhos & Resíduos CmprOD"


def get_datafile_abspath():
  datafilepath = os.path.join(datafolder_abspath, datafilename)
  return datafilepath


class EntulhoProvider:

  def __init__(self, name, endr, bairro, telefone, email):
    self.name = name
    self.endr = endr
    self.bairro = bairro
    self.telefone = telefone
    self.email = email

  def to_dict(self):
    outdict = {
      'name': self.name,
      'endr': self.endr,
      'bairro': self.bairro,
      'telefone': self.telefone,
      'email': self.email,
    }
    return outdict

  def datum_inbetween_vertbar(self):
    outstr = '{name} | {endr} | {bairro} | {telefone} | {email}'.format(**self.to_dict())
    return outstr

  def __str__(self):
    outstr = '''
    {name}
    {endr}
    {bairro}
    {telefone}
    {email}
    '''.format(**self.to_dict())
    return outstr


class FileProcessor:

  def __init__(self):
    self.row_count = 0

  def read_file_n_return_contents(self):
    fp = get_datafile_abspath()
    text = open(fp, 'r').read()  # , encodings='utf-8'
    return text

  def process_contents(self):
    text = self.read_file_n_return_contents()
    lines = text.split('\n')
    self.row_count = 0
    for line in lines:
      if line.startswith('Email: '):
        self.row_count += 1
        print(self.row_count, line)

  def process(self):
    self.process_contents()


def adhoctest():
  ep = EntulhoProvider(
    name='Nico',
    endr='Rua Somewhere',
    bairro='Tijuca',
    telefone='9999-1111',
    email='email@email.com'
  )
  print(ep)
  print(ep.datum_inbetween_vertbar())

def process():
  p = FileProcessor()
  p.process()


if __name__ == '__main__':
  """
  """
  adhoctest()
  # process()
