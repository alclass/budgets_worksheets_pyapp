#!/usr/bin/env python3
"""
models/budgets/pb/prices_processor.py

import copy
import os
import prettytable
"""
import datetime
import os
from dateutil import relativedelta
import pandas
import commands.bcb_br.report.corr_monet_n_indices_calculator_from_dates as cmc  # cmc.CorrMonetWithinDatesCalculator
import lib.datefs.introspect_dates as idt  # idt.for make_date_or_none()
import art.bcb_br.fetch.models.budgets.pb.nm_metadata_fetcher as nmi  # nmi.AllNMsInfo
import art.bcb_br.fetch.models.budgets.pb.net_gross_prices as ngp  # ngp.NetNGrossPrice
import art.bcb_br.fetch.models.budgets.pb.db_n_file_settings as dbs  # dbs.get_orcdados_batch_output_filepath_w_filename
ICMS_GROSS_TO_NET = 0.16


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
    priceitems_per_nm = self.nn_n_priceitemlist_dict[nmcode]
    avg_netprice = 0.0
    for pi in priceitems_per_nm:
      avg_netprice += pi.mone_corr_netprice
    avg_netprice = avg_netprice / len(priceitems_per_nm)
    return avg_netprice

  def print_allprices_per_nm(self):
    nms = sorted(self.nn_n_priceitemlist_dict.keys())
    # output_tuplelist = []
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
    column_names = PriceItem.get_stat_col_list_for_pi_pt()
    # nms = sorted(self.nn_n_priceitemlist_dict.keys())
    nms = self.nn_n_priceitemlist_dict.keys()
    c = 0
    for nm in nms:
      c += 1
      # if c > 5:
      #   break
      priceitems = self.nn_n_priceitemlist_dict[nm]
      price_meta = priceitems[0]
      print('='*40)
      nm = price_meta.nmcode
      seq = price_meta.seq
      pn = price_meta.partnumber
      outputfilename = f"{seq:02}.txt"  # "xlsx"
      outputfilepath = dbs.get_orcdados_batch_output_filepath_w_filename(outputfilename)
      if os.path.isfile(outputfilepath):
        print('File', outputfilename, 'already exists. Continuing.')
        continue
      outfd = open(outputfilepath, 'w', encoding='utf-8')
      print(outputfilename)
      n_prices = len(priceitems)
      family = price_meta.familycode
      ncm = price_meta.ncmcode
      ipi = f"{price_meta.ipi:.4f}".replace('.', ',')
      fabr = price_meta.manufacturer_sname
      ft_bru_a_liq = f"{price_meta.factor_grossprice_to_net:.4f}".replace('.', ',')
      fname = price_meta.fname
      # pt = prettytable.PrettyTable(column_names)
      hline1 = ';'
      for column_name in column_names:
        hline1 += f'"{column_name}";'
      print(hline1)
      outfd.write(hline1 + '\n')
      for pi in priceitems:
        line = ';'
        for val in pi.values_in_listorder_pi():
          # pt.add_row(pi.values_in_listorder_pi())
          if isinstance(val, float):
            val = f"{val:.2f}".replace('.', ',')
          line += f'"{val}";'
        outfd.write(line + '\n')
        print(line)
      # prettiedtable = str(pt)
      # prettiedtable = prettiedtable.replace('+', '|').replace('.', ',')
      qty = price_meta.qty
      tipounid = price_meta.meas_unit
      avgprice = self.calc_avg_netprice_of_nm(nm)
      totalprice = avgprice * qty
      fline1 = ';'*8 + 'nome de arquivo com as printscreens comprovantes:'
      print(fline1)
      outfd.write(fline1 + '\n')
      fline1 = ';'*8 + f'[{fname}]'
      print(fline1)
      outfd.write(fline1 + '\n')
      avgprc_str = f"{avgprice:.4f}".replace('.', ',')
      totalprice_str = f"{totalprice:.2f}".replace('.', ',')
      fline2 = (f';nº de preços (amostra):; {n_prices}; preço-médio:; {avgprc_str}'
                f'; qtd (expressa em {tipounid}):; {qty}; preço líquido total do item'
                f' (a transportar à aba [síntese preços]:; {totalprice_str}')
      print(fline2)
      outfd.write(fline2 + '\n')
      description = price_meta.description
      description = description.replace('"', "pol")
      hline1 = f';seq:;{seq:02};NM:;{nm};part-number:;"{pn}";descrição: {description}'
      print(hline1)
      outfd.write(hline1 + '\n')
      hline2 = (f';NCM:; {ncm}; IPI:;{ipi}; família: {family}; fabricante: {fabr}'
                f'; fator brut-a-líq:; {ft_bru_a_liq}')
      print(hline2)
      outfd.write(hline2 + '\n')
      hline3 = ';' * 8  # 9 altogether
      print(hline3)
      outfd.write(hline3 + '\n')
      print()
      outfd.close()
    # return df.to_string()


