#!/usr/bin/env python3
"""
fs/db/db_settings.py

"""
IDXIND_TABLENAME = 'idxind_monthly_indices'
EXRATE_TABLENAME = 'currencies_exchangerates'
EXRATE_INTEGER_TO_FLOAT_DIVISOR = 10000  # ie a quote with 51234 means 5,1234
DEFAUT_CURRENCY_PAIR = ('BRL', 'USD')
