#!/usr/bin/env python3
"""
models/geoplaces/ceps_via_awesomeapi.py
  Has classes and functions for fetching cep data from the Awesomeapi listed below.

https://docs.awesomeapi.com.br/api-cep
"""
import requests
import lib.textfs.strfs as sfs
CEP_TEST = '20550045'


class CepViaAwesomeApi:
  """

  """
  API_URL_TO_INTERPOL_W_CEP = 'https://cep.awesomeapi.com.br/json/{cep}'

  def __init__(self):
    self.n_statuscode_200 = 0
    self.n_failed_not_200 = 0

  def get_cepdata_json_response_w_cep(self, p_cep):
    cep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(p_cep)
    if cep is None:
      scrmsg = f"cep {p_cep} is not valid, it cannot access the API."
      print(scrmsg)
      return None
    url = self.API_URL_TO_INTERPOL_W_CEP.format(cep=cep)
    res = requests.get(url)
    if res.status_code == 200:
      self.n_statuscode_200 += 1
      json_r = res.json()
      return json_r
    else:
      self.n_failed_not_200 += 1
      return None

  def __str__(self):
    outstr = f"""CepViaAwesomeApi
    url base = {self.API_URL_TO_INTERPOL_W_CEP}
    n_statuscode_200 = {self.n_statuscode_200}
    n_failed_not_200 = {self.n_failed_not_200}
    """
    return outstr


def adhoctest_api_w_a_cep(pcep=None):
  cep = pcep or CEP_TEST
  co = CepViaAwesomeApi()
  json_r = co.get_cepdata_json_response_w_cep(cep)
  print('json_r', json_r)


def adhoctest():
  """
  adhoctest_api_w_a_cep()
  """
  cep = 20260320
  retcep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(cep)
  print(cep, 'retcep', retcep)
  cep = "20.260-330"
  retcep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(cep)
  print(cep, 'retcep', retcep)


def process():
  pass


if __name__ == "__main__":
  process()
  adhoctest()
