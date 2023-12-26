"""
models/geoplaces/cepaberto_api_access.py
  has a function to access the REST API available from cepaberto.com

The API needs an authorization token which is kept outside gitrepo
  (in script local_settings.py which is read by settings.py, the latter in gitrepo)

Accessing the cepaberto API:
Example response (on 2023-12-25) from https://www.cepaberto.com/api/v3/cep?cep=20260260
{'altitude': 36.4, 'cep': '20260260', 'latitude': '-22.926038', 'longitude': '-43.2206416',
'logradouro': 'Rua Augusto Paulino Filho', 'bairro': 'Tijuca',
'cidade': {'ddd': 21, 'ibge': '3304557', 'nome': 'Rio de Janeiro'}, 'estado': {'sigla': 'RJ'}}

API functions:
1) Busca do CEP pelo número
2) Busca do CEP pela latitude e longitude mais próxima
3) Busca do CEP por estado, cidade, bairro e logradouro
4) Atualização de CEPs pelo número

Limites

Inicialmente, a API tem um limite de requisições por intervalo de tempo.
  Este limite existe para inibir possiveis bots que possam comprometer o tempo de resposta.
  Atualmente, o intervalo entre requisições, para cada usuário, é de 1 segundo.
  Requisições mais frequentes resultarão em HTTP Error 403 Forbidden.
  O limite máximo de requisições, para cada usuário, é de 10 mil por dia.

Exemplos de uso, em várias linguagens *, no repo git abaixo:
  https://github.com/edumucelli/cepaberto-api-examples
* Bash, Python, Ruby, C#, PHP, Delphi, Java, VBA, Golang e Node.js
"""
import json
import requests
import settings as sett


def get_cepdata_from_cepaberto_w_cep(p_cep):
  """
  The TOKEN below is not pushed to this system's gitrepo, it's kept in local_settings.py at the app root folder.
  If it's not there, find it out and place it in local_settings.py configfile with variable-name seen here.
  """
  try:
    cepaberto_api_token = sett.CEPABERTO_API_TOKEN
  except AttributeError:
    pdict = {
      'statuscode': -1,
      'error': 'CEPABERTO_API_TOKEN is not defined in local_settings.py, '
               'API cannot be accessed.\n  Please, find it and set it there.'
    }
    return json.dumps(pdict, indent=4)
  if cepaberto_api_token is None or p_cep is None:
    return None
  print('cep', p_cep, 'token', cepaberto_api_token)
  url = f"https://www.cepaberto.com/api/v3/cep?cep={p_cep}"
  # O seu token está visível apenas pra você
  headers = {'Authorization': f'Token token={sett.CEPABERTO_API_TOKEN}'}
  print('Accessing API', url)
  response = requests.get(url, headers=headers)
  json_o = response.json()
  return json_o


def adhoctest():
  p_cep = '20260260'
  json_o = get_cepdata_from_cepaberto_w_cep(p_cep)
  print(json_o)


def process():
  pass


if __name__ == "__main__":
  process()
  adhoctest()
