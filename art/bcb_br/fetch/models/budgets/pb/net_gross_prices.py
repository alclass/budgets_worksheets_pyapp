#!/usr/bin/env python3
"""
models/budgets/pb/net_gross_prices.py

import copy
import os
"""
PIS_DEFAULT = 0.0165
COFINS_DEFAULT = 0.076
ICMS_DEFAULT = 0.22
IPI_DEFAULT = 0.0325
MAX_PRACTICAL_ICMS = 0.5


def calc_fator_basecalc_p_pis_cofins(cofins=None, pis=None):
  cofins = COFINS_DEFAULT if cofins is None else cofins
  pis = PIS_DEFAULT if pis is None else pis
  pis_cofins_basecalc = 1 / (1 - (pis + cofins))
  return pis_cofins_basecalc


def calc_fator_basecalc_p_ipi(cofins=None, icms=None, ipi=None, pis=None):
  cofins = COFINS_DEFAULT if cofins is None else cofins
  icms = ICMS_DEFAULT if icms is None else icms
  ipi = IPI_DEFAULT if ipi is None else ipi
  pis = PIS_DEFAULT if pis is None else pis
  pis_cofins_basecalc = calc_fator_basecalc_p_pis_cofins(cofins=cofins, pis=pis)
  ipi_basecalc = pis_cofins_basecalc / (1 - (icms * (1 + ipi)))
  return ipi_basecalc


def calc_fator_basecalc_p_icms(cofins=None, icms=None, ipi=None, pis=None):
  cofins = COFINS_DEFAULT if cofins is None else cofins
  pis = PIS_DEFAULT if pis is None else pis
  icms = ICMS_DEFAULT if icms is None else icms
  ipi = IPI_DEFAULT if ipi is None else ipi
  ipi_fator_base = calc_fator_basecalc_p_ipi(cofins=cofins, icms=icms, ipi=ipi, pis=pis)
  normvalue_ipi = ipi * ipi_fator_base
  icms_basecalc = ipi_fator_base + normvalue_ipi
  return icms_basecalc


def calc_factor_net_to_gross_price(cofins=None, icms=None, ipi=None, pis=None):
  """
  Obs: all factors are calculated "normalizedly", ie when initial price is 1
  """
  cofins = COFINS_DEFAULT if cofins is None else cofins
  pis = PIS_DEFAULT if pis is None else pis
  icms = ICMS_DEFAULT if icms is None else icms
  ipi = IPI_DEFAULT if ipi is None else ipi
  v_pis_cofins = (pis + cofins) * calc_fator_basecalc_p_pis_cofins(cofins=cofins, pis=pis)
  v_ipi = ipi * calc_fator_basecalc_p_ipi(cofins=cofins, icms=icms, ipi=ipi, pis=pis)
  v_icms = icms * calc_fator_basecalc_p_icms(cofins=cofins, icms=icms, ipi=ipi, pis=pis)
  factor_net_to_full_price = 1 + v_pis_cofins + v_ipi + v_icms
  return factor_net_to_full_price


def calc_factor_gross_to_net_price(cofins=None, icms=None, ipi=None, pis=None):
  inverse_factor = 1 / calc_factor_net_to_gross_price(cofins=cofins, icms=icms, ipi=ipi, pis=pis)
  return inverse_factor


def transform_grossprice_from_sourceicms_to_targeticms(grossprice, from_icms, to_icms):
  obj = NetNGrossPrice(icms_gross_to_net=from_icms)
  netprice = obj.calc_n_get_netprice_from_gross(gross_given=grossprice)
  price = obj.calc_n_get_grossprice_from_net(netprice)
  print('price', price)


