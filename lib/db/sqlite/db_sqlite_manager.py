"""
lib/db/sqlite/db_sqlite_manager.py
  Manages a Sqlite connection with opening a connection, cursor execution et al.

This module is a slighly adjusted/changed version from DeepSeek on 2025-07-14

Features:
  Connection Management:
    Automatic connection handling
    Context manager support (with statement)
    Connection pooling ready
  CRUD Operations:
    execute() - Run SQL commands
    executemany() - Run the same command with multiple parameter sets
    executescript() - Run multiple SQL commands at once
    fetch_one() - Get a single row
    fetch_all() - Get all rows
    fetch_as_dict() - Get rows as dictionaries
  Transaction Support:
    Automatic commit/rollback
    Explicit transaction control
  Utility Methods:
    Check if table exists
    Get table columns
    Database backup
    Vacuum (optimize) database
  Error Handling:
    Comprehensive error logging
    Clean rollback on failure
  Type Hints:
    Full type annotations for better IDE support
"""
import sqlite3
from typing import Optional, List, Union  # , Dict, Any, Tuple
from pathlib import Path
import logging


class SqliteHandler:
  """
  lib.db.sqlite.db_sqlite_manager.SqliteHandler

  A wrapper class for SQLite3 database operations.

  Features:
  - Automatic connection management
  - Context manager support (with statement)
  - Basic CRUD operations
  - Transaction support
  - Error handling
  - Type hints

  Example usage:
      with SQLiteDB('mydatabase.db') as db:
          # Create a table
          db.execute('''CREATE TABLE IF NOT EXISTS users
                       (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

          # Insert data
          db.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))

          # Query data
          users = db.fetch_all('SELECT * FROM users')
          print(users)
  """

  def __init__(
      self,
      db_path: Union[str, Path],
      timeout: float = 5.0,
      detect_types: int = 0,
      isolation_level: Optional[str] = None
    ):
    """
    Initialize the database wrapper.

    Args:
        db_path: Path to the SQLite database file
        timeout: How many seconds the connection should wait before raising an exception
        detect_types: Custom type detection (see sqlite3 docs)
        isolation_level: None for autocommit mode, or one of "DEFERRED", "IMMEDIATE", "EXCLUSIVE"
    """
    self.db_path = Path(db_path)
    self.timeout = timeout
    self.detect_types = detect_types
    self.isolation_level = isolation_level
    self._connection: Optional[sqlite3.Connection] = None
    self._in_transaction = False
    # Configure logging
    self.logger = logging.getLogger(__name__)
    self.logger.addHandler(logging.NullHandler())

  def __enter__(self) -> 'SqliteHandler':
    """Enter the context manager, opening a connection."""
    self.connect()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb) -> None:
    """Exit the context manager, closing the connection."""
    self.close()

  def connect(self) -> None:
    """Establish a connection to the database."""
    if self._connection is not None:
      self.logger.warning('Connection already exists')
      return
    try:
      self._connection = sqlite3.connect(
        str(self.db_path),
        timeout=self.timeout,
        detect_types=self.detect_types,
        isolation_level=self.isolation_level
      )
      # Enable foreign key constraints by default
      self.execute('PRAGMA foreign_keys = ON')
      self.logger.info(f'Connected to database at {self.db_path}')
    except sqlite3.Error as e:
      self.logger.error(f'Failed to connect to database: {e}')
      raise

  def close(self) -> None:
    """Close the database connection."""
    if self._connection is not None:
      try:
        if self._in_transaction:
          self.rollback()
        self._connection.close()
        self.logger.info('Database connection closed')
      except sqlite3.Error as e:
        self.logger.error(f'Error closing connection: {e}')
        raise
      finally:
        self._connection = None

  def execute(
      self,
      query: str,
      params: Union[tuple, dict, None] = None
    ) -> sqlite3.Cursor:
    """
    Execute a SQL query.

    Args:
        query: SQL query string
        params: Parameters to substitute in the query

    Returns:
        A cursor object
    """
    self._ensure_connection()

    try:
      cursor = self._connection.cursor()
      if params:
        cursor.execute(query, params)
      else:
        cursor.execute(query)
      self.logger.debug(f'Executed query: {query}')
      return cursor
    except sqlite3.Error as e:
      self.logger.error(f'Error executing query "{query}": {e}')
      raise

  def executemany(
      self,
      query: str,
      params_list: List[Union[tuple, dict]]
    ) -> sqlite3.Cursor:
    """
    Execute a SQL query multiple times with different parameters.

    Args:
        query: SQL query string
        params_list: Sequence of parameters

    Returns:
        A cursor object
    """
    self._ensure_connection()

    try:
      cursor = self._connection.cursor()
      cursor.executemany(query, params_list)
      self.logger.debug(f'Executed many for query: {query}')
      return cursor
    except sqlite3.Error as e:
      self.logger.error(f'Error executing many for query "{query}": {e}')
      raise

  def executescript(self, script: str) -> sqlite3.Cursor:
    """
    Execute a SQL script containing multiple statements.

    Args:
        script: SQL script string

    Returns:
        A cursor object
    """
    self._ensure_connection()

    try:
      cursor = self._connection.cursor()
      cursor.executescript(script)
      self.logger.debug(f'Executed script: {script[:100]}...')  # Log first 100 chars
      return cursor
    except sqlite3.Error as e:
      self.logger.error(f'Error executing script: {e}')
      raise

  def fetch_one(
      self,
      query: str,
      params: Union[tuple, dict, None] = None
    ) -> Optional[tuple]:
    """
    Execute a query and return a single row.

    Args:
        query: SQL query string
        params: Parameters to substitute in the query

    Returns:
        A single row as a tuple, or None if no results
    """
    cursor = self.execute(query, params)
    return cursor.fetchone()

  def fetch_all(
      self,
      query: str,
      params: Union[tuple, dict, None] = None
    ) -> List[tuple]:
    """
    Execute a query and return all rows.

    Args:
        query: SQL query string
        params: Parameters to substitute in the query

    Returns:
        A list of rows (each row is a tuple)
    """
    cursor = self.execute(query, params)
    return cursor.fetchall()

  def fetch_as_dict(
      self, query: str,
      params: Union[tuple, dict, None] = None
    ) -> List[dict]:
    """
    Execute a query and return all rows as dictionaries.

    Args:
        query: SQL query string
        params: Parameters to substitute in the query

    Returns:
        A list of dictionaries representing rows
    """
    self._ensure_connection()
    self._connection.row_factory = sqlite3.Row
    try:
      cursor = self._connection.cursor()
      cursor.execute(query, params)
      rows = cursor.fetchall()
      return [dict(row) for row in rows]
    finally:
      self._connection.row_factory = None

  def commit(self) -> None:
    """Commit any pending transaction to the database."""
    if self._connection is not None:
      try:
        self._connection.commit()
        self._in_transaction = False
        self.logger.debug('Changes committed')
      except sqlite3.Error as e:
        self.logger.error(f'Error committing transaction: {e}')
        raise

  def rollback(self) -> None:
    """Roll back any pending transaction."""
    if self._connection is not None and self._in_transaction:
      try:
        self._connection.rollback()
        self._in_transaction = False
        self.logger.debug('Transaction rolled back')
      except sqlite3.Error as e:
        self.logger.error(f'Error rolling back transaction: {e}')
        raise

  def begin_transaction(self) -> None:
    """Begin a transaction explicitly."""
    self._ensure_connection()
    if not self._in_transaction:
      self.execute('BEGIN')
      self._in_transaction = True
      self.logger.debug('Transaction begun')

  def table_exists(self, table_name: str) -> bool:
    """
    Check if a table exists in the database.

    Args:
        table_name: Name of the table to check

    Returns:
        True if the table exists, False otherwise
    """
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    result = self.fetch_one(query, (table_name,))
    return result is not None

  def get_table_columns(self, table_name: str) -> List[str]:
    """
    Get the column names of a table.

    Args:
        table_name: Name of the table

    Returns:
        List of column names
    """
    cursor = self.execute(f'PRAGMA table_info({table_name})')
    return [row[1] for row in cursor.fetchall()]

  def vacuum(self) -> None:
    """Rebuild the database file, repacking it into the minimal amount of space."""
    self.execute('VACUUM')
    self.logger.info('Database vacuumed')

  def backup(self, target_path: Union[str, Path]) -> None:
    """
    Create a backup of the database.

    Args:
        target_path: Path to save the backup
    """
    target_path = Path(target_path)
    self._ensure_connection()

    try:
      with sqlite3.connect(str(target_path)) as backup_conn:
        self._connection.backup(backup_conn)
      self.logger.info(f'Database backed up to {target_path}')
    except sqlite3.Error as e:
      self.logger.error(f'Error creating backup: {e}')
      raise

  def _ensure_connection(self) -> None:
    """Ensure we have an active database connection."""
    if self._connection is None:
      self.connect()

  @property
  def lastrowid(self) -> Optional[int]:
    """Get the rowid of the last inserted row."""
    if self._connection is not None:
      return self._connection.cursor().lastrowid
    return None

  @property
  def total_changes(self) -> int:
    """Get the total number of database rows that have been modified."""
    if self._connection is not None:
      return self._connection.total_changes
    return 0
