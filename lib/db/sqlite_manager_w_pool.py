#!/usr/bin/env python3
"""
lib/db/db_manager.py

"""
import sqlite3
import datetime
import threading
import queue
import time
import logging
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class DbManagerPool:

  def __init__(self, db_path, pool_size=5, max_retries=5, retry_delay=0.5):
    self.db_path = db_path
    self.pool = queue.Queue(maxsize=pool_size)
    self.local = threading.local()
    self.max_retries = max_retries
    self.retry_delay = retry_delay
    for _ in range(pool_size):
      conn = sqlite3.connect(
        db_path,
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False
      )
      conn.execute("PRAGMA journal_mode=WAL;")
      self.pool.put(conn)
    self.register_adapters()

  @staticmethod
  def register_adapters():
    sqlite3.register_adapter(datetime.date, lambda val: val.isoformat())
    sqlite3.register_converter("DATE", lambda val: datetime.date.fromisoformat(val.decode()))
    sqlite3.register_adapter(datetime.datetime, lambda val: val.isoformat(sep=' '))
    sqlite3.register_converter("DATETIME", lambda val: datetime.datetime.fromisoformat(val.decode()))

  def get_connection(self):
    if not hasattr(self.local, "conn"):
      self.local.conn = self.pool.get()
    return self.local.conn

  def release_connection(self):
    if hasattr(self.local, "conn"):
      self.pool.put(self.local.conn)
      del self.local.conn

  def __enter__(self):
    self.conn = self.get_connection()
    self.cursor = self.conn.cursor()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type is None:
      self.conn.commit()
    else:
      self.conn.rollback()
    self.cursor.close()
    self.release_connection()

  def execute(self, sql, values=None):
    attempt = 0
    while attempt < self.max_retries:
      try:
        self.cursor.execute(sql, values or [])
        return self.cursor.fetchall()
      except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
          logger.warning(f"SQLITE_BUSY: retrying ({attempt + 1}/{self.max_retries})...")
          time.sleep(self.retry_delay)
          attempt += 1
        else:
          raise
    logger.error("Max retries reached due to SQLITE_BUSY.")
    raise Exception("Max retries reached due to SQLITE_BUSY.")


def adhoctest():
  """
🧪 Example Usage
python
  from db_pool import DbManagerPool
  import datetime
  """
  with DbManagerPool("mydata.sqlite", pool_size=10) as db:
    db.execute(
      "INSERT INTO logs (event_name, event_time) VALUES (?, ?)",
      ("Logged Retry", datetime.datetime.now())
    )


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest2()
  """
  process()
  adhoctest()
