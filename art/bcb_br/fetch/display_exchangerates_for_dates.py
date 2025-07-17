#!/usr/bin/env python3
"""
art/bcb_br/fetch/display_exchangerates_for_dates.py

This script reads dates (either input from terminal or from a datefile in the app's data folder)
  and fetches its corresponding exchange rate quotes.
For the time being, it only finds and prints BRL (reais) /USD (dollars) exchange rate quotes.
  It's planned other combinations (one currency to another currency) to be implemented in the future.

The output text contains:
  - in the first column the input dateadhoctests and
  - in the second the day-to-day 'sell quotes *
    * 'cotação de venda' do par de moedas

Usage:
$show_exchangerates_for_dates.py -ini=<start_date> [-fim=<end_date>] | -datafile
  where
    -ini=<start_date> is the date beginning the date range
    [-fim=<end_date>] [optional] is the date ending the date range
    -datafile is a marker (not a name) for reading the system's conventioned datefile (*)
      (*) the datefile is a text file that is inside the app's data folder (the folder is informed in the config)

Examplee:
$show_exchangerates_for_dates.py -ini=2023-05-20 -fim=2023-08-14

The combination above will display all quotes from May 20, 2023, to August 14, 2023

  Obs: weekends and hollidays do not have quotes.
       The system repeats the last one available when such dateadhoctests are requested.
       Example: if Sunday's quotes are requested, Friday's one, if available, are output.
"""
import calendar
import datetime
# import datetime
import sys
import art.bcb_br.fetch.report.corr_monet_n_indices_calculator_from_dates as composite
import lib.indices.bcb_br.bcb_cotacao_fetcher_from_db_or_api as fin
import lib.datefs.dategenerators as gendt
import lib.datefs.refmonths_mod as rmd
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import argparse


def show_exchangerates_between_dates():
  pydates = composite.get_dates_from_strdates_file()
  for pdate in pydates:
    bcber = fin.BCBCotacaoFetcher(pdate)
    ntcotacao = bcber.namedtuple_cotacao
    print(str(pdate), ntcotacao)


def show_exchangerates_for_rangedate(date_ini, date_fim, decrescent=False):
  for i, pdate in enumerate(gendt.gen_dailydates_or_empty_bw_ini_fim_opt_order(date_ini, date_fim, decrescent)):
    bcber = fin.BCBCotacaoFetcher(pdate)
    bcb_api_nt = bcber.namedtuple_cotacao
    if bcb_api_nt:
      print(i+1, pdate, '|', bcb_api_nt.cotacao_venda)
    else:
      print(i+1, pdate, '| no quote')


def show_exchangerates_for_refmonth(p_refmonthdate, decrescent=False):
  refmonthdate = rmd.make_refmonth_or_current(p_refmonthdate)
  date_ini = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  _, monthslastday = calendar.monthrange(year=refmonthdate.year, month=refmonthdate.month)
  date_fim = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=monthslastday)
  return show_exchangerates_for_rangedate(date_ini, date_fim, decrescent)


def show_exchangerates_for_last_month(decrescent=False):
  for i, pdate in enumerate(gendt.gen_dailydates_for_last_month_opt_order_cday_accfut(decrescent)):
    bcber = fin.BCBCotacaoFetcher(pdate)
    bcb_api_nt = bcber.namedtuple_cotacao
    print(i+1, pdate, '|', bcb_api_nt.cotacao_venda)


def show_exchangerates_for_yearrange(yearini, yearfim=None, decrescent=False):
  if yearini is None:
    print('year ini %d not valid' % yearini)
    return
  if yearfim is None:
    today = datetime.date.today()
    yearfim = today.year
  try:
    yearini = int(yearini)
    yearfim = int(yearfim)
  except ValueError:
    scrmsg = 'year range not valid (%s, %s)' % (str(yearini), str(yearfim))
    print(scrmsg)
    return
  scrmsg = 'year range (%s, %s)' % (str(yearini), str(yearfim))
  print(scrmsg)
  for year in range(yearini, yearfim+1):
    for i, pdate in enumerate(gendt.gen_dailydates_or_empty_for_year_opt_order_coff_accfut(year, decrescent)):
      bcber = fin.BCBCotacaoFetcher(pdate)
      bcb_api_nt = bcber.namedtuple_cotacao
      print(i+1, pdate, '|', bcb_api_nt.cotacao_venda)


