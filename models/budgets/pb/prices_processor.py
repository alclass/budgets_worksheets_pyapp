#!/usr/bin/env python3
"""
models/budgets/pb/prices_processor.py

import copy
import os
"""
import pandas
import commands.show.corr_monet_n_indices_calculator_from_dates as cmc  # cmc.CorrMonetWithinDatesCalculator


def show_qtd_of_prices_per_nm(prices):
  n_tot_prices = 0
  for i, nmcode in enumerate(prices.nn_n_priceitemlist_dict):
    n_prices = len(prices.nn_n_priceitemlist_dict[nmcode])
    n_tot_prices += n_prices
    seq = i + 1
    scrmsg = f"{seq} nm {nmcode} has {n_prices} prices"
    print(scrmsg)
  avg_prices_per_item = n_tot_prices / prices.size
  print('n_tot_prices', n_tot_prices, 'avg prices per items', avg_prices_per_item)


class Prices:

  def __init__(self):
    self.nn_n_priceitemlist_dict = {}

  def add_price_via_nm(self, nmcode, priceitem):
    if nmcode in self.nn_n_priceitemlist_dict:
      self.nn_n_priceitemlist_dict[nmcode].append(priceitem)
    else:
      self.nn_n_priceitemlist_dict[nmcode] = [priceitem]

  @property
  def size(self):
    return len(self.nn_n_priceitemlist_dict)

  def get_unique_nms(self):
    return sorted(self.nn_n_priceitemlist_dict.keys())

  def get_unique_nms_n_filenames(self):
    nms = sorted(self.nn_n_priceitemlist_dict.keys())
    output_tuplelist = []
    for nm in nms:
      pi = self.nn_n_priceitemlist_dict[nm]
      tupl = (nm, pi[0].fname)
      output_tuplelist.append(tupl)
    output_tuplelist = sorted(output_tuplelist, key=lambda e: e[1])
    return output_tuplelist

  def print_allprices_per_nm(self):
    nms = sorted(self.nn_n_priceitemlist_dict.keys())
    output_tuplelist = []
    for nm in nms:
      priceitems = self.nn_n_priceitemlist_dict[nm]
      for pi in priceitems:
        print(pi)

  def show_prices_as_pandas_df(self):
    nms = sorted(self.nn_n_priceitemlist_dict.keys())
    df = pandas.DataFrame()
    for nm in nms:
      priceitems = self.nn_n_priceitemlist_dict[nm]
      for pi in priceitems:
        pdict = pi.as_dict()
        df.add(pdict)
    return df.to_string()


class PriceItem:

  known_measure_units = ['unit', 'metro', 'kg']
  meas_unit_default = 'unit'

  def __init__(self):
    self.seq = None  # a sequencial number
    self.nmcode = None  # the material item code
    self.nm_alt = None  # an alternative material item code
    self.date = None  # price date
    self.netprice = None  # price without taxes, usually a saq-request price
    self._meas_unit = self.meas_unit_default  # unit price unit-type: unit, metro, kg
    self.openprice = None  # openprice is a full price informed in general in a webpage
    self.currency = 'BRL'  # money currency in its 3-letter code (example: 'BRL' Brazilian Reais)
    self.supplier = None  # the vendor or supplier
    self.url = None  # url of price if openprice
    self.fname = None  # xlsx data filename
    self.sapreq = None  # if price comes from a pedido-sap, this number comes in here
    self._mone_corr_mult_fact = None  # monetary correction multiplication factor

  @property
  def meas_unit(self):
    return self._meas_unit

  @property
  def mone_corr_mult_fact(self):
    if self._mone_corr_mult_fact is None:
      self.set_n_calc_mult_fact_for_mone_corr()
      if self._mone_corr_mult_fact is None:
        return 1.0
    return self._mone_corr_mult_fact

  @meas_unit.setter
  def meas_unit(self, meas_unit):
    self._meas_unit = meas_unit
    self.treat_measure_unit()

  def treat_measure_unit(self):
    """
    known_measure_units = ['unit', 'metro', 'kg']
    """
    known = self.known_measure_units
    if self.meas_unit not in known:
      errmsg = f"unit {self.meas_unit} outside of known_measure_units = {known}"
      raise ValueError(errmsg)

  def set_n_calc_mult_fact_for_mone_corr(self):
    """
    Calculates the multication factor for monetary correction
    Calls the "multiplication factor" get-function giving price's date
    """
    cmclc = cmc.CorrMonetWithinDatesCalculator()
    self._mone_corr_mult_fact = cmclc.calc_composite_corr_mone_from_date(self.date)

  def get_dict_keys(self):
    return self.as_dict().keys()

  def as_dict(self):
    pdict = {
      'seq': self.seq,
      'nmcode': self.nmcode,
      'nm_alt': self.nm_alt,
      'date': self.date,
      'netprice': self.netprice,
      'meas_unit': self.meas_unit,
      'openprice': self.openprice,
      'multfact': self.mone_corr_mult_fact,
      'currency': self.currency,
      'supplier': self.supplier,
      'url': self.url,
      'fname': self.fname,
      'sapreq': self.sapreq,
    }
    return pdict

  def __str__(self):
    outstr = f"""
  seq = {self.seq}
  nmcode = {self.nmcode}
  nm_alt = {self.nm_alt}
  date = {self.date}
  netprice = {self.netprice}
  meas_unit = {self.meas_unit}
  openprice = {self.openprice}
  multfact = {self.mone_corr_mult_fact}
  currency = {self.currency }
  supplier = {self.supplier }
  url = {self.url}
  fname = {self.fname}
  sapreq = {self.sapreq}
    """
    return outstr


def adhoctest():
  pass


def process():
  pass


if __name__ == '__main__':
  """
  """
  # adhoctest()
  process()
