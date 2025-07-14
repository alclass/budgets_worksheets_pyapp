#!/usr/bin/env python3
"""
models/finindices/ipea/fetch_remote_ipca_to_local_json.py

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

last two:
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
import os
import requests
import pandas as pd
import art.ipea_br.folders_n_files_ipea_data as ppdt  # .get_output_filepath
IPEA_IPCA_URL = "http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='PRECOS12_IPCA12')"


def rest_api_call(api_url):
  """For advanced users. Returns raw Ipeadata API data in the form of a data frame."""
  response = requests.get(api_url)
  if response.status_code == requests.codes.ok:
    json_response = response.json()
    if 'value' in json_response:
      try:
        data_frame = pd.DataFrame(json_response['value'])
        return data_frame
      except ValueError:
        scrmsg = f"""Could not instantiate Pandas's dataframe from httpresponse
        from api_url = "{api_url}" """
        print(scrmsg)
    else:
      scrmsg = f"""attribute value was not present in json from httpresponse
      from api_url = "{api_url}"
      {json_response}"""
      print(scrmsg)
  else:
    scrmsg = f"""returned status code was not 'ok' from httpresponse
    from api_url = "{api_url}"
    {response}"""
    print(scrmsg)
  return None


def fetch_adhoc():
  output_filepath = ppdt.get_todays_ipca12_filepath()
  if os.path.isfile(output_filepath):
    scrmsg = f"Halting. File [{output_filepath}] exists."
    print(scrmsg)
    return
  api_url = IPEA_IPCA_URL
  print('Fetch url', api_url)
  df = rest_api_call(api_url)
  print('Saving file', output_filepath)
  df.to_excel(output_filepath)


def adhoctest():
  fetch_adhoc()


def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