def show_exchangerates_for_year(year, decrescent=False):
  for i, pdate in enumerate(gendt.gen_dailydates_or_empty_for_year_opt_order_coff_accfut(year, decrescent)):
    bcber = fin.BCBCotacaoFetcher(pdate)
    bcb_api_nt = bcber.namedtuple_cotacao
    print(i+1, pdate, '|', bcb_api_nt.cotacao_venda)


def show_exchangerates_for_current_year(decrescent=False):
  for i, pdate in enumerate(gendt.gen_dailydates_for_current_year_opt_order_coff_accfut(decrescent)):
    bcber = fin.BCBCotacaoFetcher(pdate)
    bcb_api_nt = bcber.namedtuple_cotacao
    print(i+1, pdate, '|', bcb_api_nt.cotacao_venda)


def adhoctest():
  """
  pastdate = '2020-10-15'
  pydate = datetime.date(2020, 10, 15)
  """
  # show_exchangerates_between_dates()
  # show_exchangerates_for_last_month()
  show_exchangerates_for_current_year()


def get_args_via_argparse():
  """
  https://realpython.com/command-line-interfaces-python-argparse/
  One Example:
    parser.add_argument("--veggies", nargs="+")
    parser.add_argument("--fruits", nargs="*")
      $ python cooking.py --veggies pepper tomato --fruits apple banana
    parser.add_argument("--size", choices=["S", "M", "L", "XL"], default="M")
    my_parser.add_argument("--weekday", type=int, choices=range(1, 8))
  """
  parser = argparse.ArgumentParser(description="Obtain Arguments")
  parser.add_argument(
    '-i', '--ini', metavar='date_ini', type=str, nargs=1,
    help="the beginning date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-f', '--fim', metavar='date_fim', type=str, nargs='?',
    help="the ending date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-rm', '--refmonth', type=str, nargs='?',
    help="the month as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-cy', '--current-year',  action='store_true',
    help="days since the beginning of the current year as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-y', '--year', type=int, nargs=1,
    help="year as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-yr', '--yearrange', type=int, nargs=2,
    help="year range (ini, fim) as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
      '-rdf', '--readdatefile', action='store_true',
      help="marker/signal for inputting the dateadhoctests from"
           " the conventioned datefile located in the app's data folder",
  )
  parser.add_argument(
    '-cp', '--currencypair', type=str, nargs=1, default='brl/usd',
    help="for specifying the currency pair ratio that corresponds to the output quotes (default 'brl/usd')",
  )
  args = parser.parse_args()
  print('args =>', args)
  if args.refmonth is not None:
    return show_exchangerates_for_refmonth(args.refmonth)
  if args.year is not None:
    year = args.year[0]
    return show_exchangerates_for_year(year)
  if args.yearrange is not None:
    yearini = args.yearrange[0]
    yearfim = args.yearrange[1]
    return show_exchangerates_for_yearrange(yearini, yearfim)
    # print(yearini, yearfim)


def get_args():
  """
  example parameters: -ini=2023-05-20 -fim=2023-08-14
  """
  paramdict = {}
  for arg in sys.argv:
    if arg in ['-h', '--help']:
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-datefile'):
      paramdict['datefilemarker'] = True
      return paramdict
    elif arg.startswith('-ini='):
      strdate = arg[len('-ini='):]
      date_ini = cnv.make_date_or_none(strdate)
      paramdict['date_ini'] = date_ini
    elif arg.startswith('-fim='):
      strdate = arg[len('-fim='):]
      date_fim = cnv.make_date_or_none(strdate)
      paramdict['date_fim'] = date_fim
  return paramdict


def process_via_sysargv():
  paramdict = get_args()
  if 'datefilemarker' in paramdict:
    scrmsg = ('At this version, datefilemarker has not yet been implemented.\n'
              ' dateini & datefim are the ones implemented at this time.\n'
              ' Use parameter -h or --help for usage and example.')
    print(scrmsg)
    sys.exit(0)
  if 'date_ini' not in paramdict:
    print(__doc__)
    print('Please, enter at least the first date (date ini) of range and rerun.')
    sys.exit(1)
  date_ini = paramdict['date_ini']
  date_fim = None
  if 'date_fim' in paramdict:
    date_fim = paramdict['date_fim']
  show_exchangerates_for_rangedate(date_ini, date_fim)


def process():
  get_args_via_argparse()


if __name__ == '__main__':
  """
  adhoctest1()
  """
  process()
