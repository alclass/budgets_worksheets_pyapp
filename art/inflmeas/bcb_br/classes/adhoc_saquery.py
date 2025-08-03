#!/usr/bin/env python3
"""
BudgetsWorksheets:
  art/inflmeas/bcb_br/classes/adhoc_saquery.py
"""
import lib.db.sqlalch.sqlalchemy_connection_clsmod as consa
import art.inflmeas.bcb_br.classes.daycurrexchrate_sqlal as sqal  # .SADayCurrExchRate
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv


def fetch_exrts_wi_daterange_via_sqlalchemy(date_fr, date_to):
  saconnector = consa.SqlAlchemyConnector()
  s = saconnector.get_sa_session()
  m = sqal.SADayCurrExchRate
  exrates = s.query(m). \
      filter(m.refdate.between(date_fr, date_to)). \
      order_by(m.refdate.asc())
  return exrates


def fetch_exrts_inside_datelist_via_sqlalchemy(datelist):
  saconnector = consa.SqlAlchemyConnector()
  s = saconnector.get_sa_session()
  m = sqal.SADayCurrExchRate
  exrates = s.query(m). \
      filter(m.refdate.in_(datelist)). \
      order_by(m.refdate.asc())
  return exrates


def adhoctest1():
  datelist = ['2025-4-7', '2025-6-20']
  print('Querying with datelist', datelist)
  datelist = cnv.trans_convertabledates_to_datelist(datelist)
  exrts = fetch_exrts_inside_datelist_via_sqlalchemy(datelist)
  for exrt in exrts:
    print('\t', exrt.refdate, exrt)
  if exrts.count() == 0:
    print('\tdone, got no recs with the datelist above')
  else:
    print('\t count', exrts.count())
  # ========================
  dateini = datelist[0]
  dateini = cnv.make_date_or_none(dateini)
  datefim = datelist[1]
  datefim = cnv.make_date_or_none(datefim)
  print('Querying with date range', dateini, datefim)
  exrts = fetch_exrts_wi_daterange_via_sqlalchemy(dateini, datefim)
  for exrt in exrts:
    print('\t', exrt.refdate, exrt)
  if exrts.count() == 0:
    print('\tdone, got no recs with date range')
  else:
    print('\t count', exrts.count())


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoctest1()