class NetNGrossPrice:

  """
  This class allows calculations with consume taxes
  The functionality at larger was organized based on the 4-consumer-tax in Brazil
    (until 2025 and before the sistematic of Federal and State IVA)
  It does the following:
    1) given a product's net price (ie price without taxes),
       it can calculate its gross price (ie price with taxes)
    2) it can do the inverse of 1) above, ie:
       given a gross price (ie price with taxes),
       it can calculate a product's net price (ie price without taxes)
    3) it can retransform a gross price when its origin-ICMS is different from the target-ICMS:
       Example:
          suppose a gross price has a 16̈́% ICMS informed and
          one wants to transform it to a 18% ICMS price
      This class can do this retransform with method
       given a gross price (ie price with taxes),
       it can calculate a product's net price (ie price without taxes)

  """

  def __init__(self, cofins=None, icms=None, ipi=None, pis=None, icms_gross_to_net=None):
    self.cofins, self.icms, self.ipi, self.pis = cofins, icms, ipi, pis
    self._icms_gross_to_net = None
    self.icms_gross_to_net = icms_gross_to_net
    self.treat_input_params()
    self._pis_cofins_basecalc = None
    self._ipi_basecalc = None
    self._icms_basecalc = None
    self._factor_net_to_gross_price = None
    self._factor_gross_to_net_price = None

  @property
  def icms_gross_to_net(self):
    if self._icms_gross_to_net is None:
      return self.icms
    return self._icms_gross_to_net

  @icms_gross_to_net.setter
  def icms_gross_to_net(self, p_icms_gross_to_net):
    try:
      _icms_gross_to_net = float(p_icms_gross_to_net)
      if _icms_gross_to_net < 0:
        return
      if _icms_gross_to_net > MAX_PRACTICAL_ICMS:
        return
      self._icms_gross_to_net = _icms_gross_to_net
    except (TypeError, ValueError):
      pass

  @property
  def pis_cofins_basecalc(self):
    if self._pis_cofins_basecalc is None:
      self.calc_n_set_fator_basecalc_p_pis_cofins()
    return self._pis_cofins_basecalc

  @property
  def ipi_basecalc(self):
    if self._ipi_basecalc is None:
      self.calc_n_set_fator_basecalc_p_ipi()
    return self._ipi_basecalc

  @property
  def icms_basecalc(self):
    if self._icms_basecalc is None:
      self.calc_n_set_fator_basecalc_p_icms()
    return self._icms_basecalc

  @property
  def factor_net_to_gross_price(self):
    if self._factor_net_to_gross_price is None:
      self.calc_n_set_factor_net_to_gross_price()
    return self._factor_net_to_gross_price

  @property
  def factor_gross_to_net_price(self):
    if self._factor_gross_to_net_price is None:
      self.calc_n_set_factor_gross_to_net_price()
    return self._factor_gross_to_net_price

  def treat_input_params(self):
    self.cofins = COFINS_DEFAULT if self.cofins is None else self.cofins
    self.pis = PIS_DEFAULT if self.pis is None else self.pis
    self.icms = ICMS_DEFAULT if self.icms is None else self.icms
    self.ipi = IPI_DEFAULT if self.ipi is None else self.ipi

  def calc_n_set_fator_basecalc_p_pis_cofins(self):
    self._pis_cofins_basecalc = calc_fator_basecalc_p_pis_cofins(
      cofins=self.cofins,
      pis=self.pis
    )

  def calc_n_set_fator_basecalc_p_ipi(self):
    self._ipi_basecalc = calc_fator_basecalc_p_ipi(
      cofins=self.cofins,
      icms=self.icms,
      ipi=self.ipi,
      pis=self.pis
    )

  def calc_n_set_fator_basecalc_p_icms(self):
    self._icms_basecalc = calc_fator_basecalc_p_icms(
      cofins=self.cofins,
      icms=self.icms,
      ipi=self.ipi,
      pis=self.pis
    )

  def calc_n_set_factor_net_to_gross_price(self):
    self._factor_net_to_gross_price = calc_factor_net_to_gross_price(
      cofins=self.cofins,
      icms=self.icms,
      ipi=self.ipi,
      pis=self.pis
    )

  def calc_n_set_factor_gross_to_net_price(self):
    self._factor_gross_to_net_price = calc_factor_gross_to_net_price(
      cofins=self.cofins,
      icms=self.icms_gross_to_net,
      ipi=self.ipi,
      pis=self.pis
    )

  def calc_n_get_netprice_from_gross(self, gross_given):
    netprice = gross_given * self.factor_gross_to_net_price
    return netprice

  def calc_n_get_grossprice_from_net(self, net_given):
    grossprice = net_given * self.factor_net_to_gross_price
    return grossprice

  def __str__(self):
    outstr = f"""{self.__class__.__name__}
    cofins = {self.cofins:.4f}
    pis = {self.pis:.4f}
    icms = {self.icms:.4f}
    icms_gross_to_net = {self.icms_gross_to_net:.4f}
    ipi = {self.ipi:.4f}
    pis_cofins_basecalc = {self.pis_cofins_basecalc:.4f}
    ipi_basecalc = {self.ipi_basecalc:.4f}
    icms_basecalc = {self.icms_basecalc:.4f}
    factor_net_to_gross = {self.factor_net_to_gross_price:.4f}
    factor_gross_to_net = {self.factor_gross_to_net_price:.4f}"""
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


def adhoctest2():
  fromto_price = NetNGrossPrice()
  fromto_price.icms_gross_to_net = 0.16
  print(fromto_price)
  gross_given = 100
  netprice = fromto_price.calc_n_get_netprice_from_gross(gross_given)
  grossprice = fromto_price.calc_n_get_grossprice_from_net(netprice)
  scrmsg = f'gross_given = {gross_given} | netprice = {netprice} | grossprice = {grossprice}'
  print(scrmsg)
  transform_grossprice_from_sourceicms_to_targeticms(100, 0.16, 0.2)

def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest2()
