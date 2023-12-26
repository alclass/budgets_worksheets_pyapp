"""
models/geoplaces/ceps_via_cepaberto.py
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
import fs.textfs.strfs as sfs
import settings as sett


class CepViaCepAberto:
  """
  1) Busca dos dados CEP via número-CEP
    Example (fetching '20260260'):
  {'altitude': 36.4, 'cep': '20260260', 'latitude': '-22.926038', 'longitude': '-43.2206416',
 'logradouro': 'Rua Augusto Paulino Filho', 'bairro': 'Tijuca',
 'cidade': {'ddd': 21, 'ibge': '3304557', 'nome': 'Rio de Janeiro'},
 'estado': {'sigla': 'RJ'}}

  2) Busca do CEP pela latitude e longitude mais próxima


  3) Busca do CEP por estado, cidade, bairro e logradouro
  {'latitude': '-23.4336578', 'longitude': '-45.0838481',
   'estado': {'sigla': 'SP'}, 'cep': '11680000',
   'cidade': {'nome': 'Ubatuba', 'ddd': 12, 'ibge': '3555406'},
   'altitude': 4.8}
  """
  API_URL_TO_INTERPOL_W_CEP = "https://www.cepaberto.com/api/v3/cep?cep={cep}"

  def __init__(self):
    self.n_statuscode_200 = 0
    self.n_failed_not_200 = 0
    self.cepaberto_api_token = None
    self.init_setget_api_token()

  def init_setget_api_token(self):
    try:
      self.cepaberto_api_token = sett.CEPABERTO_API_TOKEN
    except AttributeError:
      pass

  def is_api_token_set(self):
    return self.cepaberto_api_token is not None

  def return_error_if_api_token_not_set_or_none(self):
    if self.is_api_token_set():
      return None
    self.n_failed_not_200 += 1
    pdict = {
      'statuscode': -1,
      'error': 'CEPABERTO_API_TOKEN is not defined in local_settings.py, '
               'API cannot be accessed.\n  Please, find it and set it there.'
    }
    return json.dumps(pdict, indent=4)

  def return_error_if_cep_is_malformed_or_none(self, p_cep):
    cep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(p_cep)
    if cep is None:
      self.n_failed_not_200 += 1
      pdict = {
        'statuscode': -1,
        'error': f"""parameter p_cep given as None (null) or it's malformed
          (p_cep={p_cep}). API cannot be accessed.
          Please, reset parameter p_cep and try again."""
      }
      return json.dumps(pdict, indent=4)
    return None

  def get_cepdata_from_cepaberto_w_cep(self, p_cep):
    """
    The TOKEN below is not pushed to this system's gitrepo,
      it's kept in local_settings.py at the app root folder.
    If it's not there, find it out and place it in local_settings.py configfile
      with the same variable-name seen here.
    """
    json_o = self.return_error_if_api_token_not_set_or_none()
    if json_o is not None:
      return json_o
    json_o = self.return_error_if_cep_is_malformed_or_none(p_cep)
    if json_o is not None:
      return json_o
    cep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(p_cep)
    print('cep', cep, 'token', self.cepaberto_api_token)
    url = self.API_URL_TO_INTERPOL_W_CEP.format(cep=cep)
    headers = {'Authorization': f'Token token={sett.CEPABERTO_API_TOKEN}'}
    print('Accessing API', url)
    try:
      response = requests.get(url, headers=headers)
      json_o = response.json()
      self.n_statuscode_200 += 1
      return json_o
    except requests.exceptions.ConnectionError as exc_error:
      pdict = {
        'statuscode': -1,
        'error': f"""Connection error when accessing {url}.
          {exc_error}"""
      }
      self.n_failed_not_200 += 1
      return json.dumps(pdict, indent=4)

  def __str__(self):
    outstr = f"""CepViaCepAberto
    url base = {self.API_URL_TO_INTERPOL_W_CEP}
    n_statuscode_200 = {self.n_statuscode_200}
    n_failed_not_200 = {self.n_failed_not_200}
    """
    return outstr


def adhoctest():
  p_cep = '20260260'
  cepo = CepViaCepAberto()
  json_o = cepo.get_cepdata_from_cepaberto_w_cep(p_cep)
  print(json_o)
  print('cepo', cepo)


def process():
  pass


if __name__ == "__main__":
  process()
  adhoctest()
