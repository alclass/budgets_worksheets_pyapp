#!/usr/bin/env python3
"""
models/geoplaces/ceps.py

https://www.cepaberto.com/
https://buscacepinter.correios.com.br/app/faixa_cep_uf_localidade/index.php
https://terminaldeinformacao.com/2019/01/12/tabela-com-lista-de-ceps-do-brasil/

"""
import settings as sett
import requests
import models.geoplaces.cep_etc_settings as cset
CEP_TEST = '20550045'


class Cep:
  """

  """
  API_URL_TO_INTERPOL = 'https://cep.awesomeapi.com.br/json/{cep}'

  def __init__(self):
    pass

  def get_cep_data_via_api(self, cep):
    url = self.API_URL_TO_INTERPOL.format(cep)
    res = requests.get(url)
    if res.status_code == 200:
      json_r = res.json()
      print('json_r', json_r)


def adhoctest_api_w_a_cep(pcep=None):
  cep = pcep or CEP_TEST
  co = Cep()
  co.get_cep_data_via_api(cep)


def adhoctest():
  adhoctest_api_w_a_cep()


def process():
  pass


if __name__ == "__main__":
  process()
  adhoctest()
