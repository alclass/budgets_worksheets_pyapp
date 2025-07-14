#!/usr/bin/env python3
"""
models/finindices/ipea/ipea_rest_api_experimental_access_1.py

Descrição da REST API disponível:
  http://www.ipeadata.gov.br/api

http://www.ipeadata.gov.br/Default.aspx
  R (ipeadatar) => https://cran.r-project.org/package=ipeadatar
  Python (ipeadatapy) => https://pypi.org/project/ipeadatapy/
  Excel (versão 1.15.2) => http://ipeadata.gov.br/doc/api_IPEA_v1_15_2.xlsm

{
  "@odata.context":"http://ipeadata.gov.br/api/odata4/$metadata","value":[
    {
      "name":"Paises","kind":"EntitySet","url":"Paises"
    },{
      "name":"Metadados","kind":"EntitySet","url":"Metadados"
    },{
      "name":"Temas","kind":"EntitySet","url":"Temas"
    },{
      "name":"Territorios","kind":"EntitySet","url":"Territorios"
    },{
      "name":"Valores","kind":"EntitySet","url":"Valores"
    },{
      "name":"ValoresStr","kind":"EntitySet","url":"ValoresStr"
    }
  ]
}

Example:
http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='PRECOS12_IPCA12')

The last two records in IPCA seriesid 'PRECOS12_IPCA12':

  526
    SERCODIGO	"PRECOS12_IPCA12"
    VALDATA	"2023-10-01T00:00:00-03:00"
    VALVALOR	6716.74
    NIVNOME	""
    TERCODIGO	""
  527
    SERCODIGO	"PRECOS12_IPCA12"
    VALDATA	"2023-11-01T00:00:00-03:00"
    VALVALOR	6735.55
    NIVNOME	""
    TERCODIGO	""

"""


def adhoctest():
  pass


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest1()
  """
  process()
