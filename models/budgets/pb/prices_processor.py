#!/usr/bin/env python3
"""
models/budgets/pb/prices_processor.py

import copy
import os
"""
import datetime
from dateutil import relativedelta
import pandas
import prettytable
import commands.show.corr_monet_n_indices_calculator_from_dates as cmc  # cmc.CorrMonetWithinDatesCalculator
import fs.datefs.introspect_dates as idt
PIS_DEFAULT = 0.0165
COFINS_DEFAULT = 0.076
ICMS_DEFAULT = 0.04
IPI_DEFAULT = 0.0325


def calc_fator_basecalc_p_pis_cofins(cofins=None, pis=None):
  pis = PIS_DEFAULT if pis is None else pis
  cofins = COFINS_DEFAULT if cofins is None else cofins
  pis_cofins_basecalc = 1 / (1 - (pis+cofins))
  return pis_cofins_basecalc


def calc_fator_basecalc_p_ipi(cofins=None, icms=None, ipi=None, pis=None):
  pis_cofins_basecalc = calc_fator_basecalc_p_pis_cofins(cofins=cofins, pis=pis)
  icms = ICMS_DEFAULT if icms is None else icms
  ipi = IPI_DEFAULT if ipi is None else ipi
  ipi_fator_base = pis_cofins_basecalc / (1 - (icms*(1+ipi)))
  return ipi_fator_base


def calc_fator_basecalc_p_icms(cofins=None, icms=None, ipi=None, pis=None):
  pis = PIS_DEFAULT if pis is None else pis
  cofins = COFINS_DEFAULT if cofins is None else cofins
  ipi = IPI_DEFAULT if ipi is None else ipi
  icms = ICMS_DEFAULT if icms is None else icms
  pis_cofins_basecalc = calc_fator_basecalc_p_pis_cofins(cofins=cofins, pis=pis)
  ipi_fator_base = calc_fator_basecalc_p_ipi(cofins=cofins, icms=icms, ipi=ipi, pis=pis)
  normvalue_ipi = ipi * ipi_fator_base
  fator_basecalc_p_icms = ipi_fator_base + normvalue_ipi
  return fator_basecalc_p_icms


def calc_factor_net_to_gross_price(cofins=None, icms=None, ipi=None, pis=None):
  """
  Obs: all factors are calculated "normalizedly", ie when initial price is 1
  """
  pis = PIS_DEFAULT if pis is None else pis
  cofins = COFINS_DEFAULT if cofins is None else cofins
  ipi = IPI_DEFAULT if ipi is None else ipi
  icms = ICMS_DEFAULT if icms is None else icms
  v_pis_cofins = (pis + cofins) * calc_fator_basecalc_p_pis_cofins(cofins=cofins, pis=pis)
  v_ipi = ipi * calc_fator_basecalc_p_ipi(cofins=cofins, icms=icms, ipi=ipi, pis=pis)
  v_icms = icms * calc_fator_basecalc_p_icms(cofins=cofins, icms=icms, ipi=ipi, pis=pis)
  factor_net_to_full_price = 1 + v_pis_cofins + v_ipi + v_icms
  return factor_net_to_full_price


def calc_factor_gross_to_net_price(cofins=None, icms=None, ipi=None, pis=None):
  inverse_factor = 1 / calc_factor_net_to_gross_price(cofins=cofins, icms=icms, ipi=ipi, pis=pis)
  return inverse_factor

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

  def calc_avg_netprice_of_nm(self, nmcode):
    pis = self.nn_n_priceitemlist_dict[nmcode]
    avg_netprice = 0.0
    for pi in pis:
      avg_netprice += pi.calc_netprice
    avg_netprice = avg_netprice / len(pis)
    return avg_netprice

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

  def show_prices_as_prettyprint(self):
    """
    the prettyprint has two parts
      p1 the "metadata" so to say, composed of:
        NM, NM description, NCM, avg_price, qty, total_price
      p1 the price_item itself, composed of:
        date, mone_corr netprice, supplier, url, fname, sapreq
    """
    column_names = PriceItem.get_stat_col_list_for_pi()
    nms = sorted(self.nn_n_priceitemlist_dict.keys())
    for nm in nms:
      priceitems = self.nn_n_priceitemlist_dict[nm]
      price_meta = priceitems[0]
      print('='*40)
      print('NM:', price_meta.nmcode, 'total of prices:', len(priceitems))
      pt = prettytable.PrettyTable(column_names)
      for pi in priceitems:
        pt.add_row(pi.values_in_listorder_pi())
      print(pt)
    # return df.to_string()