class PriceItem:

  known_measure_units = ['unit', 'metro', 'kg']
  meas_unit_default = 'UN'  # 'unit'
  column_names = [
    'seq',   'nmcode',   'nm_alt',   'date',   'netprice',   'meas_unit',   'openprice',
    'multfact',   'currency',   'supplier',   'url',   'fname',   'sapreq',
  ]
  column_names_for_pi_pt = [
    'data', 'preço líq.', 'correção monetária', 'preço líq. corrigido',
    'fornecedor',   'contrato/pedido SAP',  'url',
  ]

  column_names_for_pi_en = [
    'date', 'calc_netprice', 'mone_corr_mult_fact', 'mone_corr_netprice',
    'supplier',   'sapreq',  'url',
  ]

  def __init__(self):
    self._seq = None  # a sequencial number
    self.nmcode = None  # the material item code
    self.nm_alt = None  # an alternative material item code
    self._date = None  # price date
    self.netprice = None  # price without taxes, usually a saq-request price
    self._meas_unit = self.meas_unit_default  # unit price unit-type: unit, metro, kg
    self.opengrossprice = None  # openprice is a full price informed in general in a webpage
    self.currency = 'BRL'  # money currency in its 3-letter code (example: 'BRL' Brazilian Reais)
    self._factor_grossprice_to_net = None
    self._calc_netprice = None  # this is needed when the openprice exists, not the netprice itself
    self._mone_corr_mult_fact = None  # monetary correction multiplication factor
    self._mone_corr_netprice = None  # this is the work netprice, monetarily corrected if needed
    self._supplier = None  # the vendor or supplier
    self._url = None  # url of price if openprice
    self.fname = None  # xlsx data filename
    self._sapreq = None  # if price comes from a pedido-sap, this number comes in here
    self.nminfo = nmi.AllNMsInfo()

  @property
  def seq(self):
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return nm_o.seq
    except (AttributeError, TypeError):
      pass
    return -1

  @property
  def qty(self):
    """
    qty (quantity) is integer (for the first use we have as building it),
      this needs to be updated to float later one.
    """
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return int(nm_o.qty)
    except (AttributeError, TypeError):
      pass
    return -1

  @property
  def description(self):
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return nm_o.description
    except (AttributeError, TypeError):
      pass
    return 'no description'

  @property
  def familycode(self):
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return nm_o.familycode
    except (AttributeError, TypeError):
      pass
    return None

  @property
  def manufacturer_sname(self):
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return nm_o.manufacturer_sname
    except (AttributeError, TypeError):
      pass
    return None

  @property
  def partnumber(self):
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return nm_o.partnumber
    except (AttributeError, TypeError):
      pass
    return None

  @property
  def ipi(self):
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return nm_o.ipi
    except (AttributeError, TypeError):
      pass
    return None

  @property
  def ncmcode(self):
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return nm_o.ncmcode
    except (AttributeError, TypeError):
      pass
    return None

  @property
  def date(self):
    return self._date

  @date.setter
  def date(self, pdate):
    self._date = idt.make_date_or_none(pdate)

  @property
  def supplier(self):
    if self._supplier is not None:
      return self._supplier
    if self.sapreq is not None:
      return 'histórico SAP'
    return 'n/inf'

  @supplier.setter
  def supplier(self, supplier):
    self._supplier = supplier

  @property
  def url(self):
    if self._url is not None:
      return self._url
    return 'n/inf (histórico SAP)'

  @url.setter
  def url(self, url):
    self._url = url

  @property
  def sapreq(self):
    if self._sapreq is not None:
      return self._sapreq
    return 'n/inf'

  @sapreq.setter
  def sapreq(self, sapreq):
    self._sapreq = sapreq

  @property
  def mone_corr_netprice(self):
    if self._mone_corr_netprice is None:
      if self.calc_netprice is None or self.mone_corr_mult_fact is None:
        scrmsg = f"calc_netprice {self.calc_netprice} is None or mone_corr_mult_fact {self.mone_corr_mult_fact} is None"
        print(scrmsg)
      self._mone_corr_netprice = self.calc_netprice * self.mone_corr_mult_fact
    return self._mone_corr_netprice

  def calc_n_set_factor_grossprice_to_net(self):
    """
    An example with:
      cofins = 0.0760 | pis = 0.0165 | icms_gross_to_net = 0.1600 | ipi = 0.0325
      pis_cofins_basecalc = 1.1019 | ipi_basecalc = 1.4258 | icms_basecalc = 1.4721
      factor_gross_to_net = 0.7337 | factor_net_to_gross = 1.4721
    """
    ipi_default = 0.0325
    ipi = self.ipi or ipi_default
    netgross_o = ngp.NetNGrossPrice(ipi=ipi, icms_gross_to_net=ICMS_GROSS_TO_NET)
    self._factor_grossprice_to_net = netgross_o.factor_gross_to_net_price

  @property
  def factor_grossprice_to_net(self):
    if self._factor_grossprice_to_net is not None:
      return self._factor_grossprice_to_net
    self.calc_n_set_factor_grossprice_to_net()
    return self._factor_grossprice_to_net

  @factor_grossprice_to_net.setter
  def factor_grossprice_to_net(self, factor):
    """
    The multiplication factor from price to netprice is a formula
    """
    try:
      factor = float(factor)
      factor = 1.0 if factor < 1.0 else factor
      self._factor_grossprice_to_net = factor
    except (TypeError, ValueError):
      self._factor_grossprice_to_net = 1.0

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
      imtermediate_netprice = self.opengrossprice * self.factor_grossprice_to_net
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

  @property
  def meas_unit(self):
    """
    try:
      nm_o = self.nminfo.get_nminfo_by_nm(self.nmcode)
      return nm_o.meas_unit
    except (AttributeError, TypeError):
      pass
    """
    if self._meas_unit is None:
      return 'UN'
    return self._meas_unit

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
  def get_stat_col_list_for_pi_pt(cls):
    return cls.column_names_for_pi_pt

  @classmethod
  def get_stat_col_list_for_pi_en(cls):
    return cls.column_names_for_pi_en

  def get_dict_keys(self):
    return self.as_dict().keys()

  def values_in_listorder_pi(self):
    values_in_listorder = []
    for fieldname in self.column_names_for_pi_en:
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
  pass


def process():
  col_list = PriceItem.get_stat_col_list()
  print('col list', col_list)


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
