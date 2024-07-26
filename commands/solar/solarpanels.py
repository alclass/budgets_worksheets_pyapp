#!/usr/bin/env python3
"""
"""
# import os
datafilename = "2024-07 lista da prefeitura Entulhos & Resíduos CmprOD.dat"
datafolder_abspath = "/home/dados/OurDocs/Biz OD/Compras OD/Mats Cnst CmprOD/Entulhos & Resíduos CmprOD"


class SolarPanelSpecItem:

  def __init__(
      self, maker, len_wid_tupl, ncells, volt_amp_tupl,
      price_vendor_date_curr_qua,
  ):
    self.maker = maker
    self.len_wid_tupl = len_wid_tupl
    self.ncells = ncells
    self.volt_amp_tupl = volt_amp_tupl
    self.price_vendor_date_curr_qua = price_vendor_date_curr_qua

  @property
  def length(self):
    return self.len_wid_tupl[0]

  @property
  def width(self):
    return self.len_wid_tupl[1]

  @property
  def pow_out(self):
    return self.volt * self.amp

  @property
  def volt(self):
    return self.volt_amp_tupl[0]

  @property
  def amp(self):
    return self.volt_amp_tupl[1]

  @property
  def price(self):
    return self.price_vendor_date_curr_qua[0]

  @property
  def vendor(self):
    return self.price_vendor_date_curr_qua[1]

  @property
  def pricedate(self):
    return self.price_vendor_date_curr_qua[2]

  @property
  def price3lettercurrency(self):
    return self.price_vendor_date_curr_qua[3]

  def process(self):
    print('processing', self.vendor)

  def to_dict(self):
    outdict = {
      'maker': self.maker,
      'length': self.length,
      'width': self.width,
      'ncells': self.ncells,
      'volt': self.volt,
      'amp': self.amp,
      'pow_out': self.pow_out,
    }
    return outdict

  def datum_inbetween_vertbar(self):
    outstr = ('{maker} | {length} | {width} | {ncells} | {volt} | {amp} | {pow_out}'
              .format(**self.to_dict()))
    return outstr

  def __str__(self):
    outstr = '''
    maker = {maker}
    length = {length}
    width = {width}
    ncells = {ncells}
    voltage = {volt}
    amperage = {amp}
    power out = {pow_out}
    '''.format(**self.to_dict())
    return outstr


def adhoctest():
  sp = SolarPanelSpecItem(
    maker='Era',
    len_wid_tupl=(12, 24),
    ncells=144,
    volt_amp_tupl=(80, 20),
    price_vendor_date_curr_qua=(886, '60Hz Solar Guy', '2024-07-25', 'BRL')
  )
  print(sp)
  print(sp.datum_inbetween_vertbar())


def process():
  sp = SolarPanelSpecItem(
    maker='Era',
    len_wid_tupl=(12, 24),
    ncells=144,
    volt_amp_tupl=(80, 20),
    price_vendor_date_curr_qua=(886, '60Hz Solar Guy', '2024-07-25', 'BRL')
  )
  sp.process()


if __name__ == '__main__':
  """
  """
  adhoctest()
  # process()
