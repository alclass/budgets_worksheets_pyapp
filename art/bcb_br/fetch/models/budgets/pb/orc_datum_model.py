#!/usr/bin/env python3
"""
models/budgets/pb/orc_datum_model.py

nt1 = nt_constr(
  n_jira='a', descr=None, n_orp=None, n_oport=None, date_ini=None,
  date_entr=None, date_exp_aprv=None, date_aprv=None, date_res_nect=None,
)

"""
import datetime
import collections
url_jira_interpol = "https://jira.petrobras.com.br:8443/browse/FCTIC-{n_jira}"
url_oport_res_nect_interpol = "https://petronect.com.br/{n_oport}"
_orc_fieldnames = [
  'n_jira', 'descr', 'n_orp', 'n_oport', 'date_ini',
  'date_entr', 'date_exp_aprv', 'date_aprv', 'date_res_nect',
  'jira_pree', 'jira_w_res_nect', 'orctype', 'complexity',
]
orc_fieldtype_dict = {
  'n_jira': int , 'descr': str, 'n_orp': int,
  'n_oport': int, 'date_ini': datetime.date,
  'date_entr': datetime.date, 'date_exp_aprv': datetime.date,
  'date_aprv': datetime.date, 'date_res_nect': datetime.date,
  'jira_pree': bool, 'jira_w_res_nect': bool,
  'orctype': int, 'complexity': int,
}
orc_fieldnames = list(orc_fieldtype_dict.keys())
orc_nt_constr = collections.namedtuple(
  'NTOrcDatum', field_names=orc_fieldnames,
)


class OrcDatum(orc_nt_constr):
  """
    if not isinstance(orc_nt, nt_constr):
      pass
  """

  def __new__(
      cls,
      n_jira, descr=None, n_orp=None, n_oport=None,
      date_ini=None, date_entr=None, date_exp_aprv=None,
      date_aprv=None, date_res_nect=None,
      jira_pree=False, jira_w_res_nect=False,
      orctype='bens', complexity=None,

  ):
    return super().__new__(
      cls,
      n_jira, descr, n_orp, n_oport,
      date_ini, date_entr, date_exp_aprv,
      date_aprv, date_res_nect,
      jira_pree, jira_w_res_nect,
      orctype, complexity,
    )

  @property
  def url_jira(self):
    return url_jira_interpol.format(n_jira=self.n_jira)

  @property
  def url_oport_res_nect(self):
    return url_oport_res_nect_interpol.format(n_oport=self.n_oport)

  def __str__(self):
    outstr = f"""Orçamento Datum:
  n_jira={self.n_jira},, n_orp={self.n_orp}, n_oport={self.n_oport}, 
  descr={self.descr}
  date_ini={self.date_ini}, date_entr={self.date_entr}, 
  date_exp_aprv={self.date_exp_aprv}, date_aprv={self.date_aprv}, 
  date_res_nect={self.date_res_nect},
  jira_pree={self.jira_pree}, jira_w_res_nect={self.jira_w_res_nect},
  orctype={self.orctype}, complexity={self.complexity},
  
  URLs:
    url_jira={self.url_jira}
    url_oport={self.url_oport_res_nect}
    """
    return outstr


od1 = OrcDatum(n_jira=38301, n_oport=704893)
print(od1)


def adhoctest():
  pass


def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
