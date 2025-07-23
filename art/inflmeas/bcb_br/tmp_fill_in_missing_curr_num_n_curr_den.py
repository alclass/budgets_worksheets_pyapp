#!/usr/bin/env python3
"""
commands/db/bcb_br/tmp_fill_in_missing_curr_num_n_curr_den.py
  Inserts the default curr_num (currency numerator) and curr_den (currency numerator) into the exchange rates table.

The defaults:
  'BRL' (Brazilian Real) is the default curr_num (currency numerator)
  'USD' (US Dollar) is the default curr_den (currency numerator)

This script was created because the original sql-table did not have these two fields
  at the beginning, partly because only the default currency pair
  (BRL/USD) was treated in the package/system originally.
"""
import settings as sett
import lib.db.db_settings as dbs
BRL, USD = 'BRL', 'USD'


class Updater:

  def __init__(self):
    self.n_updated = 0
    self.conn = None

  def get_n_set_connection(self):
    self.conn = sett.get_sqlite_connection()

  def update_db(self):
    sql = f"""
    UPDATE `{dbs.EXCHRATE_DBTABLENAME}`
      SET 
        curr_num="{BRL}",
        curr_den="{USD}"
      WHERE 
        curr_num is null and
        curr_den is null;
    """
    print(sql)
    cursor = self.conn.cursor()
    retval = cursor.execute(sql)
    if retval:
      print('committing; retval =', retval)
      self.n_updated = retval.rowcount
      self.conn.commit()

  def process_update_db(self):
    self.get_n_set_connection()
    self.update_db()
    self.conn.close()


def adhoctest():
  """
  """
  pass


def process():
  upt = Updater()
  upt.process_update_db()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
