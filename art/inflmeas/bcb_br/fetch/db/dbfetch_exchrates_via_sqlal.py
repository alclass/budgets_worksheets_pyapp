"""
BudgetsWorksheets:
  art/inflmeas/bcb_br/fetch/db/dbfetch_exchrates_via_sqlal.py
    Fetches currency exchange rates via SqlAlchemy DB accessor
"""
import lib.db.sqlalch.sqlalchemy_connection_clsmod as sqlal  # sqlal.SqlAlchemyConnector
import art.inflmeas.bcb_br.classes.daycurrexchrate_sqlal as exchsqlal  # exchsqlal.SADayCurrExchRate
import art.inflmeas.bcb_br.classes.daterangecurrexchrate_mod as daterang  # daterang.DateRangeCurrExchRate
from sqlalchemy import select  # create_engine, Column, Integer, Date,


class Fetcher(daterang.DateRangeCurrExchRate):

  def __init__(self, date_fr=None, date_to=None, datelist=None, curr_num=None, curr_den=None):
    """
    how to use the super() function in python class inheritance?
    """
    super().__init__(date_fr, date_to, datelist, curr_num, curr_den)
    sqlal_o = sqlal.SqlAlchemyConnector()
    self.session = sqlal_o.get_sa_session()

  def fetch_by_daterange(self):
    """
    Fetching by daterange means datefrom <= refdate <= dateto
      i.e., the object's refdate is within (in-between) given date range

    how to write query with greater than and less than dates with Python's sqlalchemy?
    """
    tab = exchsqlal.SADayCurrExchRate
    refdate = tab.refdate
    # Query for events before a specific date
    query = select(tab).where(refdate >= self.date_fr).where(refdate <= self.date_to)
    results = self.session.execute(query).scalars().all()
    for i, res in enumerate(results):
      seq = i + 1
      print(seq, res)

  def fetch2(self):
    """

    """
    tab = exchsqlal.SADayCurrExchRate
    results = self.session.query(tab).filter(
      tab.refdate >= self.date_fr,
      tab.refdate <= self.date_to
    ).all()
    return results

  def fetch(self):
    tab = exchsqlal.SADayCurrExchRate
    refdate = tab.refdate
    exrates = self.session.query(tab). \
        order_by(refdate). \
        all()
    scrmsg = f"""ExchangeRateDate: 1) create table | 2) read table 
    tablename = {exchsqlal.SADayCurrExchRate.__tablename__} | Base.metadata.create_all(con.sqlalchemy_engine
    """
    print(scrmsg)
    for i, exrate in enumerate(exrates):
      print(i + 1, exrate)
    print('Total records =', len(exrates))

  def process(self):
    self.fetch()


def adhoctest():
  date_fr, date_to = '2024-1-1', '2025-1-1'
  fetcher = Fetcher(date_fr='2024-1-1', date_to=date_to)
  # fetcher.process()
  fetcher.fetch_by_daterange()
  print(fetcher)
  print('dict size =', len(fetcher.dates_n_exchrates_dict))
  print('fetch2')
  results = fetcher.fetch2()
  for i, res in enumerate(results):
    seq = i + 1
    print(seq, res)
  print('dict size =', len(fetcher.dates_n_exchrates_dict))


def process():
  pass


if __name__ == "__main__":
  adhoctest()
