#!/usr/bin/env python3
"""
lib/db/db_settings.py
  Keeps db-related attribute parameters not placed in
    the system-wide settings.py
"""
IDXIND_TABLENAME = 'idxind_monthly_indices'
EXRATE_TABLENAME = 'currencies_exchangerates'
EXRATE_INTEGER_TO_FLOAT_DIVISOR = 10000  # ie a quote with 51234 means 5,1234
DEFAULT_CURRENCY_PAIR = ('BRL', 'USD')
