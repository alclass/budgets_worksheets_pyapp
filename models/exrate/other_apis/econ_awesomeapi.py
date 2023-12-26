#!/usr/bin/env python3
"""
models/exrate/other_apis/econ_awesomeapi.py

https://docs.awesomeapi.com.br/api-de-moedas
https://docs.awesomeapi.com.br/api-cep

https://cep.awesomeapi.com.br/json/20260260
"""
API_URL_INTERPOL = "https://cep.awesomeapi.com.br/json/{cep}"


def get_cepdata_via_awesomeapi_url_w_cep(cep):
  return API_URL_INTERPOL.format(cep)