class PriceItem:

  known_measure_units = ['unit', 'metro', 'kg']
  meas_unit_default = 'unit'
  column_names = [
    'seq',   'nmcode',   'nm_alt',   'date',   'netprice',   'meas_unit',   'openprice',
    'multfact',   'currency',   'supplier',   'url',   'fname',   'sapreq',
  ]
  column_names_for_pi = [
    'date', 'calc_netprice', 'mone_corr_mult_fact', 'mone_corr_netprice',
    'supplier',   'sapreq',  'url',   'fname',
  ]

  def __init__(self):
    self.seq = None  # a sequencial number
    self.nmcode = None  # the material item code
    self.nm_alt = None  # an alternative material item code
    self._date = None  # price date
    self.netprice = None  # price without taxes, usually a saq-request price
    self._meas_unit = self.meas_unit_default  # unit price unit-type: unit, metro, kg
    self.opengrossprice = None  # openprice is a full price informed in general in a webpage
    self.currency = 'BRL'  # money currency in its 3-letter code (example: 'BRL' Brazilian Reais)
    self._factor_price_to_netprice = None
    self._calc_netprice = None  # this is needed when the openprice exists, not the netprice itself
    self._mone_corr_mult_fact = None  # monetary correction multiplication factor
    self._mone_corr_netprice = None  # this is the work netprice, monetarily corrected if needed
    self.supplier = None  # the vendor or supplier
    self.url = None  # url of price if openprice
    self.fname = None  # xlsx data filename
    self.sapreq = None  # if price comes from a pedido-sap, this number comes in here

  @property
  def date(self):
    return self._date

  @date.setter
  def date(self, pdate):
    self._date = idt.make_date_or_none(pdate)

  @property
  def meas_unit(self):
    return self._meas_unit

  @property
  def mone_corr_netprice(self):
    if self._mone_corr_netprice is None:
      if self.calc_netprice is None or self.mone_corr_mult_fact is None:
        scrmsg = f"calc_netprice {self.calc_netprice} is None or mone_corr_mult_fact {self.mone_corr_mult_fact} is None"
        print(scrmsg)
      self._mone_corr_netprice = self.calc_netprice * self.mone_corr_mult_fact
    return self._mone_corr_netprice

  @property
  def factor_price_to_netprice(self):
    if self._factor_price_to_netprice is not None:
      return self._factor_price_to_netprice
    self._factor_price_to_netprice = 0.7
    return self._factor_price_to_netprice

  @factor_price_to_netprice.setter
  def factor_price_to_netprice(self, factor):
    """
    The multiplication factor from price to netprice is a formula
    """
    try:
      factor = float(factor)
      factor = 1.0 if factor < 1.0 else factor
      self._factor_price_to_netprice = factor
    except (TypeError, ValueError):
      factor = 1.0

  @property
  def calc_netprice(self):
    if self._calc_netprice is not None:
      return self._calc_netprice
    if self.netprice is not None:
      if not self.is_pricedate_older_than_3_months():
        self._calc_netprice = self.netprice
        return self._calc_netprice
      self._calc_netprice = self.mone_corr_mult_fact * self.netprice
      return self._calc_netprice
    if self.opengrossprice is not None:
      imtermediate_netprice = self.opengrossprice * self.factor_price_to_netprice
      if not self.is_pricedate_older_than_3_months():
        self._calc_netprice = imtermediate_netprice
        return self._calc_netprice
      self._calc_netprice = self.mone_corr_mult_fact * imtermediate_netprice
      return self._calc_netprice
    # if at least either netprice or openprice is set, flow does not get here
    # otherwise (ie having both netprice and openprice as None), raise ValueError
    # it's a data problem
    errmsg = f"calc_netprice {self._calc_netprice} did not get a value."
    print(errmsg)
    raise ValueError(errmsg)
    # return None

  @property
  def n_months_elapsed_from_pricedate(self):
    today = datetime.date.today()
    rdelta = relativedelta.relativedelta(today, self.date)
    n_elapsed_months = rdelta.months + 12*rdelta.years
    return n_elapsed_months

  def is_pricedate_older_than_3_months(self):
    if self.n_months_elapsed_from_pricedate > 3:
      return True
    return False

  @property
  def mone_corr_mult_fact(self):
    if self._mone_corr_mult_fact is None:
      self.set_n_calc_mult_fact_for_mone_corr()
      if self._mone_corr_mult_fact is None:
        self._mone_corr_mult_fact = 1.0
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

  @classmethod
  def get_stat_col_list(cls):
    return cls.column_names

  @classmethod
  def get_stat_col_list_for_pi(cls):
    return cls.column_names_for_pi

  def get_dict_keys(self):
    return self.as_dict().keys()

  def values_in_listorder_pi(self):
    values_in_listorder = []
    for fieldname in self.column_names_for_pi:
      value = eval('self.' + fieldname)
      values_in_listorder.append(value)
    return values_in_listorder

  def values_in_listorder(self):
    values_in_listorder = [
      self.seq,
      self.nmcode,
      self.nm_alt,
      self.date,
      self.netprice,
      self.meas_unit,
      self.opengrossprice,
      self.mone_corr_mult_fact,
      self.currency,
      self.supplier,
      self.url,
      self.fname,
      self.sapreq,
    ]
    return values_in_listorder

  def as_dict(self):
    pdict = {
      'seq': self.seq,
      'nmcode': self.nmcode,
      'nm_alt': self.nm_alt,
      'date': self.date,
      'netprice': self.netprice,
      'calc_netprice': self.calc_netprice,
      'mone_corr_netprice': self.mone_corr_netprice,
      'meas_unit': self.meas_unit,
      'openprice': self.opengrossprice,
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
  calc_netprice = {self.calc_netprice}
  mone_corr_netprice = {self.mone_corr_netprice}
  meas_unit = {self.meas_unit}
  openprice = {self.opengrossprice}
  multfact = {self.mone_corr_mult_fact}
  currency = {self.currency }
  supplier = {self.supplier }
  url = {self.url}
  fname = {self.fname}
  sapreq = {self.sapreq}
    """
    return outstr


def adhoctest():
  """
  test go-n-come for price & netprice
  """
  f_pis_cofins = calc_fator_basecalc_p_pis_cofins()
  f_ipi = calc_fator_basecalc_p_ipi()
  f_icms = calc_fator_basecalc_p_icms()
  scrmsg = f"f_pis_cofin={f_pis_cofins:.4f} | f_ipi={f_ipi:.4f} | f_icms={f_icms:.4f}"
  print(scrmsg)
  f_net_to_gross = calc_factor_net_to_gross_price()
  f_gross_to_net = calc_factor_gross_to_net_price()
  scrmsg = f"f_net_to_gross={f_net_to_gross:.4f} | f_gross_to_net={f_gross_to_net:.4f}"
  print(scrmsg)
  netprice = 100
  grossprice = f_net_to_gross * netprice
  scrmsg = f"netprice={netprice:.4f} | grossprice={grossprice:.4f}"
  print(scrmsg)
  calc_netprice = grossprice * f_gross_to_net
  scrmsg = f"backing up grossprice={grossprice:.4f} | calc_netprice={calc_netprice:.4f}"
  print(scrmsg)


def process():
  col_list = PriceItem.get_stat_col_list()
  print('col list', col_list)


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
